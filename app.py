from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
from urllib.parse import unquote

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

#  OpenAI API key here
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

def get_ai_response(user_message):
    #  system instructions for ChatGPT
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
    return response.choices[0].message['content']

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    if request.method == 'POST':
        data = request.get_json()
        user_message = data.get('message')
    else:  # GET method
        user_message = request.args.get('query')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    chatgpt_response = get_ai_response(user_message)
    return jsonify({'response': chatgpt_response})

@app.route('/api', methods=['GET'])
def api_query():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    decoded_query = unquote(query)
    ai_response = get_ai_response(decoded_query)
    return ai_response

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

if __name__ == '__main__':
    # Run the Flask app on all available IP addresses and port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
