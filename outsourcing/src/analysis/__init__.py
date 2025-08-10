# -*- coding: utf-8 -*-
import pandas as pd


class DataType(object):
    paper = "论文"
    patent = "专利"
    patent_families = "专利同族"


class GrowthPattern(object):
    szlxx: str = "始终领先型"
    szlhx: str = "始终落后型"
    ksczx: str = "快速成长型"
    czfhx: str = "成长放缓型"


RESEARCH_TYPE_MAPPING = {
    "0": "工程技术",
    "1": "基础科学",
    "2": "前沿交叉"
}
