import json
import pymysql
from datetime import datetime

# Define the Lambda handler
def lambda_handler(event, context):
    # Establish connection to RDS
    connection = pymysql.connect(
        host='chamudika.c5640o6qobbt.us-east-1.rds.amazonaws.com',
        user='admin',
        password='chamudika',
        db='chamudika',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        # Parse the request body
        body = json.loads(event['body'])
        track_id = body['trackId']  # Track ID
        track_name = body['trackName']  # Track Name
        username = body['username']  # Username
        count = body.get('count', 1)  # Default count to 1 if not provided
        
        # Get current timestamp
        interaction_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        # Ensure the table exists, create it if it doesn't
        create_table_query = """
        CREATE TABLE IF NOT EXISTS track_interactions (
            track_id VARCHAR(255),
            track_name VARCHAR(255),
            username VARCHAR(255),
            interaction_time DATETIME,
            interaction_count INT DEFAULT 1,
            PRIMARY KEY (track_id, username)
        );
        """
        
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)

        # Insert or update the track interaction
        insert_or_update_query = """
        INSERT INTO track_interactions (track_id, track_name, username, interaction_time, interaction_count)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE interaction_count = interaction_count + 1, interaction_time = %s;
        """
        
        with connection.cursor() as cursor:
            cursor.execute(insert_or_update_query, (track_id, track_name, username, interaction_time, count, interaction_time))
        
        connection.commit()

        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Track interaction logged successfully'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Allow all origins; adjust as needed
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS, GET, POST'
            }
        }
    
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error logging track interaction'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Allow all origins; adjust as needed
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS, GET, POST'
            }
        }
    
    finally:
        connection.close()
