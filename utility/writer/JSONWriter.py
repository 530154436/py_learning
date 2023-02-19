#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
class JSONWriter:
    def __init__(self, fpath, encoding='utf-8'):
        self.fpath = fpath
        self.writer = None
        self.encoding = encoding

    def openFile(self):
        try:
            self.writer = open(self.fpath, 'w', encoding=self.encoding)
        except Exception as e:
            print('Error while opening file.', str(e))

    def closeFile(self):
        try:
            self.writer.close()
        except Exception as e:
            print('Error while closing file.', str(e))

    def write(self, datas):
        '''
        输出字典
        :param headers:
        :param datas:
        :return:
        '''
        if self.writer == None:
            self.openFile()
        for data in datas:
            if self.encoding != "utf-8":
                for k, v in data.items():
                    if v is None:
                        data[k] = ""
                    # 对于非法字符则忽略 eg:\u200b
                    data[k] = str(v).encode(self.encoding, "ignore").decode(self.encoding)
            self.writer.write(json.dumps(data))
            self.writer.write('\n')
        print('Write to %s done.' % self.fpath)
        self.closeFile()


