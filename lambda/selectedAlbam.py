import json
import boto3
from decimal import Decimal

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Track')  # Replace with your DynamoDB table name

# Custom JSON encoder to handle Decimal type
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    try:
        # Get the album_id from path parameters
        album_id = event.get('pathParameters', {}).get('album_id')

        if not album_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',  # Adjust as needed
                    'Access-Control-Allow-Methods': '*',  # Allows all methods
                    'Access-Control-Allow-Headers': 'Content-Type'
            },
                'body': json.dumps({'error': 'Missing album_id path parameter'})
            }

        # Query DynamoDB to get tracks for the given album_id
        response = table.scan(
            FilterExpression='album_id = :album_id',
            ExpressionAttributeValues={':album_id': album_id}
        )
        
        # Check if items are returned
        tracks = response.get('Items', [])

        if not tracks:
            return {
                'statusCode': 404,
                'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
                'body': json.dumps({'message': 'No tracks found for this album_id'})
            }
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(tracks, cls=DecimalEncoder)
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Error retrieving tracks', 'error': str(e)})
        }
