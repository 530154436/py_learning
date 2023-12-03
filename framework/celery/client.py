#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2023/11/1 20:33
# @function:
import time

from celery_app import add_async, update_state_async

# 异步任务
print(add_async)
result = add_async.apply_async(args=[2, 8], kwargs={"double": 2})
print("result.id", result.id)
task = add_async.AsyncResult(result.id)
print("result.state", task.state)
print("result.get()", result.get())
print("result.state", task.state)


# 更新任务状态
print(update_state_async)
result = update_state_async.apply_async()
print("result.id", result.id)
task = update_state_async.AsyncResult(result.id)
for i in range(100):
    time.sleep(0.1)
    print("result.state", task.state)
print("result.get()", result.get())
print("result.state", task.state)
