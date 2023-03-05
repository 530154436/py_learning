#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/05/23
@function:
"""
import pandas as pd
import re

ORDER_PATTERN = re.compile('\([0-9]+\)')
SEPARATOR_PATTERN = re.compile('[,，\s]+')    # 标点空格

pd.set_option('display.width', 1000)  # 设置打印宽度
# pd.set_option('max_colwidth', 800)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

max_len = 0
def _split(x):
    global max_len

    # 按 “(数字)” 分割
    _list = [i for i in ORDER_PATTERN.split(x) if i]
    _ord = [i for i in ORDER_PATTERN.findall(x) if i ]
    if len(_ord)!=len(_list):
        raise Exception(f'啥情况 len(_ord)!=len(_list), _list={_list}')
    _res = []
    for i in range(len(_list)):
        _res.append(_ord[i]+_list[i])

    # 处理国家
    countries = []
    for i in _res:
        s = SEPARATOR_PATTERN.split(i)
        s = [j for j in s if j]
        countries.append(s[-1])
    _res.append(';'.join(countries))

    # 国家去重
    kv = {}
    for i in countries:
        if i not in kv:
            kv[i] = 0
        kv[i] += 1
    kv_sorted = sorted(kv.items(), key=lambda x:x[1], reverse=True)
    kv_sorted = [f'{k}:{v}' for k,v in kv_sorted]
    _res.append(';'.join(kv_sorted))

    # 国家INST总数
    _res.append(str(len(countries)))

    # 去重国家总数
    _res.append(str(len(kv_sorted)))

    max_len = max_len if max_len>=len(_res) else len(_res)
    # print(_res)

    return _res

def _pending(x):
    if len(x)==max_len:
        return x

    countries = x[-4]
    kv = x[-3]
    total_inst = x[-2]
    total_coun = x[-1]
    x = x[:-4]
    x.extend((max_len-len(x)-4)*[''])
    x.append(countries)
    x.append(kv)
    x.append(total_inst)
    x.append(total_coun)
    return x

df = pd.read_excel('领域汇总-提取.xlsx')
# df = pd.read_excel('领域汇总-提取.samples.xlsx')
df['Author affiliation'] = df['Author affiliation'].apply(lambda x: _split(x))
df['Author affiliation'] = df['Author affiliation'].apply(lambda x: _pending(x))
df1 = df['Author affiliation'].apply(pd.Series,
                                     index=['col_%s'%(i+1) for i in range(max_len-4)]+['countries', 'count',
                                                                                       'total_inst', 'total_coun'])

print(df1.columns)
df1.to_excel('all.xlsx')