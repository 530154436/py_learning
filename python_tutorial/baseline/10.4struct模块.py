# /usr/bin/env python3
# -*- coding:utf-8 -*-
import struct

def test_struct():
    '''
    struct模块解决bytes和其他二进制数据类型的转换。
    :return:
    '''
    sp = struct.pack('>I', 10240099)
    print(sp)

    su = struct.unpack('>IH', b'\xf0\xf0\xf0\xf0\x80\x80')
    print(su)

    s = b'\x42\x4d\x38\x8c\x0a\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28' \
        b'\x00\x00\x00\x80\x02\x00\x00\x68\x01\x00\x00\x01\x00\x18\x00'
    su = struct.unpack('<ccIIIIIIHH', s)
    print(su)

if __name__ == '__main__':
    test_struct()