import json
import pymysql

# Establish connection to RDS
def get_rds_connection():
    return pymysql.connect(
        host='chamudika.c5640o6qobbt.us-east-1.rds.amazonaws.com',
        user='admin',
        password='chamudika',
        db='chamudika',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def lambda_handler(event, context):
    connection = get_rds_connection()
    
    try:
        # Extract username from the path parameters
        username = event['pathParameters']['username']

        # Query to get album interactions for the provided username
        select_query = """
        SELECT album_id
        FROM album_interactions
        WHERE username = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(select_query, (username,))
            result = cursor.fetchall()

        # Collect the album IDs
        album_ids = [row['album_id'] for row in result]

        if album_ids:
            # Return the list of album_ids
            return {
                'statusCode': 200,
                'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins, adjust as needed
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
                'body': json.dumps({
                    'message': f'Albums for user {username} retrieved successfully',
                    'album_ids': album_ids
                })
            }
        else:
            return {
                'statusCode': 404,
                'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins, adjust as needed
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
                'body': json.dumps({
                    'message': f'No albums found for user {username}'
                })
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins, adjust as needed
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'message': 'Error retrieving album interactions',
                'error': str(e)
            })
        }
    
    finally:
        connection.close()
