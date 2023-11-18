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


# 异步任务
print(update_state_async)
result = update_state_async.apply_async()
print("result.id", result.id)
task = update_state_async.AsyncResult(result.id)
for i in range(100):
    time.sleep(1)
    print("result.state", task.state)
print("result.get()", result.get())
print("result.state", task.state)


# from celery_app import report_controller_creat_async
# _selectedRows = [
#     {
#         'gene_symbols': 'POMC,GCG,NPY,SST,TAC1',
#         'id': 422,
#         'name': 'Cholestasis, Benign Recurrent Intrahepatic, 2',
#         'no_of_genes': 5,
#         'group': 'A'
#     },
#     {
#         'gene_symbols': 'POMC,GCG,TRH,VIP,GAST,MLN',
#         'id': 298,
#         'name': '风湿关节痿软疼痛',
#         'no_of_genes': 6,
#         'group': 'B'
#     }
# ]
# _param = {"user_id": "test", "selectedRows": _selectedRows, "randomNum": 10}
# task = report_controller_creat_async.apply_async(kwargs=_param)
# print(task.id)
# result = report_controller_creat_async.AsyncResult(task.id)
# print("result.state", result.state)
# print("result.get()", result.get())
