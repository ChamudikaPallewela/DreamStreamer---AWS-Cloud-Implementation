import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Track')

def lambda_handler(event, context):
    try:
        if 'body' not in event:
            raise ValueError("Missing 'body' in the event")
        
        body = json.loads(event['body'])
        
        # Generate a UUID for the track ID
        track_id = str(uuid.uuid4())
        
        # Save track details to DynamoDB
        response = table.put_item(
            Item={
                'track_id': track_id,  # Primary key
                'title': body['title'],
                'album_id': body['album_id'],  # Reference to Album table
                'track_number': int(body['track_number']),
                'label': body['label'],
                'mp3_url': body.get('mp3_url')  # Add mp3_url field
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Track saved successfully', 'trackId': track_id})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Error saving track', 'error': str(e)})
        }
