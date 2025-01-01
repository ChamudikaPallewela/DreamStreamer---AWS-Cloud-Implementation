import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Track')

# Helper function to handle Decimal serialization
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # or int(obj) if you don't need floating points
    raise TypeError

def lambda_handler(event, context):
    try:
        # Scan the entire table to get all tracks
        response = table.scan()
        tracks = response.get('Items', [])

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(tracks, default=decimal_default)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Error fetching tracks', 'error': str(e)})
        }
