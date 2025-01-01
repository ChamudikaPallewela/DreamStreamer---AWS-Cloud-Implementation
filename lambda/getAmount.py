import json
import boto3

# Initialize DynamoDB resources
dynamodb = boto3.resource('dynamodb')

# Tables
track_table = dynamodb.Table('Track')
artist_table = dynamodb.Table('Artist')
genre_table = dynamodb.Table('Genre')
album_table = dynamodb.Table('Album')

def lambda_handler(event, context):
    try:
        # Scan each table and get the item count
        track_count = track_table.scan(Select='COUNT')['Count']
        artist_count = artist_table.scan(Select='COUNT')['Count']
        genre_count = genre_table.scan(Select='COUNT')['Count']
        album_count = album_table.scan(Select='COUNT')['Count']

        # Create a response object
        response = {
            'tracks': track_count,
            'artists': artist_count,
            'genres': genre_count,
            'albums': album_count
        }

        # Return the counts with status 200
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Counts retrieved successfully', 'data': response})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Error retrieving counts', 'error': str(e)})
        }
