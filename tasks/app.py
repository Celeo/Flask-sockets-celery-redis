from flask import Flask, render_template
from flask_socketio import emit
from datetime import timedelta
from threading import Thread
from time import sleep
from tasks.shared import db, socketio, app_settings


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
for k, v in app.config.items():
    app_settings[k] = v
app.permanent_session_lifetime = timedelta(days=14)
db.app = app
db.init_app(app)
socketio.init_app(app)
thread = None


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_task)
        thread.daemon = True
        thread.start()
    return render_template('index.html')


@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': 'Backend saw "' + message['data'] + '" from the frontend'})


def background_task():
    count = 0
    while True:
        print('Clock tick')
        socketio.emit('my response', {'data': 'Clock tick %d' % count}, namespace='/test')
        count += 1
        sleep(10)
