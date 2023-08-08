//being used to make API call.
const axios = require("axios");

//must be sent with each API request
const config = {
  headers: {
    "x-api-key": "sec_ZkEDxEah6e6Ay8FTPh1QS2uMCIZwFEj4",
    "Content-Type": "application/json",
  },
};

//current PDF source.
const source = "src_8MjmU3awoIyakJUrZIOm1";

//define the asynchronous function to make the API call
async function sendMessageToChatPDF(question) {
  const url = 'https://api.chatpdf.com/v1/chats/message';

  let data = {
    sourceId: source,
    //must include context later.
    messages: [
      {
        role: 'user',
        content: question,
      }
    ],
  };

  try {
    const response = await axios.post(url, data, config);
    console.log('Result:', response.data.content);
    return response.data.content;
  } catch (error) {
    console.error('Error:', error.message);
    console.log('Response:', error.response.data);
    throw error;
  }
}

exports.handler = async (event, context) => {
  try {
    const question = event.queryStringParameters.question; // Adjust based on your event structure
    const response = await sendMessageToChatPDF(question);

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
