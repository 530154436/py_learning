# /usr/bin/env python3
# -*- coding:utf-8 -*-
import asyncio
import time
import threading

def test1():
    async def hello():
        print('Hello World!')
        r = await asyncio.sleep(5)
        print('Hello again!')
    # 获取EventLoop:
    loop = asyncio.get_event_loop()
    # 执行coroutine
    loop.run_until_complete(hello())
    loop.close()

async def wget(host):
    print('wget {} ...'.format(host))
    connect = asyncio.open_connection(host, 80)
    reader, writer = await connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    await writer.drain()
    while True:
        line = await reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
        # Ignore the body, close the socket
    writer.close()

def test2():
    loop = asyncio.get_event_loop()
    tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

async def waiting():
    print('waiting')
    # await asyncio.sleep(5)
    time.sleep(3)
    print('done')

def test3():
    start = time.time()
    loop = asyncio.get_event_loop()
    tasks = [waiting() for i in range(5)]
    loop.run_until_complete(asyncio.wait(tasks))
    print(time.time() - start)

if __name__ == '__main__':
    # test1()
    # test2()
    test3()


