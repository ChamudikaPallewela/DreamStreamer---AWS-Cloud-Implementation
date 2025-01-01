import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Artist')

def lambda_handler(event, context):
    try:
        # Check if httpMethod is present (usually for API Gateway requests)
        if 'httpMethod' in event and event['httpMethod'] != 'GET':
            return {
                'statusCode': 405,
                'headers': {
                    'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',  # Allowed HTTP methods
                    'Access-Control-Allow-Headers': 'Content-Type'  # Allowed headers
                },
                'body': json.dumps({'message': 'Method Not Allowed'})
            }

        # Fetch all artist records from DynamoDB
        response = table.scan()
        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',  # Allowed HTTP methods
                'Access-Control-Allow-Headers': 'Content-Type'  # Allowed headers
            },
            'body': json.dumps({'Items': items})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',  # Allowed HTTP methods
                'Access-Control-Allow-Headers': 'Content-Type'  # Allowed headers
            },
            'body': json.dumps({'message': 'Error fetching artists', 'error': str(e)})
        }
