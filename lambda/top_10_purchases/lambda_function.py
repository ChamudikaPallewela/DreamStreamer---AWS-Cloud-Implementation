import json
import pymysql
from decimal import Decimal

# Helper function to convert Decimal objects to float
def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

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
        # Query to get top 10 purchased tracks by purchase count, including username
        query = """
        SELECT track_id, track_name, username, COUNT(*) AS purchase_count
        FROM purchases
        GROUP BY track_id, track_name, username
        ORDER BY purchase_count DESC
        LIMIT 10;
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            top_tracks = cursor.fetchall()
        
        # Convert Decimal values to float if needed
        top_tracks = json.loads(json.dumps(top_tracks, default=decimal_to_float))
        
        # Return success response with top 10 purchased tracks data
        return {
            'statusCode': 200,
            'body': json.dumps(top_tracks),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Adjust CORS as needed
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS, GET'
            }
        }
    
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error retrieving top tracks'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Adjust CORS as needed
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS, GET'
            }
        }
    
    finally:
        connection.close()
