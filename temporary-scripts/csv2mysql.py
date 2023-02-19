# !/usr/bin/env python3
# -*- coding : utf-8 -*-
from utility.reader.CSVReader import CSVReader
from utility.writer.CSVWriter import CSVWriter


reader = CSVReader('data/最终版-渠道归属共享的TOBD.csv')
data = reader.read2JsonList(encoding='gbk')
# for i in data:
#     print(i)

writer = CSVWriter('data/最终版-渠道归属共享的TOBD.utf8.csv')
headers = ['id', 'aff_id', 'aff_name', 'TOgsid', 'TOgs', 'TOxzid', 'TOxz', 'BDgsid', 'BDgs', 'BDxzid', 'BDxz']
writer.write(headers=headers, key_values=data)

