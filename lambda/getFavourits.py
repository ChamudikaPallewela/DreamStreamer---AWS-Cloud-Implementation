import json
import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('playlist')

def lambda_handler(event, context):
    # Get the username from the event (assume it's passed in query params)
    username = event.get('queryStringParameters', {}).get('username')
    
    if not username:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins, adjust as needed
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'username is required'})
        }
    
    # Scan DynamoDB for all favorite tracks of the user
    try:
        response = table.scan(
            FilterExpression=Attr('username').eq(username)
        )
        
        favorites = response.get('Items', [])
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins, adjust as needed
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(favorites)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins, adjust as needed
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
