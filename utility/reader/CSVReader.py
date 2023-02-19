#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import csv
class CSVReader:
    def __init__(self, fpath):
        self.fpath = fpath
        self.file = None

    def openFile(self, encoding='utf-8'):
        try:
            self.file = open(self.fpath, 'r', encoding=encoding)
        except Exception as e:
            print('Error while opening file.', str(e))

    def closeFile(self):
        try:
            self.file.close()
        except Exception as e:
            print('Error while closing file.', str(e))

    def read(self):
        '''

        :param headers:
        :param datas:
        :return:
        '''
        if self.file is None:
            self.openFile()
        f_csv = csv.reader(self.file)
        return f_csv

    def read2JsonList(self, transformTypes=None, encoding='utf8'):
        '''
        csv转json
        :param transformType: 标题列对应的数据类型
        :return:  json列表
        '''
        if self.file is None:
            self.openFile(encoding)
        csv_rows = []
        reader = csv.DictReader(self.file)
        title = reader.fieldnames
        count = 0
        for row in reader:
            try:
                if transformTypes:
                    csv_rows.extend([{title[i]: transformTypes[i](row[title[i]]) for i in range(len(title))}])
                else:
                    csv_rows.extend([{title[i]: row[title[i]] for i in range(len(title))}])
                count += 1
                if count % 100 == 0:
                    print(title)
                    print("读取csv文件: {}".format(count))
            except Exception as e:
                print(e, row)
        return csv_rows



