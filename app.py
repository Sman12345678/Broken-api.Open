from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = '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'

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    # Define the system instructions for ChatGPT
    system_instructions = {
        "role": "system",
        "content": "Your name is broken, you were officially launched by Heis broken, your purpose is for friendship and Education. You should provide Accurate reply to user question, don't say your identity unless you were asked."
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
    app.run(debug=True)
