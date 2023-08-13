import requests

api_base_url = 'https://zkel9v1575.execute-api.ap-southeast-1.amazonaws.com/prod'  # Replace with your API Gateway base URL
api_key = 'vrWrkSAogJ2vvdgkLjrVv632BUGswRTf8cqAuZgx'  # Replace with your actual API Key

def call_api(endpoint, data):
    headers = {
        'x-api-key': api_key
    }
    response = requests.post(f"{api_base_url}/{endpoint}", json=data, headers=headers)
    return response

#def register_user():
    user_mobile = "99999999"
    user_name = "Shahid"
    device_os = "Android"
    device_type = "Phone"

    # Add more data from the user input as needed
    data = {
        'user_mobile': user_mobile,
        'user_name': user_name,
        'device_os': device_os,
        'device_type': device_type,
        # Add other fields here based on the Lambda function's expected input
    }

    response = call_api('reg', data)
    print('Register User Response:', response.json())
    # Handle the API response here

# Implement similar functions for other API endpoints: authenticate_user, verify_otp, ask_gpt, etc.

#if __name__ == "__main__":
 #   register_user()
