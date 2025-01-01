import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Artist')

def lambda_handler(event, context):
    try:
        # Scan the Artist table to get all artists
        response = table.scan()
        artists = response.get('Items', [])
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed for specific domains
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(artists)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed for specific domains
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'message': 'Error retrieving artists', 'error': str(e)})
        }
