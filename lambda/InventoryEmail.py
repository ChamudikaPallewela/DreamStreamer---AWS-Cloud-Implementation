import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    try:
        # Debug: Print the entire event
        print('Raw event:', event)

        # Parse the event body if it's passed as a string
        if 'body' in event:
            try:
                event = json.loads(event['body'])
                print('Parsed event:', event)
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                        'Access-Control-Allow-Headers': 'Content-Type'
                    },
                    'body': json.dumps('Invalid JSON format in request body.')
                }

        # Initialize SES client
        ses_client = boto3.client('ses', region_name='us-east-1')

        # Extract inventory data from the event
        inventory = event.get('inventory', {})
        print('Received inventory data:', inventory)

        # Handle missing or empty inventory data
        if not inventory:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps('No inventory data provided.')
            }

        # Email content
        SENDER = "dreamstreameraws@gmail.com"  # Your SES-verified email
        RECIPIENT = "lckpallewela@gmail.com"  # SES-verified recipient email
        SUBJECT = "Inventory Report - Detailed Overview"

        # Build the HTML body of the email
        body_html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    color: #333;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #fff;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background-color: #0073e6;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .content {{
                    padding: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                table, th, td {{
                    border: 1px solid #dddddd;
                    padding: 8px;
                }}
                th {{
                    background-color: #0073e6;
                    color: white;
                    text-align: left;
                }}
                td {{
                    text-align: left;
                    font-size: 14px;
                }}
                .footer {{
                    background-color: #0073e6;
                    color: white;
                    text-align: center;
                    padding: 10px;
                    font-size: 12px;
                }}
                .highlight {{
                    font-weight: bold;
                    color: #0073e6;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Inventory Report</h2>
                    <p>Overview of Tracks, Artists, Genres, and Albums</p>
                </div>
                <div class="content">
                    <h3>Inventory Summary</h3>
                    <p>Hello,</p>
                    <p>Please find below the summary of our current inventory.</p>
                    <table>
                        <thead>
                            <tr>
                                <th>Inventory Type</th>
                                <th>Count</th>
                            </tr>
                        </thead>
                        <tbody>
        """

        # Loop through the inventory and add each item as a row in the table
        for item, count in inventory.items():
            body_html += f"""
                            <tr>
                                <td>{item.capitalize()}</td>
                                <td>{count}</td>
                            </tr>
            """

        body_html += """
                        </tbody>
                    </table>
                    <p>If you have any questions or require further details, feel free to reach out to us.</p>
                    <p class="highlight">Thank you for your continued support!</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 DreamStreamer. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        print('Email body HTML:', body_html)

        # Send the email using SES
        try:
            response = ses_client.send_email(
                Source=SENDER,
                Destination={
                    'ToAddresses': [RECIPIENT]
                },
                Message={
                    'Subject': {
                        'Data': SUBJECT
                    },
                    'Body': {
                        'Html': {
                            'Data': body_html
                        }
                    }
                }
            )
            print('SES send_email response:', response)
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps('Inventory report sent successfully!')
            }
        except ClientError as e:
            print(f"Error sending email: {e.response['Error']['Message']}")
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps(f"Error sending email: {e.response['Error']['Message']}")
            }
    except Exception as e:
        print(f"Unhandled error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(f"Unhandled error occurred: {str(e)}")
        }
