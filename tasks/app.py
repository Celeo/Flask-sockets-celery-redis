from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import timedelta
from celery import Celery
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

celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
TaskBase = celery.Task


class ContextTask(TaskBase):
    abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)

celery.Task = ContextTask


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': 'Backend saw "' + message['data'] + '" from the frontend'})


if __name__ == '__main__':
    socketio.run(app, debug=True)
