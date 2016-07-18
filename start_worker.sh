#!/bin/sh
celery worker -A tasks.app.celery -P eventlet --loglevel=info
