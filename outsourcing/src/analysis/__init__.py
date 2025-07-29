# -*- coding: utf-8 -*-
import pandas as pd


class DataType(object):
    paper = "论文"
    patent = "专利"
    patent_families = "专利同族"


# 设置 Pandas 打印选项
pd.set_option('display.max_rows', 100)  # 显示所有行
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.width', 2000)  # 不折叠单元格
pd.set_option('display.max_colwidth', None)  # 显示完整的单元格内容
