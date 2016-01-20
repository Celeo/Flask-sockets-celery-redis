from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask.ext.redis import FlaskRedis
from datetime import timedelta
from threading import Thread
import time
from tasks.shared import db, app_settings

import eventlet
eventlet.monkey_patch()


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
for k, v in app.config.items():
    app_settings[k] = v
app.permanent_session_lifetime = timedelta(days=14)
db.app = app
db.init_app(app)
socketio = SocketIO(app, async_mode='eventlet')
redis_store = FlaskRedis(app)
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
        time.sleep(1)
        count += 1
        print('Clock tick')
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


if __name__ == '__main__':
    socketio.run(app, debug=True)
