import boto3
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract bucket & key from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key    = event['Records'][0]['s3']['object']['key']

    print(f"File uploaded: {key} in bucket: {bucket}")

    # Read the file content (optional)
    file_obj = s3.get_object(Bucket=bucket, Key=key)
    content = file_obj['Body'].read().decode('utf-8')

    print("File Content:")
    print(content)

    return {
        'statusCode': 200,
        'body': json.dumps(f"Read file {key} successfully")
    }
