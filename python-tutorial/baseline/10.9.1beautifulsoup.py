# /usr/bin/env python3
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup

'''
pip3 install beautifulsoup4
pip3 install lxml
'''

html = '''
    <html>
    <head></head>
    <body>
    <!-- test html parser -->
        <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
    </body></html>
    '''.strip()

#HTML解析器
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify(formatter='html'))
# print(soup.p)

# for child in soup.descendants:
#     print(child)

# for child in soup.body.children:
#     print(child)

#第三方解析器lxml
# soup = BeautifulSoup(html, 'lxml')
# print(soup.prettify())