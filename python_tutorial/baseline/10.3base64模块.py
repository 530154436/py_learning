# /usr/bin/env ppython3
# -*- coding:utf-8 -*-
import base64

def test_base64():
    '''
    Base64是一种用64个字符来表示任意二进制数据的方法。由于2的6次方等于64，所以每6个比特为一个单元，对应某个可打印字符。
    三个字节有24个比特，对应于4个Base64单元，即3个字节可表示4个可打印字符。
    使用的字符包括大小写字母各26个，加上10个数字，和加号“+”，斜杠“/”，一共64个字符，等号“=”用来作为后缀用途。
    :return:
    '''
    en = base64.b64encode(b'binary\x00string')
    print(en)
    de = base64.b64decode(b'YmluYXJ5AHN0cmluZw==')
    print(de)

    en = base64.b64encode(b'i\xb7\x1d\xfb\xef\xff')
    print(en)
    en = base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff')
    print(en)
    de = base64.urlsafe_b64decode(b'abcd--__')
    print(de)

def safe_base64_decode(b64_str):
    len_res = len(b64_str)%4
    if len_res % 4 == 0:
        return base64.b64decode(b64_str)
    else:
        return base64.b64decode(b64_str+b'='*(4-len_res))


def exercise():
    '''
    请写一个能处理去掉=的base64解码函数：
    :return:
    '''
    assert b'abcd' == safe_base64_decode(b'YWJjZA=='), safe_base64_decode('YWJjZA==')
    assert b'abcd' == safe_base64_decode(b'YWJjZA'), safe_base64_decode('YWJjZA')
    print('Pass')

if __name__ == '__main__':
    # test_base64()
    exercise()