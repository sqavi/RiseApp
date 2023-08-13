import json
import boto3
import random
import string
import time
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb')
# Function to cretae token
def generate_token(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def lambda_handler(event, context):
    try:
        
        # Extract user_mobile and OTP from the request
        user_mobile = event['user_mobile']
        entered_otp = event['otp']
        if not user_mobile or not entered_otp:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'user_mobile and otp are required'})
            }

        # Verify OTP against DynamoDB
        response = dynamodb.get_item(
            TableName='RiseApp_registration', 
            Key={'user_mobile': {'S': user_mobile}}
        )
        dynamodb_otp = response.get('Item', {}).get('otp', {}).get('S')

        if entered_otp != dynamodb_otp:
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'OTP verification failed'})
            }

        # Generate a 16-digit alphanumeric token
        auth_token = generate_token(16)

        # Get user details from the first table
        user_details = response.get('Item', {})
        user_name = user_details.get('user_name', {}).get('S', '')
        device_os = user_details.get('device_os', {}).get('S', '')
        device_type = user_details.get('device_type', {}).get('S', '')

        # Calculate token expiry 30 days from now
        expiry_date = (datetime.utcnow() + timedelta(days=30)).isoformat()
        
        # Get the current timestamp
        request_time = int(time.time()) 
        
        #Set token Status valid 
        token_status = "valid"
        # Create item to save in second DynamoDB table
        item = {
            'auth_token': {'S': auth_token},
            'user_mobile': {'S': user_mobile},
            'user_name': {'S': user_name},
            'device_os': {'S': device_os},
            'device_type': {'S': device_type},
            'request_time': {'N': str(request_time)},
            'token_expiry': {'S': expiry_date},
            'token_status' : {'S': token_status}
        }

        # Save token-related data to second DynamoDB table
        dynamodb.put_item(
            TableName='authentication_table',  
            Item=item
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Token created successfully', 'auth_token': auth_token})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'DynamoDB ClientError: {str(e)}'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
