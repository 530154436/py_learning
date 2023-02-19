#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import os
import pandas

Sname = re.compile('<div id="contact_info">.*?<h2>(.*?)</h2>', re.DOTALL)
Scompany = re.compile('<div id="contact_info">.*?<h3>(.*?)</h3>', re.DOTALL)
Ssecondray = re.compile('Secondary Section:.*?</span>(.*?)<br />', re.DOTALL)
Sprimary = re.compile('Primary Section:.*?</span>(.*?)<br />', re.DOTALL)
Smembership_type = re.compile('<meta name="member_membertype" content=?"(.*?)"', re.DOTALL)
Smembership_year = re.compile('<div id="membership-type".*?\(.*?([0-9]+)\)', re.DOTALL)
Smember_country = re.compile('<meta name="member_country" content=?"(.*?)"', re.DOTALL)
Sbiosketch = re.compile('<div id="biosketch">.*?<p>(.*?)</p>', re.DOTALL)
Sresearch_interests = re.compile('<div id="research_interests">.*?<p>(.*?)</p>', re.DOTALL)

# 相关链接
Related_Links = re.compile('<div id="related_links">(.*?)</div>', re.DOTALL)
Related_Links_detail = re.compile('<a href="(.*?)".*?>(.*?)</a>', re.DOTALL)


def extract_links(string: str) -> tuple:
    results = ''.join(Related_Links.findall(string))
    text, links = [], []
    for link, txt in Related_Links_detail.findall(results):
        text.append(txt)
        links.append(link)
    return '\r'.join(text), '\r'.join(links)


def extract_text(pattern: re.Pattern, string: str) -> str:
    results = pattern.findall(string, re.S)
    if results:
        result: str = results[0]
        ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
        result: str = ILLEGAL_CHARACTERS_RE.sub(r'', result)
        return result.lstrip().rstrip()
    return ''


data = []
for i, path in enumerate(os.listdir('htmls'), start=1):
    if not path.endswith('html'):
        continue

    with open('htmls/' + path, encoding='UTF-8') as f:
        html = ''.join(f.readlines())
        url = 'http://www.nasonline.org/member-directory/members/' + path

    try:
        # 姓名
        name = extract_text(Sname, html)
        print(i, path, name)

        # 国籍
        country = extract_text(Smember_country, html)

        # 单位（没有放出来）
        # company = extract_text(Scompany, html)
        company = ""

        # 入选类型、年份
        membership_type = extract_text(Smembership_type, html)
        membership_year = extract_text(Smembership_year, html)

        # 入选研究领域
        secondray = extract_text(Ssecondray, html)
        primary = extract_text(Sprimary, html)

        # 个人简介
        biosketch = extract_text(Sbiosketch, html)

        # 研究兴趣
        research_interests = extract_text(Sresearch_interests, html)

        # 相关链接
        related_links = extract_links(html)
        related_texts = extract_links(html)

        outputdata = {
            '姓名': name,
            '国籍': country,
            '单位': company,
            '入选类型': membership_type,
            '入选年份': membership_year,
            '入选研究领域（Primary Section）': primary,
            '入选研究领域（Secondray Section）': secondray,
            '个人简介（Biosketch）': biosketch,
            '研究兴趣（Research Interests）': research_interests,
            '相关链接文本（Related Links)': related_links[0],
            '相关链接地址（Related Links)': related_links[1],
            'Url': url
         }

        data.append(outputdata)

    except Exception as err:
        print('====>', err, path)

with pandas.ExcelWriter('美国科学院院士情况20220719.xlsx') as writer:
    data = pandas.DataFrame(data)
    data = data.sort_values(by=['入选年份', '姓名'], ascending=[0, 1])
    data.to_excel(writer, index=False)
