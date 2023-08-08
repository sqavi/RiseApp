const apiBaseUrl = 'https://zkel9v1575.execute-api.ap-southeast-1.amazonaws.com/prod/reg'; // Replace with your API Gateway base URL

function callApi(endpoint, apiKey, requestData) {
  return axios.post(`${apiBaseUrl}/${endpoint}`, requestData, {
    headers: {
      'x-api-key': apiKey
    }
  });
}

function registerUser() {
  const apiKey = document.getElementById('api-key').value;
  const userMobile = document.getElementById('user-mobile').value;
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

