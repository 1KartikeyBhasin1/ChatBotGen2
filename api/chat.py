from flask import Flask, request, jsonify
import sys
import os

# Add the parent directory to the path so we can import mychatbot
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mychatbot import Me

app = Flask(__name__)
me = Me()

def handler(request):
    if request.method == 'POST':
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
    
    return jsonify({'error': 'Method not allowed'}), 405