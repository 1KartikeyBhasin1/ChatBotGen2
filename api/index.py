from flask import Flask, request, jsonify, send_from_directory
from mychatbot import Me
from flask_cors import CORS
import os

# Get the absolute path of the directory where the script is located
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# Define the path to the assets directory
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
CORS(app)
me = Me()

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(ASSETS_DIR, filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)

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

# Vercel serverless function handler
def handler(request, context):
    return app(request, context)

# For local development
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
