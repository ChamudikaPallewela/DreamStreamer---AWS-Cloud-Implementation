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
        purchase_date = body['date']  # Date of purchase
        click_count = body.get('clickCount', 1)  # Default click count to 1 if not provided
        
        # Get current timestamp
        purchase_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        # Ensure the table exists, create it if it doesn't
        create_table_query = """
        CREATE TABLE IF NOT EXISTS purchases (
            track_id VARCHAR(255),
            track_name VARCHAR(255),
            username VARCHAR(255),
            purchase_date DATETIME,
            click_count INT DEFAULT 1,
            PRIMARY KEY (track_id, username, purchase_date)
        );
        """
        
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)

        # Insert or update the purchase record
        insert_or_update_query = """
        INSERT INTO purchases (track_id, track_name, username, purchase_date, click_count)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE click_count = click_count + %s;
        """
        
        with connection.cursor() as cursor:
            cursor.execute(insert_or_update_query, (track_id, track_name, username, purchase_date, click_count, click_count))
        
        connection.commit()

        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Purchase logged successfully'}),
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
            'body': json.dumps({'message': 'Error logging purchase'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Allow all origins; adjust as needed
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS, GET, POST'
            }
        }
    
    finally:
        connection.close()
