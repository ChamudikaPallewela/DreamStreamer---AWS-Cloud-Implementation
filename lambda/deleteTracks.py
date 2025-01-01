import json
import boto3

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
TABLE_NAME = 'Track'
BUCKET_NAME = 'chamuawsfile'

def lambda_handler(event, context):
    try:
        # Extract track_id from the URL path parameters
        track_id = event['pathParameters']['track_id']
        table = dynamodb.Table(TABLE_NAME)

        # Fetch the track details first
        response = table.get_item(Key={'track_id': track_id})
        track = response.get('Item')

        if not track:
            return {
                'statusCode': 404,
                'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
                'body': json.dumps({'message': 'Track not found'})
            }

        # Delete the track from DynamoDB
        table.delete_item(Key={'track_id': track_id})

        # Delete the image from S3 (if available)
        if 'ImageUrl' in track:
            image_key = track['ImageUrl'].split('/')[-1]  # Extract file name from URL
            s3.delete_object(Bucket=BUCKET_NAME, Key=image_key)

        # Delete the MP3 files from S3 (if available)
        if 'Mp3Url' in track and isinstance(track['Mp3Url'], list):
            for mp3_url in track['Mp3Url']:
                mp3_key = mp3_url.split('/')[-1]  # Extract file name from URL
                s3.delete_object(Bucket=BUCKET_NAME, Key=mp3_key)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Track deleted successfully'})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
