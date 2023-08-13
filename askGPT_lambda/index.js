const AWS = require('aws-sdk');
const ssm = new AWS.SSM();
const axios = require("axios");

const getApiKey = async () => {
  try {
    const response = await ssm.getParameter({ Name: 'gptkey', WithDecryption: true }).promise();
    return response.Parameter.Value;
  } catch (error) {
    throw error;
  }
};

// Usage example
let generateHeaders = async function(){
  let apiKey = await getApiKey()
  const config = {
    headers: {
      "x-api-key": apiKey,
      "Content-Type": "application/json",
    },
  };
  return config;
}

const sourceId = "src_8MjmU3awoIyakJUrZIOm1"; // Replace with your desired sourceId

async function sendMessageToChatPDF(data, config) {
  const url = 'https://api.chatpdf.com/v1/chats/message';

  try {
    const response = await axios.post(url, data, config);
    console.log('Result:', response.data.content);
    return response.data.content;
  } catch (error) {
    console.error('Error:', error.message);
    throw error; // Rethrow the error to be caught in the handler
  }
}

exports.handler = async (event, context) => {
  try {
    // Construct the inputData object in the format you need
    const inputData = {
      sourceId: sourceId, // Use sourceId (camel case) here
      messages: event.messages,
    };
    const config = await generateHeaders();

    const response = await sendMessageToChatPDF(inputData, config);
    return {
      statusCode: 200,
      body: JSON.stringify({ response }),
    };
  
  } catch (error) {
    console.error('Error:', error.message);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'An error occurred while processing the request' }),
    };
  }
};
