# /usr/bin/env python3
# -*- coding:utf-8 -*-
import asyncio
import threading

def test1():
    @asyncio.coroutine
    def hello():
        print('Hello World!')
        # 异步调用asyncio.sleep(1):
        r = yield from asyncio.sleep(5)
        print('Hello again!')

    # 获取EventLoop:
    loop = asyncio.get_event_loop()
    # 执行coroutine
    loop.run_until_complete(hello())
    loop.close()

def test2():
    @asyncio.coroutine
    def hello():
        print('Hello World! (%s)' % threading.current_thread().name)
        # 异步调用asyncio.sleep(1):
        r = yield from asyncio.sleep(5)
        print('Hello again! (%s)' % threading.current_thread().name)

    # # 获取EventLoop:
    loop = asyncio.get_event_loop()
    tasks = [hello(), hello()]
    # 由打印的当前线程名称可以看出，两个coroutine是由同一个线程并发执行的
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

def test3():
    @asyncio.coroutine
    def wget(host):
        # 异步网络连接来获取sina、sohu和163的网站首页
        print('wget %s...' % host)
        connect = asyncio.open_connection(host, 80)
        reader, writer = yield from connect
        header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
        writer.write(header.encode('utf-8'))
        yield from writer.drain()
        while True:
            line = yield from reader.readline()
            if line == b'\r\n':
                break
            print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
            # Ignore the body, close the socket
        writer.close()

    loop = asyncio.get_event_loop()
    tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
#http://python.jobbole.com/88427/
#https://www.python.org/dev/peps/pep-0492/
# https://aiohttp.readthedocs.io/en/stable/client.html#aiohttp-client-websockets
if __name__ == '__main__':
    # test1()
    # test2()
    test3()