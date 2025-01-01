import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_album = dynamodb.Table('Album')
table_tracks = dynamodb.Table('Track')

def lambda_handler(event, context):
    try:
        if 'body' not in event:
            raise ValueError("Missing 'body' in the event")
        
        body = json.loads(event['body'])
        album_id = body.get('album_id')

        if not album_id:
            raise ValueError("Missing 'album_id'")

        # Check if there are any tracks associated with the album
        response = table_tracks.scan(
            FilterExpression="album_id = :album_id",
            ExpressionAttributeValues={":album_id": album_id}
        )

        tracks = response.get('Items', [])

        # If tracks are found, do not delete the album
        if tracks:
            return {
                'statusCode': 400,
                'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
                'body': json.dumps({
                    'message': f"Cannot delete album with ID '{album_id}' because it has associated tracks.",
                    'track_count': len(tracks)
                })
            }

        # No tracks found, delete the album
        table_album.delete_item(Key={'album_id': album_id})

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': f"Album with ID '{album_id}' deleted successfully"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Error deleting album', 'error': str(e)})
        }
