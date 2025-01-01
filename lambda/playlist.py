import json
import boto3
import uuid
from botocore.exceptions import ClientError
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('playlist')

def generate_playlist_id(username):
    """Generates a unique playlist_id for the user."""
    # For example, we can concatenate username with 'favourite' or use UUID
    return f'{username}-favourite-{uuid.uuid4()}'

def lambda_handler(event, context):
    # Parse the incoming request body
    body = json.loads(event.get('body', '{}'))
    
    track_id = body.get('track_id')
    track_name = body.get('track_name')
    username = body.get('username')
    
    if not track_id or not track_name or not username:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'track_id, track_name, and username are required'})
        }
    
    # Generate a unique playlist_id using the username
    playlist_id = generate_playlist_id(username)
    
    # Prepare the item for DynamoDB
    item = {
        'playlist_id': playlist_id,
        'track_id': track_id,
        'username': username,
        'track_name': track_name,
        'added_at': datetime.utcnow().isoformat()
    }
    
    try:
        # Insert the item into the DynamoDB table
        table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(track_id)'  # Prevent adding the same track twice
        )
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Track added to favorites', 'playlist_id': playlist_id})
        }
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
                'statusCode': 409,
                'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
                'body': json.dumps({'message': 'Track is already in favorites'})
            }
        else:
            return {
                'statusCode': 500,
                'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
                'body': json.dumps({'message': 'Internal server error'})
            }
