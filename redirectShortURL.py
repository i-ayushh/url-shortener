import os
import json
import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    # extract code from path
    code = event.get('pathParameters', {}).get('code')
    if not code:
        return {
            'statusCode': 400,
            'body': 'Missing path parameter "code"'
        }

    # fetch item from DynamoDB
    resp = table.get_item(Key={'short_code': code})
    item = resp.get('Item')

    # check existence and expiry
    now_ts = int(datetime.now(timezone.utc).timestamp())
    if not item or ('expiry' in item and item['expiry'] < now_ts):
        return {
            'statusCode': 404,
            'body': 'Not found'
        }

    # redirect to the original URL
    return {
        'statusCode': 301,
        'headers': {
            'Location': item['long_url']
        },
        'body': ''  # <-- important for API Gateway to pass headers cleanly
    }