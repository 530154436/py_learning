# -*- coding: utf-8 -*-
import pandas as pd
from dataclasses import field, dataclass
from dataclasses_json import config
from pathlib import Path
from analysis import DataType
from analysis.abstract_base import AbstractBase
from analysis.scholar_base import ScholarIdGroupEntity
from config import TIME_WINDOW_0_END, TIME_WINDOW_1_END, TIME_WINDOW_0_START, TIME_WINDOW_1_START
from config import DATASET_DIR, OUTPUT_DIR
from utils.pd_common_util import contains_in


class ScholarBasicMetric(AbstractBase):
    __tbl_name__ = f"A2-评价指标数据集"

    def __init__(self, basic_info_path: Path,
                 data_paper_path: Path, data_patent_path: Path, **kwargs):
        super().__init__()
        self.basic_info_path = basic_info_path
        self.data_paper_path = data_paper_path
        self.data_patent_path = data_patent_path
        self.data_weight_path = kwargs.get("data_weight_path")

    def calc(self):

        # 加载权重值
        df_weight = pd.read_excel(self.data_weight_path)
        columns = [
            "通讯作者论文数（A1）",
            "专利族数量（A2）",
            "第一发明人授权专利数量（A3）",
            "论文篇均被引频次（B1）",
            "单篇最高被引频次（B2）",
            "前10%高影响力期刊或会议通讯作者论文数量占比（B3）",
            "专利被引频次（B4）",
        ]
        df_weight.columns = ["研究类型（1=基础科学，0=工程技术，2=前沿交叉）"] + [f"w_{i}" for i in columns + ["学术生产力", "学术影响力"]]
        df_data_with_weight = pd.merge(df_data_zh, df_weight, on=["研究类型（1=基础科学，0=工程技术，2=前沿交叉）"], how="left")

        # 归一化（min-max）
        for column in columns:
            _max = df_data_with_weight[column].max()
            _min = df_data_with_weight[column].min()
            df_data_with_weight[f"std_{column}"] = (df_data_with_weight[column] - _min) / (_max - _min)
        print(df_data_with_weight)
        print(df_data_with_weight.columns)

        # 计算得分：权重*归一化值
        for column in columns:
            df_data_with_weight[f"score_{column}"] = df_data_with_weight[f"w_{column}"] * df_data_with_weight[f"std_{column}"]

        # 计算一级指标
        df_data_with_weight["学术生产力"] = 0
        for column in ["通讯作者论文数（A1）", "专利族数量（A2）", "第一发明人授权专利数量（A3）"]:
            df_data_with_weight["学术生产力"] = df_data_with_weight["学术生产力"] + df_data_with_weight[f"score_{column}"].values

        df_data_with_weight["学术影响力"] = 0
        for column in ["论文篇均被引频次（B1）", "单篇最高被引频次（B2）",
                       "前10%高影响力期刊或会议通讯作者论文数量占比（B3）", "专利被引频次（B4）"]:
            df_data_with_weight["学术影响力"] = df_data_with_weight["学术生产力"] + df_data_with_weight[f"score_{column}"].values

        df_data_with_weight["综合分数"] = \
            df_data_with_weight["w_学术影响力"] * df_data_with_weight["学术影响力"] \
            + df_data_with_weight["w_学术生产力"] * df_data_with_weight["学术生产力"]
        print(df_data_with_weight)
        self.save_to_excel(df_data_with_weight, save_file=f"{self.__tbl_name__}.xlsx")


if __name__ == "__main__":
    _input_file0 = DATASET_DIR.joinpath("S2.1-学者基本信息.xlsx")
    _input_file1 = DATASET_DIR.joinpath("S1.1-目标数据表-249人获奖前后10年论文数据汇总.xlsx")
    _input_file2 = DATASET_DIR.joinpath("S1.2-目标数据集-249人获奖前后10年专利数据汇总.xlsx")
    _input_file3 = DATASET_DIR.joinpath("S2.3-指标计算权重值.xlsx")
    _metric = ScholarBasicMetric(_input_file0, data_paper_path=_input_file1,
                                 data_patent_path=_input_file2, data_weight_path=_input_file3)
    _metric.calc()
