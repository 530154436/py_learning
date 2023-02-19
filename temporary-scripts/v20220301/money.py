#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2022/03/01
@function:
"""
import re
import requests

headers = {

}

NAME = re.compile('<span class="name">(.*?)\n')
MEMBER_TYPE = re.compile("<span class='badge memberType member '>(.*?)</span>")
JOB_TITLE_BORDER = re.compile('<span class="jobTitle border">(.*?)</span>')
ORGANIZATION_BORDER = re.compile('<span class="organization border">(.*?)</span>')
ADDRESS = re.compile('<div class="address">(.*?)</div>')
ELECTION_YEAR = re.compile('<label>Election Year.*?<span>(.*?)</span>')
PRIMARY_SECTION = re.compile('<label>Primary Section.*?<span>(.*?)</span>')
ELECTION_CITATION = re.compile('Election Citation.*?<div class="description">(.*?)</div>')

data =[]
with open('details.txt', mode='r') as f:
    for index, line in enumerate(f):
        if not line:
            continue
        name, url = line.strip().split('###')
        print(index, name, url)
        html = requests.get(url).text
        print(html)

        name = NAME.findall(html)
        member_type = MEMBER_TYPE.findall(html)
        job_title_border = JOB_TITLE_BORDER.findall(html)
        organization_border = ORGANIZATION_BORDER.findall(html)
        address = ADDRESS.findall(html)
        election_year = ELECTION_YEAR.findall(html)
        primary_section = PRIMARY_SECTION.findall(html)
        election_citation = ELECTION_CITATION.findall(html)



        data.append({
            'name': name,
            'member_type': member_type,
            'job_title_border': job_title_border,
            'organization_border': organization_border,
            'address': address,
            'election_year': election_year,
            'primary_section': primary_section,
            'election_citation': election_citation,
        })

        break