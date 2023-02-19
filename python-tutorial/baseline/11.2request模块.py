# /usr/bin/env python3
# -*- coding:utf-8 -*-
import requests

def demoGet():
    r = requests.get('https://www.douban.com/')
    print(r.status_code)
    # print(r.text)

    params = {'q': 'python', 'cat': '1001'}
    r = requests.get('https://www.douban.com/search', params=params)
    print(r.url)
    print(r.encoding)
    # print(r.content)

    r = requests.get('https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%202151330&format=json')
    print(r.json())

def demoPost():
    url = 'https://accounts.douban.com/login'
    data = {'form_email': 'abc@example.com', 'form_password': '123456'}
    r = requests.post(url=url, data=data)
    print(r.status_code)

    # 上传文件
    upload_files = {'file':open('11.2request模块.py', 'rb')}
    r = requests.post(url, files=upload_files)
    print(r.status_code)
    print(r.headers)
    # print(r.cookies)

    cs = {'token': '12345', 'status': 'working'}
    r = requests.get(url,cookies=cs)
    print(r)


if __name__ == '__main__':
    # demoGet()
    demoPost()