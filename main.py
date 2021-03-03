from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)



#@socketio.on('connect')
#def connect_message(data):
    #username = session.get('username')

@socketio.on('message')
def handle_message(data):
    username = session.get('username')
    print(f'message: {data["data"]}')
    emit('message', {'data': f"[{username}]: {data['data']}"}, broadcast=True)

@app.route('/')
def index():
    username = None
    if session.get('username'):
        username = session.get('username')
    return render_template('index.html', username=username)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        session['username'] = username
    return redirect('/')


@app.route('/logout', methods=['GET'])
def logout():
    session['username'] = None
    return redirect('/')

#if __name__ == '__main__':
    #app.run(debug=True)

if __name__ == '__main__':
    socketio.run(app, host='192.168.0.24', port=8080)