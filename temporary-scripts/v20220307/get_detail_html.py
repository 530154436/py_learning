#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2022/03/01
@function:
"""
import os
import requests

if not os.path.exists('htmls'):
    os.mkdir('htmls')

errors = []
with open('details.txt', mode='r') as f:
    for index, line in enumerate(f, start=1):
        try:
            if not line:
                continue

            name, url = line.strip().split('###')
            _id = url.split('/')[-1]
            print(index, name, _id, url)

            with open(f'htmls/{_id}', mode='w', encoding='utf8') as html_file:
                html = requests.get(url).text
                html_file.write(html)
        except Exception as err:
            errors.append((name, url))
            print('====>', err, index, name, url)

err_file = open('errors.txt', mode='w')
for name, url in errors:
    err_file.write(f'{name}###{url}\n')
