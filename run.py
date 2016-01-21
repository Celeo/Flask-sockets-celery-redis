#!/usr/bin/env python

from tasks import app, socketio

socketio.run(app, debug=True)
