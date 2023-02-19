#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@function: 生成用户字典
"""
import data_loader
from config import DATA_DIR

movie = data_loader.load_movie()
person = data_loader.load_person()

words = {}
for i in movie['title'].tolist():
    if i not in words:
        words[i] = [1, 'movie']
    else:
        words[i][0] += 1

for i in person['name'].tolist():
    if i not in words:
        words[i] = [1, 'person']
    else:
        words[i][0] += 1

with open(DATA_DIR.joinpath('userdict.txt'), mode='w') as f:
    for k,v in words.items():
        f.write(f'{k} {v[0]} {v[1]}')
        f.write('\n')
