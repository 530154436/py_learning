# /usr/bin/env python3
# -*- coding:utf-8 -*-

from html.parser import HTMLParser
from lxml import etree
import requests

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print('<%s>' % tag)

    def handle_endtag(self, tag):
        print('<%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('<%s>' % tag)

    def handle_data(self, data):
        print(data)

    def handle_comment(self, data):
        print('<!--', data, '-->')

    def handle_entityref(self, name):
        print('&#%s' % name)

    def handle_charref(self, name):
        print('&#%s' % name)

def test_html_parse():
    html = '''
    <html>
    <head></head>
    <body>
    <!-- test html parser -->
        <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
    </body></html>
    '''.strip()
    parser = MyHTMLParser()
    parser.feed(html)

def get_html(url):
    content = requests.get(url=url).content
    html = etree.HTML(content)
    nodes = html.xpath(r'//ul[@class="list-recent-events menu"]/li')
    all = []
    for node in nodes:
        title = node.xpath(r'h3[@class="event-title"]/a/text()')
        date = node.xpath(r'p/time/text()')
        year = node.xpath(r'p/time/span[@class="say-no-more"]/text()')
        location = node.xpath(r'p/span[@class="event-location"]/text()')
        # print(type(title), title)
        # print(type(date), date, year)
        # print(type(location), location)
        data={}
        data['会议主题'] = title[0]
        data['会议时间'] = date[0] + year[0]
        data['会议地点'] = location[0]
        all.append(data)
    return all

def exercise():
    '''
    找一个网页，例如https://www.python.org/events/python-events/，
    用浏览器查看源码并复制，然后尝试解析一下HTML，输出Python官网发布的会议时间、名称和地点。
    参考
    http://cuiqingcai.com/2621.html
    http://www.w3school.com.cn/xpath/xpath_syntax.asp
    :return:
    '''
    all = get_html(url='https://www.python.org/events/python-events/')
    for s in all:
        print(s)


if __name__ == '__main__':
    test_html_parse()
    # exercise()