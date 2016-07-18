# SocketIO Redis Testing

This Flask application is for testing flask-socketio's 2.0 release with a redis task queue.

Read about this app on my blog: [celeodor.com/flask-flask-socketio-celery-and-redis-background-task-processing](https://celeodor.com/flask-flask-socketio-celery-and-redis-background-task-processing/)

# Installation

```bash
git clone http://git.celeodor.com/Celeo/Flask-sockets-celery-redis
cd Flask-sockets-celery-redis
virtualenv env
. env/bin/activate
pip install -r requirements.txt
```

# Running

You have to run the Celery worker along with the web app.

```bash
./start_worker.sh &
python run.py
```
