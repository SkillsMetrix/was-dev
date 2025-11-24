terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  region     = "us-east-1"
  access_key = ""
  secret_key = ""
}

# Create minimal VPC
resource "aws_vpc" "v" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
}

# Subnet
resource "aws_subnet" "s" {
  vpc_id            = aws_vpc.v.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.v.id
}

# Route Table
resource "aws_route_table" "rt" {
  vpc_id = aws_vpc.v.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

# Associate route table with subnet
resource "aws_route_table_association" "rta" {
  subnet_id      = aws_subnet.s.id
  route_table_id = aws_route_table.rt.id
}

# Security group (SSH open)
resource "aws_security_group" "sg" {
  name   = "tf-sg"
  vpc_id = aws_vpc.v.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 instance
resource "aws_instance" "web" {
  ami                    = "ami-0f34c5ae932e6f0e4"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.s.id
  vpc_security_group_ids = [aws_security_group.sg.id]

  tags = {
    Name = "minimal-ec2"
  }
}

output "public_ip" {
  value = aws_instance.web.public_ip
}
