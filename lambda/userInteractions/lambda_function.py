import json
import pymysql
from datetime import datetime, timedelta

# Define the Lambda handler
def lambda_handler(event, context):
    connection = pymysql.connect(
        host='chamudika.c5640o6qobbt.us-east-1.rds.amazonaws.com',
        user='admin',
        password='chamudika',
        db='chamudika',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        # Get the username from the event (assuming it's passed in the query string parameters)
        username = event.get('queryStringParameters', {}).get('username')
        
        if not username:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Username is required'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'OPTIONS, GET'
                }
            }
        
        # Get current date and the date 7 days ago
        today = datetime.utcnow()
        week_ago = today - timedelta(days=7)
        
        # Initialize the result dictionary
        user_stats = {
            'most_listened_album': None,
            'most_listened_album_id': None,
            'most_listened_track': None,
            'most_listened_artist': None,
            'most_listened_artist_id': None
        }

        # Query for the most listened album in the last 7 days
        album_query = """
        SELECT album_id, album_name, SUM(interaction_count) AS total_interactions
        FROM album_interactions 
        WHERE username = %s AND interaction_time BETWEEN %s AND %s
        GROUP BY album_id, album_name
        ORDER BY total_interactions DESC 
        LIMIT 1;
        """
        with connection.cursor() as cursor:
            cursor.execute(album_query, (username, week_ago.strftime('%Y-%m-%d %H:%M:%S'), today.strftime('%Y-%m-%d %H:%M:%S')))
            result = cursor.fetchone()
            if result:
                user_stats['most_listened_album'] = result['album_name']
                user_stats['most_listened_album_id'] = result['album_id']

        # Query for the most listened track in the last 7 days
        track_query = """
        SELECT track_name, SUM(interaction_count) AS total_interactions
        FROM track_interactions 
        WHERE username = %s AND interaction_time BETWEEN %s AND %s
        GROUP BY track_name
        ORDER BY total_interactions DESC 
        LIMIT 1;
        """
        with connection.cursor() as cursor:
            cursor.execute(track_query, (username, week_ago.strftime('%Y-%m-%d %H:%M:%S'), today.strftime('%Y-%m-%d %H:%M:%S')))
            result = cursor.fetchone()
            if result:
                user_stats['most_listened_track'] = result['track_name']

        # Query for the most listened artist in the last 7 days
        artist_query = """
        SELECT artist_id, artist_name, SUM(interaction_count) AS total_interactions
        FROM artist_interactions 
        WHERE username = %s AND interaction_time BETWEEN %s AND %s
        GROUP BY artist_id, artist_name
        ORDER BY total_interactions DESC 
        LIMIT 1;
        """
        with connection.cursor() as cursor:
            cursor.execute(artist_query, (username, week_ago.strftime('%Y-%m-%d %H:%M:%S'), today.strftime('%Y-%m-%d %H:%M:%S')))
            result = cursor.fetchone()
            if result:
                user_stats['most_listened_artist'] = result['artist_name']
                user_stats['most_listened_artist_id'] = result['artist_id']

        # Return success response with user's listening stats
        return {
            'statusCode': 200,
            'body': json.dumps(user_stats),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS, GET'
            }
        }

    except pymysql.MySQLError as e:
        print(f"Database Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Database Error: {e}'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS, GET'
            }
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error retrieving user data: {e}'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS, GET'
            }
        }
    
    finally:
        connection.close()
