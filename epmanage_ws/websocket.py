"""
websocket.py : Websocket namespaces

This file is part of EPControl.

Copyright (C) 2016  Jean-Baptiste Galet & Timothe Aeberhardt

EPControl is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

EPControl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with EPControl.  If not, see <http://www.gnu.org/licenses/>.
"""
import os

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask import request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room
from werkzeug.utils import import_string

import epmanage_ws.settings as settings
from epmanage_ws.auth import check_token


class PyShellNamespace(Namespace):
    def on_connect(self):
        token = check_token(request.headers.get('Authorization'), audience='agent')
        if token and token.get('sub'):
            logging.info("Agent %s connected", token['sub'])
            join_room(token['sub'])

    def on_disconnect(self):
        logging.info("ws:disconnect")

    def on_join(self, data):
        token = check_token(request.headers.get('Authorization'), audience='shell')
        if token:
            logging.debug("ws:join %s", data)
            join_room(data)

    def on_leave(self, data):
        logging.debug("ws:leave %s", data)
        leave_room(data)

    def on_cmd_req(self, data):
        token = check_token(request.headers.get('Authorization'), audience='shell')
        if token:
            logging.debug("ws:cmd_req %s", data)
            room = data.pop('room', None)
            emit('cmd', data, room=room)

    def on_cmd_rsp(self, data):
        token = check_token(request.headers.get('Authorization'), audience='agent')
        if token and token.get('sub'):
            logging.info("ws:cmd_rsp %s", data)
            emit('rsp', data, room=token['sub'])

app = Flask(__name__)
conf_module = os.environ.get('EPMANAGE_CONFIG_MODULE')
if not conf_module:
    conf_module = 'epmanage_ws.settings.Config'
obj = import_string(conf_module)()
app.config = obj
settings.config = obj

logging.basicConfig(
    format="[%(asctime)s] {%(name)s} %(levelname)s - %(message)s",
    handlers=[RotatingFileHandler(app.config.LOGFILE, maxBytes=1000000, backupCount=1)],
    level=logging.DEBUG)

socketio = SocketIO(app)
socketio.on_namespace(PyShellNamespace('/shell'))
