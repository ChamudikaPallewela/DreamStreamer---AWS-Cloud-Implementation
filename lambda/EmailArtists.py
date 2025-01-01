import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Debug: Print the entire event to see the raw data structure
    print('Raw event:', event)
    
    # Check if Lambda Proxy Integration is enabled (body will be a string)
    if 'body' in event:
        try:
            # Parse the body if it's a string (proxy integration)
            event = json.loads(event['body'])
            print('Parsed event:', event)
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',  # Adjust as needed
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps('Invalid JSON format in request body.')
            }
    
    # Initialize SES client
    ses_client = boto3.client('ses', region_name='us-east-1')
    
    # Extract artist data from the event
    artists = event.get('artists', [])
    
    # Log the received data
    print('Received artists data:', artists)
    
    # Handle missing or empty artist data
    if not isinstance(artists, list) or not artists:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Allow all origins, adjust as needed
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps('No artist data provided.')
        }
    
    # Email content
    SENDER = "dreamstreameraws@gmail.com"  # Your SES-verified email
    RECIPIENT = "lckpallewela@gmail.com"  # SES-verified recipient email
    SUBJECT = "Top 10 Artists Report"
    
    # Build the HTML body of the email with professional styling
    body_html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
                background-color: #f9f9f9;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 20px auto;
                background-color: #fff;
                border-radius: 8px;
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
                margin-top: 20px;
            }}
            table, th, td {{
                border: 1px solid #ddd;
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
                <h2>Top 10 Artists by Interaction</h2>
                <p>Generated Report</p>
            </div>
            <div class="content">
                <p>Hello,</p>
                <p>Below is a summary of the top 10 artists based on user interactions.</p>
                <table>
                    <thead>
                        <tr>
                            <th>Artist Name</th>
                            <th>Interactions</th>
                        </tr>
                    </thead>
                    <tbody>
    """

    # Loop through the artists and add each one as a row in the table
    for artist in artists:
        artist_name = artist.get('artist_name', 'Unknown')
        total_interactions = artist.get('total_interactions', 'N/A')
        body_html += f"""
                        <tr>
                            <td>{artist_name}</td>
                            <td>{total_interactions}</td>
                        </tr>
        """

    # Close the table and the HTML body
    body_html += """
                    </tbody>
                </table>
                <p>Thank you for reviewing this report. Should you have any questions or require further insights, feel free to reach out.</p>
                <p class="highlight">DreamStreamer Team</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 DreamStreamer. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Log the final email content
    print('Email body HTML:', body_html)
    
    # Send the email
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
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps('Email sent successfully!')
        }
    except ClientError as e:
        print(f"Error sending email: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(f"Error sending email: {e.response['Error']['Message']}")
        }
