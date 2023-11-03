#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2023/11/1 20:33
# @function:

# 异步任务
from framework.celery.celery_app import add_async

print(add_async)
result = add_async.apply_async(args=[2, 8], kw=2)
print('hello world')
print(result.get())

# user = "test_async"
# gene_set1 = ['POMC,GCG,NPY,SST,TAC1,haia']
# gene_set2 = ['POMC,GCG,TRH,VIP,GAST,MLN,hakes']
# result = association_handler_async.apply_async(args=(user, gene_set1, gene_set2))
# print('association_handler_async')
# print(result.get())
