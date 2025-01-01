import json
import boto3
from decimal import Decimal
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Album')

# Custom JSON encoder to handle Decimal type
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    try:
        # Parse incoming request body
        body = json.loads(event['body'])
        
        # Check if album ID is provided, throw an error if missing during an update
        if 'album_id' not in body:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': 'album_id is required for updating an album.'})
            }
        
        # Extract album_id and other data from the request body
        album_id = body['album_id']

        # Prepare the update expression
        update_expression = "SET #title = :title, #genre = :genre, #year = :year, #artist_id = :artist_id, #album_art_url = :album_art_url"

        expression_attribute_names = {
            "#title": "title",
            "#genre": "genre",
            "#year": "year",  # 'year' is a reserved word
            "#artist_id": "artist_id",
            "#album_art_url": "album_art_url"
        }

        expression_attribute_values = {
            ":title": body['title'],
            ":genre": body['genre'],
            ":year": int(body['year']),
            ":artist_id": body['artist_id'],
            ":album_art_url": body['album_art_url']
        }
        
        # Use a conditional expression to ensure that the album exists
        table.update_item(
            Key={'album_id': album_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ConditionExpression="attribute_exists(album_id)"  # Ensure the album exists
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, PUT',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'Album updated successfully', 'album_id': album_id})
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'Error updating album', 'error': str(e)})
        }
