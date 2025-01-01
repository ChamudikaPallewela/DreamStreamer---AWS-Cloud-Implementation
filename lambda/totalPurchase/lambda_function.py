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
        
        # Query to get track_id, track_name, and purchase_date for all purchases
        purchases_query = """
        SELECT track_id, track_name, purchase_date
        FROM purchases
        ORDER BY purchase_date DESC;
        """
        
        # Query to calculate the total number of purchases
        total_revenue_query = """
        SELECT COUNT(*) as total_purchases
        FROM purchases;
        """
        
        with connection.cursor() as cursor:
            # Execute purchase query
            cursor.execute(purchases_query)
            all_purchases = cursor.fetchall()
            
            # Execute total revenue query
            cursor.execute(total_revenue_query)
            total_purchases_result = cursor.fetchone()
            total_revenue = total_purchases_result['total_purchases'] * 1  # Each purchase is $1
            
        # Log the retrieved data
        print(f"Retrieved purchases: {all_purchases}")
        print(f"Total revenue: {total_revenue}")
        
        # Convert datetime to string if needed
        all_purchases = json.loads(json.dumps(all_purchases, default=lambda o: datetime_to_str(o) if isinstance(o, (datetime, Decimal)) else str(o)))
        
        # Return success response with purchases and total revenue
        return {
            'statusCode': 200,
            'body': json.dumps({
                'total_revenue': total_revenue,
                'purchases': all_purchases
            }),
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
            'body': json.dumps({'message': f'Error retrieving purchases: {e}'}),
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
