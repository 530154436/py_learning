# -*- coding: utf-8 -*-
import json
import pandas as pd
from pathlib import Path
from pydantic import BaseModel, Field
from typing import OrderedDict
from config import DATASET_DIR, OUTPUT_DIR
from entity.abstract_base import AbstractBase
from entity.s2_2_scholar_basic_metric import ScholarBasicMetric


class ScholarSummary(AbstractBase):
    __tbl_name__ = "综合报告"

    def __init__(self, basic_info_path: Path, data_path: Path):
        super().__init__()
        self.basic_info_path = basic_info_path
        self.data_path = data_path

    def calc(self) -> pd.DataFrame:
        pass


if __name__ == "__main__":
    # 设置 Pandas 打印选项
    pd.set_option('display.max_rows', 100)  # 显示所有行
    pd.set_option('display.max_columns', None)  # 显示所有列
    pd.set_option('display.width', 2000)  # 不折叠单元格
    pd.set_option('display.max_colwidth', None)  # 显示完整的单元格内容

    _input_file0 = DATASET_DIR.joinpath("S0.0-获奖人基础信息表.xlsx")
    _input_file1 = OUTPUT_DIR.joinpath(ScholarBasicMetric.__tbl_name__ + ".xlsx")
    _metric = ScholarSummary(_input_file0, data_path=_input_file1)
    _metric.calc()
