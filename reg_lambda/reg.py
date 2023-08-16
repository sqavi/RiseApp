import json
import boto3
import random
import time
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb')
ses = boto3.client('ses')

def generate_otp():
    return str(random.randint(10000, 99999))

#   def send_email(email, otp):
#    # Replace 'YOUR_FROM_EMAIL' with the email address you want to send from
#    from_email = 'shahidqavi@gmail.com'
#    subject = 'RISE: Your OTP for User Registration'
#    message = f'Your OTP for registration is: {otp}. Please Note that this OTP is valid for 30 minutes. Complete your registration process by veryfying your account with OTP'
#    
#    try:
#        response = ses.send_email(
#            Source=from_email,
#           Destination={'ToAddresses': [email]},
#            Message={
#                'Subject': {'Data': subject},
#                'Body': {'Text': {'Data': message}}
#            }
#        )
#        print("Email sent:", response)
#    except ClientError as e:
#        print("Error sending email:", e)
#
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
        
        # Try to retrieve user_email, set it to None if not present
        try:
            user_email = event['user_email']
        except KeyError:
            user_email = "None"
       
         # Add user_email to item if it's not None
        if user_email != "None":
            item['user_email'] = {'S': user_email} 
       
        data = {
            'user_mobile': user_mobile,
            'device_os': device_os,
            'device_type': device_type,
            'user_name': user_name,
            'user_email': user_email
        }
        # Generate a random 5-digit OTP
        otp = generate_otp()

        # Get the current timestamp
        req_time = int(time.time()) 

        # Create item to save in DynamoDB
        item = {
            'user_mobile': {'S': user_mobile},
            'user_name': {'S': user_name},
            'user_email': {'S': user_email},
            'device_os': {'S': device_os},
            'device_type': {'S': device_type},
            'otp': {'S': otp},
            'req_time': {'N': str(req_time)}
        }

        # Save data to DynamoDB
        dynamodb.put_item(
            TableName='RiseApp_registration',
            Item=item
        )
        
        # Send OTP email using SES
        if user_email != "None":
            ses.send_email(
                Source='shahidqavi@gmail.com',
                Destination={
                    'ToAddresses': [user_email]
                },
                Message={
                    'Subject': {
                        'Data': 'RISE Chat: Your OTP Code'
                    },
                    'Body': {
                        'Text': {
                            'Data': f'Your OTP code is: {otp}. Please note that this code is valid for 30 minutes only. Please verify OTP and complete your registration process'
                        }
                    }
                }
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
