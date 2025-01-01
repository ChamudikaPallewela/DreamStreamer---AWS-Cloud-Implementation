import json
import pymysql
from decimal import Decimal
from datetime import datetime

# Helper function to convert Decimal objects to float
def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

# Helper function to convert datetime objects to ISO format strings
def datetime_to_str(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError

def lambda_handler(event, context):
    connection = None  # Initialize connection variable
    try:
        # Log the entire event for debugging
        print(f"Received event: {json.dumps(event)}")
        
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
        
        # Establish connection to RDS
        connection = pymysql.connect(
            host='chamudika.c5640o6qobbt.us-east-1.rds.amazonaws.com',
            user='admin',
            password='chamudika',
            db='chamudika',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        # Log connection success
        print("Database connection established.")
        
        # Query to get track_id, track_name, and purchase_date for a specific user
        query = """
        SELECT track_id, track_name, purchase_date
        FROM purchases
        WHERE username = %s
        ORDER BY purchase_date DESC;
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, (username,))
            user_purchases = cursor.fetchall()
        
        # Log the retrieved purchases
        print(f"Retrieved purchases: {user_purchases}")
        
        # Convert Decimal values to float and datetime to string if needed
        user_purchases = json.loads(json.dumps(user_purchases, default=lambda o: datetime_to_str(o) if isinstance(o, (datetime, Decimal)) else str(o)))
        
        # Return success response with user's purchases data
        return {
            'statusCode': 200,
            'body': json.dumps(user_purchases),
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
            'body': json.dumps({'message': f'Error retrieving user purchases: {e}'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS, GET'
            }
        }
    
    finally:
        if connection:
            connection.close()
