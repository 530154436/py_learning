# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import threading

class Student:
    def __init__(self,name):
        self.name = name
'''
    global dic
'''

global_dic = {}

def test_global_dic():
    t1 = threading.Thread(target=std_thread, args=('Alice',), name='Thread-1')
    t2 = threading.Thread(target=std_thread, args=('Edward',), name='Thread-2')
    t1.start()
    t2.start()
    t1.join()
    t2.join()

def std_thread(name):
    std = Student(name)
    # 把std放到全局变量global_dict中：
    global_dic[threading.current_thread()] = std
    do_task_1()
    do_task_2()

def do_task_1():
    # 不传入std，而是根据当前线程查找：
    std = global_dic[threading.current_thread()]
    print(std.name, threading.current_thread().name, 'has done task 1')

def do_task_2():
    # 任何函数都可以查找出当前线程的std变量：
    std = global_dic[threading.current_thread()]
    print(std.name, threading.current_thread().name, 'has done task 2')

'''
    thread local
'''
# 创建全局ThreadLocal对象:
local_school = threading.local()

def process_student():
    # 获取当前线程关联的student:
    std = local_school.student
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))

def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name
    process_student()

def test_thread_local():
    t1 = threading.Thread(target=process_thread, args=('Alice',), name='Thread-1')
    t2 = threading.Thread(target=process_thread, args=('Edward',), name='Thread-2')
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    # test_global_dic()
    test_thread_local()









