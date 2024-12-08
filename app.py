from web_socket_server import WebSocketServer, socketio, app
from flask import render_template, request, jsonify
import json

app = WebSocketServer().create_app()

message_storage = {}

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    print(data)
    user = data.get('username')
    message = data.get('message')
    
    if not user or not message:
        return  
    
    if user not in message_storage:
        message_storage[user] = []
    message_storage[user].append(message)
    
    print(f"Message from {user}: {message}")
    
    socketio.emit('message', {'username': user, 'message': message})


@socketio.on('get_user_messages')
def handle_get_user_messages(data):
    user = data.get('user')
    user_messages = message_storage.get(user, [])
    socketio.emit('get_user_messages', {'user': user, 'messages': user_messages})


@app.route('/')
def index():
    return render_template('WebChatRoom.html')

if __name__ == '__main__':
    socketio.run(app)