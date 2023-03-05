#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/05/23
@function:
"""
import pandas as pd
import re
import pkuseg


SPLIT_PATTERN = re.compile('(\([0-9]+\))')

pd.set_option('display.width', 1000)  # 设置打印宽度
# pd.set_option('max_colwidth', 800)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


seg = pkuseg.pkuseg(postag=True)
def _split(x):
    _list = SPLIT_PATTERN.split(x)
    _list = [ i for i in _list if i ]
    for i in _list:
        print(seg.cut(i))
    return _list

# df = pd.read_excel('领域汇总-提取.xlsx')
df = pd.read_excel('领域汇总-提取.samples.xlsx')
s = df['Author affiliation'].apply(lambda x: _split(x))
# print(df.columns)

print(s)
s.to_excel('aa.xlsx')