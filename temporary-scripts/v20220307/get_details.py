#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2022/3/7 15:55
# @function:
import math
import re
import requests

HOST = 'http://www.nasonline.org'
URL = '/member-directory/member-search-results.html?include=living&page={page}'
DETAIL_PATTERN = re.compile('<div class="information">.*?<a href="(.*?)">(.*?)</a>', re.DOTALL)
# Scompany = re.compile('<div class="information">.*?<a href="(.*?)">(.*?)</a>', re.DOTALL)

file = open('details.txt', mode='w')

pages = 3118
page_size = 50
for page, _ in enumerate(range(math.ceil(pages / page_size)), start=1):
    url = HOST + URL.format(page=page)
    rsp = requests.get(url).text
    print(page, url)
    for detail, name in DETAIL_PATTERN.findall(rsp):
        file.write(f'{name}###{detail}\n')
