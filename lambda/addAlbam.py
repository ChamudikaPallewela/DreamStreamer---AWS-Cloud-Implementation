import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
table = dynamodb.Table('Album')

# Replace with your SNS topic ARN
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:157070555729:notification'

def lambda_handler(event, context):
    try:
        if 'body' not in event:
            raise ValueError("Missing 'body' in the event")

        body = json.loads(event['body'])
        
        # Generate a UUID for the album ID
        album_id = str(uuid.uuid4())
        
        # Save album details to DynamoDB
        response = table.put_item(
            Item={
                'album_id': album_id,  # Primary key
                'title': body['title'],
                'genre': body['genre'],  # Reference to Genre table
                'year': int(body['year']),
                'artist_id': body['artist_id'],  # Reference to Artist table
                'album_art_url': body['album_art_url']
            }
        )
        
        # Publish message to SNS topic
        sns_message = {
            'subject': 'New Album Added!',
            'message': f"A new album '{body['title']}' has been added to the collection.",
            'topicArn': SNS_TOPIC_ARN
        }
        
        sns.publish(
            TopicArn=sns_message['topicArn'],
            Subject=sns_message['subject'],
            Message=sns_message['message']
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Album saved and notification sent successfully', 'albumId': album_id})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Error saving album', 'error': str(e)})
        }
