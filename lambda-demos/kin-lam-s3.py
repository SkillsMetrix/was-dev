#https://chatgpt.com/c/692489c3-3d3c-8323-89ce-24bab4f1ffae
import boto3
import json

kinesis = boto3.client(
    'kinesis',
    region_name='us-east-1'
)

STREAM_NAME = "my-demo-stream"

def send_dummy_data():
    records = [
        {"name": "John", "email": "john@test.com", "city": "Delhi"},
        {"name": "Emma", "email": "emma@test.com", "city": "Mumbai"},
        {"name": "Ravi", "email": "ravi@test.com", "city": "Pune"}
    ]

    for record in records:
        response = kinesis.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(record),
            PartitionKey="partition-1"
        )
        print("Sent:", record)

if __name__ == "__main__":
    send_dummy_data()
