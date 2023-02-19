#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import csv
# 取消csv列名长度的限制
csv.field_size_limit(1000)

class CSVWriter:
    def __init__(self, fpath, encoding='utf-8', mode='w'):
        self.fpath = fpath
        self.file = None
        self.encoding = encoding
        self.mode = mode

    def openFile(self):
        try:
            self.file = open(self.fpath, self.mode, encoding=self.encoding)
        except Exception as e:
            print('Error while opening file.', str(e))

    def closeFile(self):
        try:
            self.file.close()
        except Exception as e:
            print('Error while closing file.', str(e))

    def write(self, headers, key_values):
        '''
        输出字典
        :param headers:
        :param key_values:
        :return:
        '''
        if self.file == None:
            self.openFile()
        f_csv = csv.DictWriter(self.file, headers)

        f_csv.writeheader()
        for data in key_values:
            if self.encoding != "utf-8":
                for k, v in data.items():
                    if v is None:
                        data[k] = ""
                    # 对于非法字符则忽略 eg:\u200b
                    data[k] = str(v).encode(self.encoding, "ignore").decode(self.encoding)
            f_csv.writerow(data)
        print('Write to %s done.\n' % self.fpath)
        self.closeFile()


