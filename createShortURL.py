import os
import json
import uuid
import boto3
from datetime import datetime, timezone, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    # parse request body
    body = json.loads(event.get('body', '{}'))
    long_url = body.get('url')
    if not long_url:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing "url" in request body'})
        }
    
    MIN_URL_LENGTH = 20
    if len(long_url) < MIN_URL_LENGTH:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'URL is too short. Please enter a URL with at least {MIN_URL_LENGTH} characters.'})
        }

    # generate or use custom short code
    short_code = body.get('custom_code') or uuid.uuid4().hex[:6]

    # prepare expiry timestamp
    if 'expiry' in body:
        try:
            expiry_ts = int(body['expiry'])
        except ValueError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': '"expiry" must be an integer timestamp'})
            }
    else:
        # default expiry: 30 days from now
        expiry_ts = int((datetime.now(timezone.utc) + timedelta(days=30)).timestamp())

    # prepare item for DynamoDB
    item = {
        'short_code': short_code,
        'long_url': long_url,
        'expiry': expiry_ts
    }

    # write to DynamoDB
    table.put_item(Item=item)

    # build response
    base = os.environ.get('BASE_URL', '').rstrip('/')
    short_url = f"{base}/{short_code}"
    return {
        'statusCode': 200,
        'body': json.dumps({'short_url': short_url})
    }
