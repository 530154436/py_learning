#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/08/28
@function:
"""
import requests
import json

def Siri():
    print("您好，我是Siri。有什么需要帮助的吗？[输入0退出]")
    while True:
        text = input("我: ")
        if text == '0':
            print("Siri: 再见～")
            break
        url = "http://127.0.0.1:5200/answer?question="+text
        response = requests.get(url)
        result = json.loads(response.content)['data']
        print("Siri:",result)

if __name__ == '__main__':
    Siri()
