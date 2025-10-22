# !/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
[TOC]
Tqdm 是一个快速，可扩展的Python`进度条`，可以在 Python 长循环中添加一个进度提示信息，用户只需要封装任意的`迭代器` tqdm(iterator)。

+ 安装
```
python3 -m pip install tqdm -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
```
'''

import time
import pandas as pd
import numpy as np
from tqdm import tqdm,trange

# 1）基于迭代器的方法
for i in tqdm(range(10)):
    time.sleep(0.2)

for j in trange(10):
    time.sleep(0.2)

# 2) 手动控制
# 对于实例之外的循环允许对tqdm（）手动控制
pbar = tqdm(["a", "b", "c", "d"])
for char in pbar:
    time.sleep(0.2)
    pbar.set_description("processing %s" % char)

total = 10
with tqdm(total=total) as pbar:
    for k in range(total):
        time.sleep(0.2)
        pbar.update()

# 3) pandas支持
# DataFrame.progress_apply和DataFrameGroupBy.progress_apply
df = pd.DataFrame(np.random.randint(0, 100, (5000, 6)))
tqdm.pandas(desc='My Bar')

a = df.groupby(0).progress_apply(lambda x: x**2)
b = df.progress_apply(lambda x:x**2, axis=1)
print(df.head())
print(a.head())
print(b.head())