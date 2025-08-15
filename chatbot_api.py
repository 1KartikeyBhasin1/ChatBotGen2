import os
from flask import Flask, request, jsonify, send_from_directory
from mychatbot import Me
from flask_cors import CORS
from flask import render_template

# Get the absolute path of the directory where the script is located
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Define the path to the assets directory
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

app = Flask(__name__)
CORS(app)
me = Me()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(ASSETS_DIR, filename)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    history = data.get('history', [])
    # Convert history to the format expected by me.chat
    formatted_history = []
    for turn in history:
        if turn.get('role') and turn.get('content'):
            formatted_history.append({'role': turn['role'], 'content': turn['content']})
    response = me.chat(message, formatted_history)
    return jsonify({'reply': response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
