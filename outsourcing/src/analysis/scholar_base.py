# -*- coding: utf-8 -*-
import re
from typing import List
import pandas as pd
from pathlib import Path
from dataclasses import dataclass, field
from dataclasses_json import config, DataClassJsonMixin
from config import CURRENT_YEAR
from analysis.abstract_base import AbstractBase


# 1. 最小基类
@dataclass
class ScholarIdGroupEntity(DataClassJsonMixin):
    id: int = field(metadata=config(field_name="学者唯一ID"))
    name: str = field(metadata=config(field_name="姓名"))


@dataclass
class ScholarBaseEntity(ScholarIdGroupEntity):
    """
    S2.1-学者基本信息（支持中文别名序列化）
    """
    # 基础信息
    company: str = field(metadata=config(field_name="工作单位"))
    birth_year: str = field(metadata=config(field_name="出生年"))
    age: int = field(metadata=config(field_name=f"年龄（截至统计年份-{CURRENT_YEAR}年）"))
    research_fields: str = field(metadata=config(field_name="研究领域"))  # 多个研究领域按分号分隔
    research_types: str = field(metadata=config(field_name="研究类型（1=基础科学，0=工程技术，2=前沿交叉）"))  # 多个研究类型按分号分隔
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
        self.export_to_excel(df.to_dict(orient="records"), clazz=ScholarBaseEntity)
        return df


if __name__ == "__main__":
    from config import DATASET_DIR, OUTPUT_DIR
    _input_file1 = DATASET_DIR.joinpath("S2.1-学者基本信息.xlsx")
    ScholarBase(_input_file1).calc()
