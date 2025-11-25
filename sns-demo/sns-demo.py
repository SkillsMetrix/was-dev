import boto3

# -----------------------------
# CONFIGURATION
# -----------------------------
AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""
AWS_REGION = "us-east-1"

TOPIC_NAME = "amartop"
EMAIL_TO_SUBSCRIBE = "amarjeet.sn1@gmail.com"
SUBJECT = "Test Email from AWS SNS + Python"
MESSAGE = "Hello! This is a test email sent using AWS SNS from Python."

# -----------------------------
# CREATE SNS CLIENT
# -----------------------------
sns = boto3.client(
    "sns",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# -----------------------------
# 1. CREATE SNS TOPIC
# -----------------------------
topic = sns.create_topic(Name=TOPIC_NAME)
topic_arn = topic["TopicArn"]
print("Topic ARN:", topic_arn)

# -----------------------------
# 2. SUBSCRIBE EMAIL TO TOPIC
# -----------------------------
sub = sns.subscribe(
    TopicArn=topic_arn,
    Protocol="email",
    Endpoint=EMAIL_TO_SUBSCRIBE
)
print("Subscription ARN (PendingConfirmation):", sub["SubscriptionArn"])

print("⚠️ Check your email and CONFIRM the subscription before sending!")

# -----------------------------
# 3. PUBLISH MESSAGE TO TOPIC
# -----------------------------
publish_response = sns.publish(
    TopicArn=topic_arn,
    Subject=SUBJECT,
    Message=MESSAGE
)

print("Email sent! Message ID:", publish_response["MessageId"])
