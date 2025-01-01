import json
import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
album_table = dynamodb.Table('Album')
track_table = dynamodb.Table('Track')
artist_table = dynamodb.Table('Artist')
genre_table = dynamodb.Table('Genre')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    try:
        # Ensure queryStringParameters exists
        query_params = event.get('queryStringParameters', {})

        # Fetch and sanitize query parameters
        genre = query_params.get('genre')
        artist_name = query_params.get('artist')  # Get the artist name from the input
        album_name = query_params.get('album')    # Get the album title from the input
        track_title = query_params.get('track')   # Get the track title from the input

        # Treat 'undefined' or None as absent
        if genre == 'undefined' or genre is None:
            genre = None
        if artist_name == 'undefined' or artist_name is None:
            artist_name = None
        if album_name == 'undefined' or album_name is None:
            album_name = None
        if track_title == 'undefined' or track_title is None:
            track_title = None

        # Prepare filter expressions for albums
        filter_expressions = []

        # If artist_name is provided, query the Artist table to fetch the artist_id
        artist_id = None
        if artist_name:
            artist_response = artist_table.scan(
                FilterExpression=Attr('name').eq(artist_name)
            )
            if 'Items' in artist_response and artist_response['Items']:
                artist_id = artist_response['Items'][0].get('artist_id')
            else:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                    },
                    'body': json.dumps({'error': 'Artist not found'})
                }

        # Filter by track title if provided
        album_ids = None
        if track_title:
            track_response = track_table.scan(
                FilterExpression=Attr('title').eq(track_title)
            )
            tracks = track_response.get('Items', [])
            if not tracks:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
                    },
                    'body': json.dumps({'error': 'Track not found'})
                }

            # Collect the album_ids from matching tracks
            album_ids = [track['album_id'] for track in tracks]

            # Add filter for album_id based on track matches
            filter_expressions.append(Attr('album_id').is_in(album_ids))

        # Filter by genre if provided
        if genre:
            filter_expressions.append(Attr('genre').eq(genre))
        
        # Filter by album title if provided
        if album_name:
            filter_expressions.append(Attr('title').eq(album_name))

        # Filter albums by artist_id if found
        if artist_id:
            filter_expressions.append(Attr('artist_id').eq(artist_id))

        # Combine all filter expressions using logical AND (&)
        filter_expression = None
        if filter_expressions:
            filter_expression = filter_expressions[0]
            for expr in filter_expressions[1:]:
                filter_expression = filter_expression & expr

        # Query the Album table using the filter expression
        if filter_expression:
            response = album_table.scan(
                FilterExpression=filter_expression
            )
        else:
            response = album_table.scan()  # Return all albums if no filter is applied

        albums_with_details = []
        for album in response['Items']:
            # Fetch associated tracks for the album
            track_response = track_table.scan(
                FilterExpression=Attr('album_id').eq(album['album_id'])
            )
            tracks = track_response.get('Items', [])

            # Fetch artist details using the artist_id from the album
            artist_response = artist_table.get_item(Key={'artist_id': album.get('artist_id')})
            artist = artist_response.get('Item', {})

            # Fetch genre details for the album
            genre_response = genre_table.get_item(Key={'name': album.get('genre')})
            genre_info = genre_response.get('Item', {})

            # Append full album details including tracks and artist info
            albums_with_details.append({
                'album_id': album.get('album_id', 'Unknown'),
                'title': album.get('title', 'Unknown'),  # Album title
                'year': album.get('year', 'Unknown'),
                'tracks': tracks,
                'artist': artist.get('name', 'Unknown'),
                'band_composition': artist.get('band_composition', 'Unknown'),
                'album_art_url': album.get('album_art_url', 'Unknown'),
                'genre': genre_info.get('name', 'Unknown'),
            })

        # Return the albums along with the detailed information
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({'albums': albums_with_details}, cls=DecimalEncoder)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': json.dumps({'error': str(e)})
        }
