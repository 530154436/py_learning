# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import re

# 匹配电话号码 0755-26632121
tel_rex = r'^\d{4}-\d{3,8}$'

# 匹配连续的多个空格
space_rex = r'[\s\,\;]+'

# 识别合法的时间 19:05:30
time_rex = r'^(0[0-9]|1[0-9]|2[0-3]|[0-9])\:' \
           r'(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])\:' \
           r'(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])'

# 识别邮箱
email_rex_1 = r'^([0-9a-zA-Z]+|[0-9a-zA-Z]+\.[0-9a-zA-Z]+)@[0-9a-zA-Z]+\.com$'
email_rex_2 = r'^[0-9a-zA-Z]+\.([a-zA-Z]+@[0-9a-zA-Z]+\.[a-zA-Z]+)$'

url_rex = r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-zA-Z][0-9a-zA-Z]))+)'

REPLY_PATTERN = '@.+?[：:\s]|//@.+?[:：\s]|回复@.+?[:：\s]|#.+?#|http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

EMOJI_PATTERN = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)

'''
    匹配 match
'''
def test_match():
    text = '0755-26632217'
    tel = re.match(tel_rex, text)
    if tel:
        print('yes')
    else:
        print('no')

'''
    切分字符串
'''
def test_split():
    s1 = 'a a , , dsa b as;    c'
    # 无法识别连续的空格
    print(s1.split(' '))
    # 识别连续的空格
    print(re.split(space_rex, s1))

'''
    分组
'''
def test_group():
    group_rex = r'^(\d{4})-(\d{3,8})$'
    text = '0755-26632217'
    m = re.match(group_rex, text)
    print(m.group(0))
    print(m.group(1))
    print(m.group(2))

    t = '19:05:30'
    m = re.match(time_rex, t)
    print(m.groups())

'''
    贪婪匹配
'''
def test_greedy():
    print(re.match(r'^(\d+)(0*)$', '102300').groups())
    print(re.match(r'^(\d+?)(0*)$', '102300').groups())

'''
    编译
'''
def test_compile():
    tel_rex = r'^(\d{4})-(\d{3,8})$'
    tel_com = re.compile(tel_rex)
    print(tel_com.match('0775-123123').groups())
    print(tel_com.match('9012-123').groups())

'''
    练习
'''
def test_email():
    email_com_1 = re.compile(email_rex_1)
    email_com_2 = re.compile(email_rex_2)
    print(email_com_1.match('someone@gmail.com').group())
    print(email_com_1.match('bill.gates@microsoft.com').group())
    print(email_com_2.match('chubin.edwad@microsoft.org').groups())

if __name__ == '__main__':
    # test_match()
    # test_split()
    # test_group()
    # test_greedy()
    # test_compile()
    # test_email()
    text = u'This dog\U0001f602'
    print(text)  # with emoji
    print(EMOJI_PATTERN.sub(r'', text))

    # 查找替换
    blog = '大家好，我是，我来自https://blog.csdn.net/u013421629/article/details/82918060，谢谢'
    blog = re.sub(url_rex, r'<aherf=\1></a>', blog)