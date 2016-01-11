from flask import Flask, render_template
from flask_socketio import emit
from datetime import timedelta
from tasks.shared import db, socketio, app_settings


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
for k, v in app.config.items():
    app_settings[k] = v
app.permanent_session_lifetime = timedelta(days=14)
db.app = app
db.init_app(app)
socketio.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': 'Backend saw "' + message['data'] + '" from the frontend'})
