const apiBaseUrl = 'https://zkel9v1575.execute-api.ap-southeast-1.amazonaws.com/prod/reg'; // Replace with your API Gateway base URL
apiKey = 'vrWrkSAogJ2vvdgkLjrVv632BUGswRTf8cqAuZgx'; // Replace with your API Key
userName = 'Shahid Qavi';
deviceOs = 'android';
deviceId = 'test';
userMobile = '9999999999';



// Helper function to call the API Gateway endpoint with the provided API Key and data.
// Returns a Promise that resolves to the response data.
// See https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-set-up-simple-proxy.html#api-gateway-simple-proxy-for-lambda-input-format
// for the expected input format.
// See https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-response-json-format.html
// for the expected response format.
// See https://docs.aws.amazon.com/lambda/latest/dg/nodejs-prog-model-handler.html for the expected handler input format.
function callApi(endpoint, apiKey, requestData) {
  return axios.post(`${apiBaseUrl}/${endpoint}`, requestData, {
    headers: {
      'x-api-key': apiKey
    }
  });
}

//function registerUser() {
 // const apiKey = document.getElementById('api-key').value;
 // const userMobile = document.getElementById('user-mobile').value;
  // Add more data from the frontend form as needed
  const requestData = {
    user_mobile: userMobile,
    user_name: userName,
    device_os: deviceOs,
    device_id: deviceId,
    // Add other fields here based on the Lambda function's expected input
  };

  callApi('reg', apiKey, requestData)
    .then(response => {
      console.log('Register User Response:', response.data);
      // Handle the API response here
    })
    .catch(error => {
      console.error('Error calling Register User API:', error);
      // Handle the error here
    });
}

// Implement similar functions for other API endpoints: authenticateUser, verifyOTP, askGPT, etc.

