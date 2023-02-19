# /usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import os
import re
import requests
from lxml import etree
from utility.writer import CSVWriter

sys.path.insert(0, os.path.abspath(os.getcwd()+"/../"))
sys.path.insert(0, os.path.abspath(os.getcwd()+"/../../"))

'''
中教网     http://www.teachercn.com/zxyw/Html/ZXYWJA/index.html
中教网-教案 http://www.teachercn.com/Jxal/
'''

GRADE = '年级'
SUBJECT = '科目'
TITLE = '标题'
CONTENT = '内容'
DOC_URL = 'URL'

# 正则-去掉特殊字符
COMPILER = re.compile('[\u3000]')

def save2csv(fpath, key_values):
    writer = CSVWriter.CSVWriter(fpath)
    Headers = ['年级','科目', '标题', 'URL', '内容']
    writer.write(Headers, key_values)

def getDocHtml(url):
    ''' 解析文章 '''
    content = requests.get(url=url).content
    html = etree.HTML(content)
    rows = COMPILER.sub("", '\n'.join(html.xpath(r'//p/text()')))
    return rows

def getGradeHtml(url, grade, subject):
    ''' 解析年级 '''
    content = requests.get(url=url).content
    html = etree.HTML(content)
    rows = html.xpath(r'//div[@align="List"]/table/tr')
    docs = []
    for row in rows:
        documents = row.xpath(r'./td/table/tr')
        for doc in documents:
            infos = doc.xpath(r'./td/a')
            if len(infos) < 1:
                continue
            # grade = infos[0].xpath(r'text()')[0]
            title = infos[1].xpath('@title')[0]
            doc_url = infos[1].xpath('@href')[0]
            print(grade, title, doc_url)

            # 保存文章
            doc = {}
            doc[GRADE] = grade
            doc[SUBJECT] = subject
            doc[TITLE] = title
            doc[DOC_URL] = doc_url
            doc[CONTENT] = getDocHtml(doc_url)
            docs.append(doc)
    return docs

def main():
    # 初中一年级语文教案
    # 年级-文章
    # index = 'http://www.teachercn.com/zxyw/Html/CZYNJYWJA/index{}.html'
    grade = '初中二年级'
    subject = '语文'

    index = 'http://www.teachercn.com/zxyw/Html/CZENJYWJA/index.html'

    documents = []
    for i in range(3):
        if i==0:
            url = index.format('')
        else:
            url = index.format('_' + str(i+1))
        print(url)
        documents.extend(getGradeHtml(url, grade, subject))
    save2csv('/Users/zhengchubin/Desktop/samples.csv', documents)

if __name__ == '__main__':
    main()