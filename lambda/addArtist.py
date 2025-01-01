import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Artist')

def lambda_handler(event, context):
    try:
        if 'body' not in event:
            raise ValueError("Missing 'body' in the event")
        
        body = json.loads(event['body'])
        
        # Generate a UUID for the artist ID
        artist_id = str(uuid.uuid4())
        
        # Ensure 'imageUrl' is present in the body
        if 'imageUrl' not in body:
            raise ValueError("Missing 'imageUrl' in the request body")

        # Save artist details to DynamoDB, including the image URL
        response = table.put_item(
            Item={
                'artist_id': artist_id,  # Primary key
                'name': body['name'],
                'band_composition': body['bandComposition'],
                'image_url': body['imageUrl']  # Image URL from S3
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Artist saved successfully', 'artistId': artist_id})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Error saving artist', 'error': str(e)})
        }
