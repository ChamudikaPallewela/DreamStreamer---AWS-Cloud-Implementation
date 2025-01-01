import json
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
artist_table = dynamodb.Table('Artist')  # DynamoDB table where artist details are stored

# Lambda function to handle artist image URL requests
def lambda_handler(event, context):
    try:
        # Extract the artist_id from the query parameters
        artist_id = event['queryStringParameters']['artist_id']
        
        # Query DynamoDB for the artist details (to get the image_url)
        response = artist_table.get_item(
            Key={'artist_id': artist_id}
        )
        
        # Check if the artist was found
        if 'Item' not in response:
            raise ValueError(f"Artist with ID {artist_id} not found")

        artist = response['Item']
        image_url = artist.get('image_url', 'URL not available')  # Get the image_url from DynamoDB

        # Return the image_url in the response
        return {
            'statusCode': 200,
            'body': json.dumps({'image_url': image_url}),
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error fetching artist image', 'error': str(e)}),
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        }
