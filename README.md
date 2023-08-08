"# RiseApp" 
"# RiseApp" 

reg_lambda function recieved request from Mobile for regstration. It creates an OTP token and save information in DynamoDB Table. 
verify_lambda function verify the OTP and generates the authentication token which is used to authenticate app. Token information is saved in DynamoDB
auth_lamda recieves the token and verifies if token is valid 
token_expire will expire the token and update dynamodb table
clear_otp will delete the expired otp from DynamoDB table
RiseApp.py is CDK script to deploy the app and lambda functions
