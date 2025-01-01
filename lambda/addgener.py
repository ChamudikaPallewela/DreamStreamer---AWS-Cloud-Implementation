import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Genre')  # Ensure the table name is correct

def lambda_handler(event, context):
    try:
        if 'body' not in event:
            raise ValueError("Missing 'body' in the event")
        
        body = json.loads(event['body'])
        
        # Check that the Partition Key 'name' is present
        if 'name' not in body:
            raise ValueError("Missing 'name' in the request body")
        
        # Save genre details to DynamoDB
        response = table.put_item(
            Item={
                'name': body['name'],  # Partition Key
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins, adjust as needed
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(body['name'])
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Error retrieving genres', 'error': str(e)})
        }
