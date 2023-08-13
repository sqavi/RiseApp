import boto3
import json
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = 'authentication_table'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Parse input JSON
     
        auth_token = event['auth_token']
        user_mobile = event['user_mobile']
        
        # Query DynamoDB for the item with the given mobile number
        response = table.get_item(Key={'user_mobile': user_mobile})
        item = response.get('Item')
        
        # Check if the item exists in DynamoDB
        if item is not None:
            stored_token = item.get('auth_token')
            token_status = item.get('token_status')
            
            # Compare the stored token and validate it
            if stored_token == auth_token and token_status == 'valid':
                # Token is valid, return success
                return {
                    'statusCode': 200,
                    'body': json.dumps({'status': 'success'})
                }
            else:
                # Token is invalid or token_status is not valid, return error
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Invalid auth_token or token expired'})
                }
        else:
            # Item not found in DynamoDB, return error
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Mobile number not found'})
            }
    except Exception as e:
        # Handle any exceptions and return error
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
