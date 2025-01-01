import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Artist')

def lambda_handler(event, context):
    try:
        # Parse incoming request body
        body = json.loads(event['body'])
        
        # Ensure artist_id is provided
        if 'artist_id' not in body:
            raise ValueError("Missing 'artist_id' in the request body")
        
        # Prepare the update expression
        update_expression = "SET #name = :name, #band_composition = :band_composition"
        expression_attribute_names = {
            "#name": "name",
            "#band_composition": "band_composition"
        }
        expression_attribute_values = {
            ":name": body['name'],
            ":band_composition": body['band_composition']
        }

        # Add image_url only if it's included in the update request
        if 'image_url' in body and body['image_url']:
            update_expression += ", #image_url = :image_url"
            expression_attribute_names["#image_url"] = "image_url"
            expression_attribute_values[":image_url"] = body['image_url']

        # Perform the update operation
        table.update_item(
            Key={'artist_id': body['artist_id']},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Artist updated successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Adjust as needed
                'Access-Control-Allow-Methods': '*',  # Allows all methods
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Error updating artist', 'error': str(e)})
        }
