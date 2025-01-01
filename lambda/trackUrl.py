import json
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
track_table = dynamodb.Table('Track')  # DynamoDB table where track details are stored

# Lambda function to handle track download requests
def lambda_handler(event, context):
    try:
        # Extract the track_id from the query parameters
        track_id = event['queryStringParameters']['track_id']
        
        # Query DynamoDB for the track details (to get the mp3_url)
        response = track_table.get_item(
            Key={'track_id': track_id}
        )
        
        # Check if the track was found
        if 'Item' not in response:
            raise ValueError(f"Track with ID {track_id} not found")

        track = response['Item']
        mp3_url = track['mp3_url']  # Get the mp3_url from DynamoDB

        # Return the mp3_url in the response
        return {
            'statusCode': 200,
            'body': json.dumps({'mp3_url': mp3_url}),
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error fetching track', 'error': str(e)}),
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }
