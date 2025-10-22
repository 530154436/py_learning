# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import queue, time, random
from multiprocessing.managers import BaseManager

'''
    task_master
'''
# 发送任务的队列:
task_queue = queue.Queue()

# def get_task_queue():
#     return  task_queue

# 接收结果的队列:
result_queue = queue.Queue()

# def get_result_queue():
#     return result_queue

# 从BaseManager继承的QueueManager:
class QueueManger(BaseManager):
    pass


# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManger.register('get_task_queue', callable=lambda : task_queue)
QueueManger.register('get_result_queue', callable=lambda : result_queue)

# 绑定端口5000, 设置验证码'abc':
manager = QueueManger(address=('', 5000), authkey=b'abc')

# 启动Queue:
manager.start()

# 获得通过网络访问的Queue对象:
task = manager.get_task_queue()
result = manager.get_result_queue()

# 放几个任务进去:
for i in range(10):
    n = random.randint(0,10000)
    print('Put task %d ...' % n)
    task.put(n)

# 从result队列读取结果:
print('Try get results ...')
for i in range(10):
    r = result.get(timeout = 20)
    print('Result: %s' % r)

# 关闭:
manager.shutdown()
print('master exit.')

