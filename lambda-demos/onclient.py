import json
import boto3

client = boto3.client('lambda')
response = client.invoke(
    FunctionName='dem-python',
    Payload='{"string":"Demoapp"}'
)

print(response['Payload'].read())
