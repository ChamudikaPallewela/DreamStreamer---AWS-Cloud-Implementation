import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_artist = dynamodb.Table('Artist')
table_album = dynamodb.Table('Album')

def lambda_handler(event, context):
    try:
        if 'body' not in event:
            raise ValueError("Missing 'body' in the event")
        
        body = json.loads(event['body'])
        artist_id = body.get('artist_id')

        if not artist_id:
            raise ValueError("Missing 'artist_id'")

        # Check if there are any albums associated with the artist
        response = table_album.scan(
            FilterExpression="artist_id = :artist_id",
            ExpressionAttributeValues={":artist_id": artist_id}
        )

        albums = response.get('Items', [])

        # If albums are found, do not delete the artist
        if albums:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',  # Adjust as needed
                    'Access-Control-Allow-Methods': '*',  # Allows all methods
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({
                    'message': f"Cannot delete artist with ID '{artist_id}' because it has associated albums.",
                    'album_count': len(albums)
                })
            }

        # No albums found, delete the artist
        table_artist.delete_item(Key={'artist_id': artist_id})

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': f"Artist with ID '{artist_id}' deleted successfully"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Error deleting artist', 'error': str(e)})
        }
