# -*- coding: utf-8 -*-
import re
from typing import List
import pandas as pd
from pathlib import Path
from dataclasses import dataclass, field
from dataclasses_json import config, DataClassJsonMixin
from pandas import DataFrame
from config import CURRENT_YEAR
from analysis.abstract_base import AbstractBase


# 1. 最小基类
@dataclass
class ScholarIdNameEntity(DataClassJsonMixin):
    id: int = field(metadata=config(field_name="学者唯一ID"))
    name: str = field(metadata=config(field_name="姓名"))


@dataclass
class ScholarBaseEntity(ScholarIdNameEntity):
    """
    学者基本信息（支持中文别名序列化）
    """
    # 基础信息
    company: str = field(metadata=config(field_name="工作单位"))
    birth_year: str = field(metadata=config(field_name="出生年"))
    age: int = field(metadata=config(field_name=f"年龄（截至统计年份-{CURRENT_YEAR}年）"))
    research_field: str = field(metadata=config(field_name="研究领域"))
    research_type: str = field(metadata=config(field_name="研究类型（1=基础科学，0=工程技术，2=前沿交叉）"))
    main_research_direction: str = field(metadata=config(field_name="主要研究方向"))
    academic_honors: str = field(metadata=config(field_name="学术奖励荣誉/资助"))


class ScholarBase(AbstractBase):
    """
    学者基本信息
    """
    __tbl_name__ = "A0-学者基本信息"

    def __init__(self, basic_info_path: Path):
        self.basic_info_path = basic_info_path

    @staticmethod
    def calc_age(x):
        # 计算年龄
        match = re.search(r"\d+", str(x))
        return CURRENT_YEAR - int(match.group())

    def calc(self) -> pd.DataFrame:
        df = pd.read_excel(self.basic_info_path)
        df["age"] = df["出生年"].apply(lambda x: self.calc_age(x))
        self.save_to_excel(df.to_dict(orient="records"), clazz=ScholarBaseEntity)
        return df


if __name__ == "__main__":
    from config import DATASET_DIR, OUTPUT_DIR
    # 设置 Pandas 打印选项
    pd.set_option('display.max_rows', 100)  # 显示所有行
    pd.set_option('display.max_columns', None)  # 显示所有列
    pd.set_option('display.width', 2000)  # 不折叠单元格
    pd.set_option('display.max_colwidth', None)  # 显示完整的单元格内容

    _input_file1 = DATASET_DIR.joinpath("S2.1-学者基本信息.xlsx")
    ScholarBase(_input_file1).calc()
