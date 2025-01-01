import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Album')

# Custom JSON encoder to handle Decimal type
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    try:
        # Scan the Album table to get all albums
        response = table.scan()
        albums = response.get('Items', [])
        
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
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'Error retrieving albums', 'error': str(e)})
        }
