import json
import boto3
import logging

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Track')  # Ensure this is your correct table name

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Allow all origins
        'Access-Control-Allow-Methods': 'OPTIONS, POST, GET, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    if event['httpMethod'] == 'PUT':
        try:
            # Get the track_id from the URL path
            track_id = event['pathParameters']['track_id']
            
            # Parse the request body
            body = json.loads(event['body'])
            
            # Validate required fields (except track_id, since it's from the path)
            required_fields = ['title', 'album_id', 'track_number', 'label']
            for field in required_fields:
                if field not in body:
                    return {
                        'statusCode': 400,
                        'body': json.dumps(f"Missing required field: {field}"),
                        'headers': headers,
                    }

            # Extract track details from the body
            updated_track = {
                'title': body['title'],
                'album_id': body['album_id'],
                'track_number': int(body['track_number']),
                'label': body['label']
            }

            # Update the track in DynamoDB
            response = table.update_item(
                Key={'track_id': track_id},
                UpdateExpression="set title = :t, album_id = :a, track_number = :n, label = :l",
                ExpressionAttributeValues={
                    ':t': updated_track['title'],
                    ':a': updated_track['album_id'],
                    ':n': updated_track['track_number'],
                    ':l': updated_track['label']
                },
                ReturnValues="UPDATED_NEW"
            )

            # Log successful update
            logger.info(f"Track {track_id} updated successfully.")

            return {
                'statusCode': 200,
                'body': json.dumps('Track updated successfully.'),
                'headers': headers,
            }

        except Exception as e:
            # Log the error
            logger.error(f"Error updating track: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps(f"Error updating track: {str(e)}"),
                'headers': headers,
            }

    elif event['httpMethod'] == 'OPTIONS':
        # Return headers for pre-flight OPTIONS request
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(''),
        }

    else:
        return {
            'statusCode': 405,
            'body': json.dumps('Method Not Allowed'),
            'headers': headers,
        }
