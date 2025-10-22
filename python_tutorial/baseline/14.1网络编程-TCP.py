#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import threading
import time

def testTcp():
    # 创建一个socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 建立连接:
    s.connect(('www.sina.com.cn', 80))

    # 发送数据:
    s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')

    # 接收数据:
    buffer = []
    while True:
        # 调用recv(max)方法，一次最多接收指定的字节数
        d = s.recv(1024)
        if d:
            buffer.append(d)
        else:
            break
    data = b''.join(buffer)
    print(data)

    # 关闭连接:
    s.close()

    header,html = data.split(b'\r\n\r\n', 1)
    print(header.decode('utf-8'))
    print(html.decode('utf-8')[:200])

def tcpLink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome.')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8')=='exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 监听端口:
    s.bind(('127.0.0.1',9999))

    # 调用listen()方法开始监听端口，传入的参数指定等待连接的最大数量：
    s.listen(5)
    print('Waiting for connection...')

    while True:
        # 接受一个新连接:
        sock, addr = s.accept()

        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=tcpLink, args=(sock, addr))
        t.start()

def client():
    # 创建一个socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 9999))
    print(s.recv(1024).decode('utf-8'))
    for data in [b'Edward', b'John']:
        s.send(data)
        print(s.recv(1024).decode('utf-8'))
    s.send(b'exit')
    s.close()

if __name__ == '__main__':
    # testTcp()
    # server()
    client()