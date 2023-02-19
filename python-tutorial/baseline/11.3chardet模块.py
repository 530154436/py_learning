#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import chardet

def demoBytes():
    asciiStr = b'I am zhengchubin'
    print(chardet.detect(asciiStr))

    data = '你好'
    gbk = data.encode('gbk')
    utf = data.encode('utf-8')

    print(chardet.detect(gbk))
    print(chardet.detect(utf))

    data = '最新の主要ニュース'.encode('euc-jp')
    print(chardet.detect(data))
if __name__ == '__main__':
    # demoGet()
    demoBytes()