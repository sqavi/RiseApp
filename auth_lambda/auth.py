import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Extract token from query string parameters
        query_params = event.get('queryStringParameters')
        token = query_params.get('token')
        if not token:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Token is required in query string'})
            }

        # Check if the token exists as an S3 object
        object_key = f'{token}.txt'
        try:
            s3.head_object(Bucket='your-bucket-name', Key=object_key)
        except s3.exceptions.NoSuchKey:
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Token does not exist. Please register again.'})
            }

        # Retrieve the token's expiry date from the S3 object's metadata
        response = s3.get_object(Bucket='your-bucket-name', Key=object_key)
        expiry_date = response['Metadata'].get('expiry_date')

        # Compare token's expiry date with the current date
        current_time = datetime.utcnow().isoformat()
        if expiry_date and current_time > expiry_date:
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Token has expired. Please register again.'})
            }

        # If token exists and is valid, return status code 200 to continue
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Token is valid. Continue.'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
