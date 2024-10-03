from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
from urllib.parse import unquote

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

def get_ai_response(user_message):
    # System instructions for Gpt 
    system_instructions = {
        "role": "system",
        "content": ("Your name is broken, you were officially launched by Heis broken, "
                    "your purpose is for friendship and education. You should provide "
                    "accurate replies to user questions and not reveal your identity unless asked. "
                    "Your model is Heis v2.0.")
    }

    # Define the conversation history
    conversation = [
        system_instructions,
        {"role": "user", "content": user_message}
    ]

    try:
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=conversation
        )

        # Extract the response from ChatGPT
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/korraai', methods=['POST', 'GET'])
def chat():
    if request.method == 'POST':
        data = request.get_json()
        user_message = data.get('message')
    else:  # GET method
        user_message = request.args.get('query')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    decoded_message = unquote(user_message)
    chatgpt_response = get_ai_response(decoded_message)
    return jsonify({'response': chatgpt_response})

if __name__ == '__main__':
    # Run the Flask app on all available IP addresses and port 5000
    app.run(host='0.0.0.0', port=3000, debug=True)
