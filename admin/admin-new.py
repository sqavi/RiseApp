import json
import boto3
import uuid
from datetime import datetime

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
USER_TABLE = 'known_users'  # Replace with your DynamoDB table name
ADMIN_TABLE = 'rise_admins'  # Replace with the session DynamoDB table name


def add_user(user_mobile, user_name):
    current_time = datetime.now()
    formatted_timestamp = current_time.strftime('%Y-%m-%d:%H:%M:%S')

    table = dynamodb.Table(USER_TABLE)
    table.put_item(Item={
        'user_mobile': user_mobile,
        'user_name': user_name,
        'timestamp': formatted_timestamp,  # Store formatted timestamp as a string
    })

def remove_user(user_mobile):
    table = dynamodb.Table(USER_TABLE)
    table.delete_item(Key={
        'user_mobile': user_mobile,
    })

def list_users():
    table = dynamodb.Table(USER_TABLE)
    response = table.scan()
    return response['Items']
   
   
def lambda_handler(event, context):
    try:
        action = event['action']
        session_id = event.get('session_id')  # Assuming the session ID is provided in the request

        if action == 'add_user':
            user_mobile = event['user_mobile']
            user_name = event['user_name']
            add_user(user_mobile, user_name)
            return {
                'statusCode': 200,
                'body': json.dumps({'status': 'User added successfully'}),
            }
        elif action == 'remove_user':
            user_mobile = event['user_mobile']
            remove_user(user_mobile)
            return {
                'statusCode': 200,
                'body': json.dumps({'status': 'User removed successfully'}),
            }
        elif action == 'list_users':
            users = list_users()
            return {
                'statusCode': 200,
                'body': json.dumps({'users': users}),
            }
        else:
            return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid action'}),
               }
    except Exception as e:
        print('Error:', e)
        return {
            'statusCode': 500,
             'body': json.dumps({'error': 'An error occurred while processing the request'}),
}
