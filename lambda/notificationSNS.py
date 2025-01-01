import json
import boto3

# Initialize the SNS client
sns = boto3.client('sns')

# Replace with your SNS Topic ARN
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:157070555729:notification'

def lambda_handler(event, context):
    try:
        # Get the email from the query string parameters in the event
        user_email = event['queryStringParameters']['email']
        
        # Subscribe the user's email to the SNS topic
        sns.subscribe(
            TopicArn=SNS_TOPIC_ARN,
            Protocol='email',
            Endpoint=user_email
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'User subscribed to SNS topic successfully'})
        }
    except KeyError:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Email is missing from query string parameters'})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Error subscribing user', 'error': str(e)})
        }
