from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/chat', methods=['GET'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    # Define the system instructions for ChatGPT
    system_instructions = {
        "role": "system",
        "content": "Your name is broken, you were officially launched by Heis broken, your purpose is for friendship and Education. You should provide Accurate reply to user question, don't say your identity unless you were asked . Your model is Heis v2.0."
    }

    # Define the conversation history
    conversation = [
        system_instructions,
        {"role": "user", "content": user_message}
    ]

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=conversation
    )

    # Extract the response from ChatGPT
    chatgpt_response = response.choices[0].message['content']

    return jsonify({'response': chatgpt_response})

if __name__ == '__main__':
    # Run the Flask app on all available IP addresses and port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
