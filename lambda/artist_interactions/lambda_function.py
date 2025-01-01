import json
import pymysql
from datetime import datetime

# Define the Lambda handler
def lambda_handler(event, context):
    # Establish connection to RDS
    connection = pymysql.connect(host='chamudika.c5640o6qobbt.us-east-1.rds.amazonaws.com',
                                 user='admin',
                                 password='chamudika',
                                 db='chamudika',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    try:
        # Parse the request body
        body = json.loads(event['body'])
        artist_id = body['artistId']
        artist_name = body['artistName']  # Add artistName to request body
        username = body['username']
        count = body.get('count', 1)  # Default count to 1 if not provided
        
        # Get current timestamp
        interaction_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        # Ensure the table exists, create it if it doesn't
        create_table_query = """
        CREATE TABLE IF NOT EXISTS artist_interactions (
            artist_id VARCHAR(255),
            artist_name VARCHAR(255),
            username VARCHAR(255),
            interaction_time DATETIME,
            interaction_count INT DEFAULT 1,
            PRIMARY KEY (artist_id, username)
        );
        """
        
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)

        # Insert or update the artist interaction
        insert_or_update_query = """
        INSERT INTO artist_interactions (artist_id, artist_name, username, interaction_time, interaction_count)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE interaction_count = interaction_count + 1, interaction_time = %s;
        """
        
        with connection.cursor() as cursor:
            cursor.execute(insert_or_update_query, (artist_id, artist_name, username, interaction_time, count, interaction_time))
        
        connection.commit()

        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Interaction logged successfully'})
        }
    
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Error logging interaction'})
        }
    
    finally:
        connection.close()
