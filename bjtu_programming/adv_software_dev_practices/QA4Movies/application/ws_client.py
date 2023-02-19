#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/08/29
@function:
"""
from websocket import create_connection

def send_query_webSocket():
    ws = create_connection("ws://127.0.0.1:5000/chat")
    result = ws.recv()  # 接收服务端发送的连接成功消息
    print('socket', result)
    ws.send("周润发演了什么电影")
    result = ws.recv()
    print(result)
    ws.close()


if __name__ == '__main__':
    send_query_webSocket()