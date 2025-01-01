import json
import boto3
from decimal import Decimal

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Album')  # Replace with your DynamoDB table name

# Custom JSON encoder to handle Decimal type
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    try:
        # Get artist_id from path parameters
        artist_id = event['pathParameters'].get('artist_id')
        
        if not artist_id:
            return {
                'statusCode': 400,
                'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
                'body': json.dumps({'error': 'Missing artist_id path parameter'})
            }
        
        # Query DynamoDB to get albums for the given artistId
        response = table.scan(
            FilterExpression='artist_id = :artist_id',
            ExpressionAttributeValues={':artist_id': artist_id}
        )
        
        # Check if items are returned
        albums = response.get('Items', [])
        
        if not albums:
            return {
                'statusCode': 404,
                'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
                'body': json.dumps({'message': 'No albums found for this artist_id'})
            }
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allows requests from any origin
                'Access-Control-Allow-Methods': 'GET',  # Allows GET requests
                'Content-Type': 'application/json'
            },
            'body': json.dumps(albums, cls=DecimalEncoder)  # Use custom encoder for Decimal
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'Error retrieving albums', 'error': str(e)})
        }
