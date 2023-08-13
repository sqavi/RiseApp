import json
import boto3
from datetime import datetime

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'known_users'  # Replace with your DynamoDB table name
SESSION_TABLE_NAME = 'rise_admins'  # Replace with the session DynamoDB table name

def is_authorized(session_id):
    try:
        session_table = dynamodb.Table(SESSION_TABLE_NAME)
        response = session_table.get_item(Key={'session_id': session_id})
        if 'Item' in response:
            return True  # The session ID exists in the table, authorized
        else:
            return False  # The session ID was not found in the table, unauthorized
    except Exception as e:
        print('Authorization Error:', e)
        return False  # An error occurred, unauthorized for safety

def authenticate_user(login_id, password):
    try:
        # Your authentication logic here
        # This is a simple example, you should implement a more secure authentication mechanism
        ssession_table = dynamodb.Table(SESSION_TABLE_NAME)
        stored_loginID = session_table.get_item(Key={'loginID': loginID}) 
        stored_password = session_table.get_item(Key={'password': password})
        if login_id == 'stored_loginID' and password == 'stored_password':
            # Generate a unique session ID
            session_id = str(uuid.uuid4())
            
            # Store the session ID in the DynamoDB table
            session_table = dynamodb.Table(SESSION_TABLE_NAME)
            session_table.put_item(Item={
                'session_id': session_id,
                'timestamp': datetime.now().strftime('%Y-%m-%d:%H:%M:%S'),
            })
            return session_id
        else:
            return None
    except Exception as e:
        print('Authentication Error:', e)
        return None

def add_user(user_mobile, user_name):
    current_time = datetime.now()
    formatted_timestamp = current_time.strftime('%Y-%m-%d:%H:%M:%S')
    
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item={
        'user_mobile': user_mobile,
        'user_name': user_name,
        'timestamp': formatted_timestamp,  # Store formatted timestamp as a string
    })
    
def remove_user(user_mobile):
    table = dynamodb.Table(TABLE_NAME)
    table.delete_item(Key={
        'user_mobile': user_mobile,
    })

def list_users():
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    return response['Items']

def lambda_handler(event, context):
    try:
        
        action = event['action']
        session_id = event['session_id']  # Assuming the session ID is provided in the request
        #stored_session_id = is_authorized(session_id)
        
        if action == 'auth_admin':
            login_id = event['login_id']
            password = event['password']
            session_id = authenticate_user(login_id, password)
            if session_id:
                return {
                    'statusCode': 200,
                    'body': json.dumps({'session_id': session_id}),
                }
            else:
                return {
                    'statusCode': 401,
                    'body': json.dumps({'error': 'Authentication failed'}),
                }
        else:
     
            # Check if the user is authorized
            if is_authorized(session_id) == 'False':
                print('Unauthorized access for session ID:', session_id)
                return {
                    'statusCode': 403,
                    'body': json.dumps({'error': 'Unauthorized', 'session_id': session_id}),
                }
        
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