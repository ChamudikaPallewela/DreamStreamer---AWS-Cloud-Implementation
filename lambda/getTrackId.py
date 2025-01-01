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

    if event['httpMethod'] == 'GET':
        try:
            # Extract track_id from the path parameters
            track_id = event['pathParameters']['track_id']
            
            # Fetch the track from DynamoDB
            response = table.get_item(
                Key={'track_id': track_id}
            )

            # Check if the item was found
            if 'Item' in response:
                track = response['Item']
                return {
                    'statusCode': 200,
                    'body': json.dumps(track),
                    'headers': headers
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps(f"Track with track_id {track_id} not found."),
                    'headers': headers
                }

        except Exception as e:
            # Log the error
            logger.error(f"Error fetching track: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps(f"Error fetching track: {str(e)}"),
                'headers': headers
            }

    elif event['httpMethod'] == 'OPTIONS':
        # Return headers for pre-flight OPTIONS request
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('')
        }

    else:
        return {
            'statusCode': 405,
            'body': json.dumps('Method Not Allowed'),
            'headers': headers
        }
