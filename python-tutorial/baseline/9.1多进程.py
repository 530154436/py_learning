#!/usr/bin/env python3
# -*- coding : utf-8 -*-

import os,time,random
from multiprocessing import Process,Queue
from multiprocessing import Pool
import subprocess

print('Process %s starting ...' % os.getpid())

# Only works on Unix/Linux/Mac:

# pid = os.fork() #执行了一遍，返回两次
# if pid == 0:
#     print('I am a child process %s and my parent is %s' % (os.getpid(), os.getppid()))
# else:
#     print('I (%s) just created a child process (%s)' % (os.getpid(), pid))


'''
    multiThread
'''
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

def test_multi_thread():
    print('Parent process %s ' % os.getpid())
    p = Process(target=run_proc, args=('test',))

    print('Child process will start.')

    # 开始进程
    p.start()

    # join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步。
    p.join()

    print('Child process end.')


'''
    Pool
'''
def long_time_task(name):
    print('Run task %s (%s) ...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

def test_multi_pool():
    print('Parent process %s ' % os.getpid())
    # cpu 核数
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')

    # 调用join()之前必须先调用close()
    p.close()

    # join()方法会等待所有子进程执行完毕
    p.join()
    print('All subprocesses done.')


'''
    子进程
'''
def test_subprocess():
    print('$ nslookup www.python.org')
    r = subprocess.call(['nslookup', 'www.python.org'])
    print('Exit code:', r)

    print('$ nslookup')
    p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
    print(output.decode('utf-8'))
    print('Exit code:', p.returncode)


'''
    进程间通信
'''
# 写数据进程执行的代码:
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue ...' % value)
        q.put(value)
        time.sleep(random.random())

# 读数据进程执行的代码:
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

def test_communicate():
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start()
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()

if __name__ == '__main__':
    # test_multi_thread()
    # test_multi_pool()
    # test_subprocess()
    test_communicate()














