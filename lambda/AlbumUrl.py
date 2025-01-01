import json
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
album_table = dynamodb.Table('Album')  # DynamoDB table where album details are stored

# Lambda function to handle album URL requests
def lambda_handler(event, context):
    try:
        # Extract the album_id from the query parameters
        album_id = event['queryStringParameters']['album_id']
        
        # Query DynamoDB for the album details (to get the album_art_url)
        response = album_table.get_item(
            Key={'album_id': album_id}
        )
        
        # Check if the album was found
        if 'Item' not in response:
            raise ValueError(f"Album with ID {album_id} not found")

        album = response['Item']
        album_art_url = album.get('album_art_url', 'URL not available')  # Get the album_art_url from DynamoDB

        # Return the album_art_url in the response
        return {
            'statusCode': 200,
            'body': json.dumps({'album_art_url': album_art_url}),
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error fetching album', 'error': str(e)}),
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }
