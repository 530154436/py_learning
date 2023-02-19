# /usr/bin/env python3
# -*- coding:utf-8 -*-

from urllib import request, parse
from xml.parsers.expat import ParserCreate

def test_get():
    '''
    发送一个GET请求到指定的页面，然后返回HTTP的响应
    :return:
    '''
    with request.urlopen(url='https://app.douban.com/v2/book/2129650') as r :
        data = r.read().decode('utf-8')
        # 状态码
        print(r.status, r.reason)
        # 请求头
        for k,v in r.getheaders():
            print('%s: %s' % (k,v))
        print(data)

    # 模拟浏览器发送GET请求，就需要使用Request对象，
    # 通过往Request对象添加HTTP头，我们就可以把请求伪装成浏览器。
    req = request.Request('http://www.douban.com/')
    req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    with request.urlopen(req) as r :
        data = r.read().decode('utf-8')
        # 状态码
        print(r.status, r.reason)
        # 请求头
        for k,v in r.getheaders():
            print('%s: %s' % (k,v))
        print(data)

def test_post():
    print('Login to weibo.cn...')
    email = input('Email: ')
    passwd = input('Password: ')
    login_data = parse.urlencode([
        ('username', email),
        ('password', passwd),
        ('entry', 'mweibo'),
        ('client_id', ''),
        ('savestate', '1'),
        ('ec', ''),
        ('pagerefer', 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F')
    ])

    req = request.Request('https://passport.weibo.cn/sso/login')
    req.add_header('Origin', 'https://passport.weibo.cn')
    req.add_header('User-Agent',
                   'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    req.add_header('Referer',
                   'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F')

    with request.urlopen(req, data=login_data.encode('utf-8')) as f:
        print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        print('Data:', f.read().decode('utf-8'))

if __name__ == '__main__':
    # test_get()
    test_post()
