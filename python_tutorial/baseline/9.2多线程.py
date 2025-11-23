# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import time, threading,multiprocessing,threadpool
import requests

'''
    多线程-python仅支持单核CPU
'''
def loop():
    print('thread %s is running ...' % threading.current_thread().name)
    n = 0
    while n < 100:
        n = n+1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        # time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

def test_loop():
    print('thread %s is running ...' % threading.current_thread().name)
    t = threading.Thread(target=loop, name='LoopThread')
    t.start()
    t.join()
    print('thread %s ended.' % threading.current_thread().name)


'''
    Lock
'''
balance = 0
lock = threading.Lock()

def change_it(n):
    # 先存后取，结果应该为0
    global balance

    # x = balance + n
    # balance = x
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(1000000):
        # 先要获取锁
        lock.acquire()
        try:
            change_it(n)
        finally:
            # 改完了一定要释放锁:
            lock.release()

def test_lock():
    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)

'''
    多核CPU
'''
def loop():
    x = 0
    while True:
        x = x ^ 1

def test_die_loop():
    for i in range(multiprocessing.cpu_count()):
        t = threading.Thread(target=loop)
        t.start()

'''
    练习
'''
def run(i):
    # requests.get(url=url)
    print(i)

def exercise():
    print('访问100次https://www.liaoxuefeng.com/需耗时长：')
    url = 'https://www.liaoxuefeng.com/'

    # 1.单进程
    start = time.time()
    [requests.get(url) for i in range(100)]
    print('单线程:', time.time() - start)

    # 2.多线程
    pool = threadpool.ThreadPool(10)
    start = time.time()
    reqes = threadpool.makeRequests(run, [url for i in range(100)])
    [pool.putRequest(x) for x in reqes]
    pool.wait()
    print('多线程:', time.time() - start)

    # 3.多进程
    p = multiprocessing.Pool(10)
    start = time.time()
    for i in range(100):
        p.apply_async(run, args=(url,))
    p.close()
    p.join()
    print('多进程:', time.time() - start)

if __name__ == '__main__':
    # test_loop()
    # test_lock()
    # test_die_loop()
    # exercise()
    pool = threadpool.ThreadPool(40)
    start = time.time()
    count = 0
    while True:
        tasks = []
        for i in range(1000):
            tasks.append(i)
        reqes = threadpool.makeRequests(run, tasks)
        [pool.putRequest(x) for x in reqes]
        count += 1
        pool.wait()
        if count==2:
            break
    print('多线程:', time.time() - start)