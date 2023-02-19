#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/08/28
@function:
"""
import traceback
import json
import qa_processor
from gevent import pywsgi
from flask_sockets import Sockets
from flask import Flask
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
sockets = Sockets(app)

# ------------------------------------------------------------------------
# WebSocket接口
# http://127.0.0.1:5000/chat
# ------------------------------------------------------------------------


@sockets.route('/chat')
def chat(ws):
    ws.send(json.dumps({'message': "Hello, I'm Siri"}))
    while not ws.closed:
        msg = ws.receive()
        print(f'server ws received:{msg}')
        if msg:
            answer = qa_processor.run(msg)
            print(type(answer), answer)
            ws.send(json.dumps({'message': answer}))


if __name__ == '__main__':

    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

    print('Server start: WebSocket[5000]')