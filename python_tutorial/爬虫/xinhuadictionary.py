# /usr/bin/env python3
# -*- coding:utf-8 -*-

from lxml import etree
import requests
'''
    爬取新华字典所有的字, 共 16159
'''
def getChar(url):
    content = requests.get(url=url).content.decode('gbk')
    html = etree.HTML(content)
    nodes = html.xpath('//table[@style="border-collapse:collapse"]/tr')
    chars = []
    for node in nodes:
        char = node.xpath('./td/a/text()')
        if len(char) == 1:
            chars.append(char[0])
    return chars

def getAllChars():
    '''
    找一个网页，例如https://www.python.org/events/python-events/，
    用浏览器查看源码并复制，然后尝试解析一下HTML，输出Python官网发布的会议时间、名称和地点。
    参考
    http://cuiqingcai.com/2621.html
    http://www.w3school.com.cn/xpath/xpath_syntax.asp
    :return:
    '''
    allChars = []
    for page in range(1, 539):
        chars = getChar(url='http://xh.bm8.com.cn/all.asp?PAGE={}'.format(page))
        allChars.extend(chars)
        print('get char count: {}'.format(len(allChars)))
    return set(allChars)

def save(path='/Users/zhengchubin/Desktop/xinhua.txt'):
    with open(path, mode='w', encoding='utf-8') as f:
        for char in chars:
            f.write(char)
            f.write('\n')
            f.flush()

if __name__ == '__main__':
    # test_html_parse()
    chars = getAllChars()
    save()


