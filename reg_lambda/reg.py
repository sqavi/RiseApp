import json
import boto3
import random
import time
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb')

def generate_otp():
    return str(random.randint(10000, 99999))

def lambda_handler(event, context):
    try:
        # Parse request body
        user_mobile = event['user_mobile']
        if not user_mobile:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'user_mobile is required'})
            }
        device_os = event['device_os']
        device_type = event['device_type']
        user_name = event['user_name']
        #device_ip = event['ip']

        data = {
            'user_mobile': user_mobile,
            'device_os': device_os,
            'device_type': device_type,
            'user_name': user_name
        }
        # Generate a random 5-digit OTP
        otp = generate_otp()

        # Get the current timestamp
        req_time = int(time.time()) 

        # Create item to save in DynamoDB
        item = {
            'user_mobile': {'S': user_mobile},
            'user_name': {'S': user_name},
            'device_os': {'S': device_os},
            'device_type': {'S': device_type},
            #'device_ip': {'S': device_ip},
            'otp': {'S': otp},
            'req_time': {'N': str(req_time)}
        }

        # Save data to DynamoDB
        dynamodb.put_item(
            TableName='RiseApp_registration',
            Item=item
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Data saved successfully', 'otp': otp})
        }
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'JSON parsing error: {str(e)}'})
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
