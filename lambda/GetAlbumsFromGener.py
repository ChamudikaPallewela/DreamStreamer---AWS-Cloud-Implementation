import json
import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

# Initialize DynamoDB resources
dynamodb = boto3.resource('dynamodb')
album_table = dynamodb.Table('Album')
track_table = dynamodb.Table('Track')
artist_table = dynamodb.Table('Artist')

# Custom JSON encoder to handle Decimal objects
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    try:
        # Get the album_ids from the request body
        body = json.loads(event['body'])
        album_ids = body.get('album_ids', [])

        if not album_ids:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'error': 'album_ids parameter is required'})
            }

        genres = set()
        albums_with_details = []

        # Fetch genre details for each album_id
        for album_id in album_ids:
            album_response = album_table.get_item(Key={'album_id': album_id})
            album = album_response.get('Item', {})

            if album:
                genres.add(album.get('genre'))

        # Fetch all albums in the same genres, excluding the provided album_ids
        for genre in genres:
            genre_response = album_table.scan(
                FilterExpression=Attr('genre').eq(genre)
            )
            same_genre_albums = genre_response.get('Items', [])

            for album in same_genre_albums:
                if album['album_id'] in album_ids:
                    continue  # Skip the album if it's one of the provided album_ids

                # Fetch associated tracks for the album
                track_response = track_table.scan(
                    FilterExpression=Attr('album_id').eq(album['album_id'])
                )
                tracks = track_response.get('Items', [])

                # Fetch artist details for the album
                artist_response = artist_table.get_item(Key={'artist_id': album.get('artist_id')})
                artist = artist_response.get('Item', {})

                # Append album details including the album_id
                albums_with_details.append({
                    'album_id': album.get('album_id'),  # Include the album_id in the response
                    'title': album.get('title', 'Unknown'),
                    'year': album.get('year', 'Unknown'),
                    'tracks': tracks,
                    'artist': artist.get('name', 'Unknown'),
                    'band_composition': artist.get('band_composition', 'Unknown'),
                    'album_art_url': album.get('album_art_url', 'Unknown'),
                    'genre': album.get('genre', 'Unknown'),
                })

        # Return the albums with detailed information
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'albums': albums_with_details}, cls=DecimalEncoder)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
        }
