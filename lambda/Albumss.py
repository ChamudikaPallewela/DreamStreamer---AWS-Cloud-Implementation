import json
import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Extract the genre from the query parameters
    genre_name = event.get('queryStringParameters', {}).get('genre')
    
    if not genre_name:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins, adjust as needed
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Missing genre parameter'})
        }
    
    # Scan DynamoDB for albums with the specified genre
    try:
        response = dynamodb.scan(
            TableName='Album',  # Table name
            FilterExpression='genre = :genre',
            ExpressionAttributeValues={
                ':genre': {'S': genre_name}
            }
        )
        
        # Return the results
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins, adjust as needed
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(response['Items'])
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins, adjust as needed
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Internal server error'})
        }
