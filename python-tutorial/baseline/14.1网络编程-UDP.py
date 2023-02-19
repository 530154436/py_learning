#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

def server():
    # SOCK_DGRAM指定了这个Socket的类型是UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定端口:
    s.bind(('127.0.0.1', 9999))

    print('Bind UDP on 9999...')
    while True:
        # recvfrom() 方法返回数据和客户端的地址与端口
        data,addr = s.recvfrom(1024)
        print('Received from %s:%s.' % (addr, data))
        s.sendto(b'Hello, %s!' % data, addr)

def client():
    # SOCK_DGRAM指定了这个Socket的类型是UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for data in [b'Edward', b'Jason']:
        s.sendto(data, ('127.0.0.1', 9999))
        print(s.recv(1024).decode('utf-8'))
    s.close()

if __name__ == '__main__':
    # server()
    client()