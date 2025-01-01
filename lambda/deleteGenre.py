import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_genres = dynamodb.Table('Genre')   # Table name for genres
table_albums = dynamodb.Table('Album')  # Table name for albums

def lambda_handler(event, context):
    try:
        # Check if the body is present in the request
        if 'body' not in event:
            raise ValueError("Missing 'body' in the event")
        
        body = json.loads(event['body'])
        
        # Extract genre name or ID from the body
        genre_name = body.get('name')
        
        if not genre_name:
            raise ValueError("Missing 'name' in the request body")

        # Step 1: Check if any albums are associated with the genre
        response = table_albums.scan(
            FilterExpression="genre = :genre_name",
            ExpressionAttributeValues={":genre_name": genre_name}
        )

        albums = response.get('Items', [])

        # Step 2: If albums are found, block the deletion and return an error message
        if albums:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,DELETE',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({
                    'message': f"Cannot delete genre '{genre_name}' as it has associated albums.",
                    'album_count': len(albums)
                })
            }

        # Step 3: If no albums are found, proceed to delete the genre
        table_genres.delete_item(
            Key={'name': genre_name}  # Assuming 'name' is the primary key
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,DELETE',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'message': f"Genre '{genre_name}' deleted successfully"
            })
        }

    except Exception as e:
        # Return a 500 error for unexpected errors
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,DELETE',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'message': 'Error deleting genre',
                'error': str(e)
            })
        }
