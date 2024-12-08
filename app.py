from web_socket_server import WebSocketServer, socketio, app
from flask import render_template
import json

app = WebSocketServer().create_app()
#messages = []
message_storage = {}

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(response):
    #print(f'Received message: {message}')
    #messages.append(message)
    res = json.loads(response)
    user = res['user']
    message = res['message']
    if user not in message_storage:
        message_storage[user]=[]
    message_storage[user].append(message)
    socketio.emit('message', message)

@socketio.on('get_user_messages')
def handle_get_user_messages(data):
    socketio.emit('get_user_messages', message_storage)

@app.route('/')
def index():
    return render_template('WebChatRoom.html')

if __name__ == '__main__':
    socketio.run(app)