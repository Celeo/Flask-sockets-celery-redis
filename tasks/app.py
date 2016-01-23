from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import timedelta
from celery import Celery
import time
from tasks.shared import app_settings

import eventlet
eventlet.monkey_patch()


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
for k, v in app.config.items():
    app_settings[k] = v
app.permanent_session_lifetime = timedelta(days=14)

socketio = SocketIO(app, async_mode='eventlet', message_queue=app.config['SOCKETIO_REDIS_URL'])

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task()
def background_task(url):
    local_socketio = SocketIO(message_queue=url)
    local_socketio.emit('my response', {'data': 'background task starting ...'}, namespace='/test')
    time.sleep(10)
    local_socketio.emit('my response', {'data': 'background task complete!'}, namespace='/test')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bg')
def start_background_thread():
    print('Starting background celery task thread call ...')
    print(background_task.delay(app.config['SOCKETIO_REDIS_URL']))
    return 'Started'


@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': 'Backend saw "' + message['data'] + '" from the frontend'})
