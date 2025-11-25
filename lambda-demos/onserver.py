import json

def lambda_handler(event, context):
    # Extract the string from the event payload
    string = event.get('string', '')

    # Reverse the string
    reversed_string = string[::-1]

    return {
        'statusCode': 200,
        'body': json.dumps({
            'original': string,
            'reversed': reversed_string
        })
    }
