# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path
from analysis.A2_scholar_basic_metric_raw import ScholarBasicMetricRaw
from analysis.abstract_base import AbstractBase
from config import DATASET_DIR, OUTPUT_DIR


class IndexSet:
    A_INDICATORS = [
        "通讯作者论文数（A1）",
        "专利族数量（A2）",
        "第一发明人授权专利数量（A3）"
    ]
    B_INDICATORS = [
        "论文篇均被引频次（B1）",
        "单篇最高被引频次（B2）",
        "前10%高影响力期刊或会议通讯作者论文数量占比（B3）",
        "专利被引频次（B4）"
    ]
    ALL_INDICATORS = A_INDICATORS + B_INDICATORS


class ScholarBasicMetricIndex(AbstractBase):
    __tbl_name__ = f"A2-评价指标数据集"

    def __init__(self, comparison_path: Path,
                 data_path: Path, weight_path: Path):
        super().__init__()
        self.comparison_path = comparison_path
        self.data_path = data_path
        self.weight_path = weight_path

    def calc(self):

        # 加载对照组和指标原始数据
        df_comparison = pd.read_excel(self.comparison_path)
        df_data = pd.read_excel(self.data_path)
        df_data = pd.merge(df_comparison, df_data, how="left", on=["学者唯一ID", "姓名"])
        df_data.fillna(0, inplace=True)
        print(df_data)

        # 加载权重值
        df_weight = pd.read_excel(self.weight_path)[["研究类型（1=基础科学，0=工程技术，2=前沿交叉）"] + IndexSet.ALL_INDICATORS]
        df_weight.columns = ["研究类型（1=基础科学，0=工程技术，2=前沿交叉）"] + [f"权重_{i}" for i in IndexSet.ALL_INDICATORS]
        df_data_with_w = pd.merge(df_data, df_weight, on=["研究类型（1=基础科学，0=工程技术，2=前沿交叉）"], how="left")
        print(df_data_with_w)


        # 按领域分组
        data = []
        for _, chunk in df_data_with_w.groupby(["研究领域", "时间窗口（0=获奖前5年，1=获奖后5年）"]):
            # 归一化（min-max）、计算权重*归一化值
            for column in IndexSet.ALL_INDICATORS:
                _max = chunk[column].max()
                _min = chunk[column].min()
                if _max == _min:
                    chunk[f"归一化_{column}"] = 0.0  # 所有值相同，归一化为0
                else:
                    chunk[f"归一化_{column}"] = (chunk[column] - _min) / (_max - _min)
            data.append(chunk)

        df_result = pd.concat(data)
        for column in IndexSet.ALL_INDICATORS:
            df_result[f"得分_{column}"] = df_result[f"权重_{column}"] * df_result[f"归一化_{column}"]
        print(df_data_with_w)

        # 计算一级指标
        df_result["学术生产力"] = sum(df_result[f"得分_{col}"] for col in IndexSet.A_INDICATORS)
        df_result["学术影响力"] = sum(df_result[f"得分_{col}"] for col in IndexSet.B_INDICATORS)
        df_result["综合分数"] = df_result["学术生产力"] + df_result["学术影响力"]

        df_result = df_result.sort_values(by=["关联ID", "时间窗口（0=获奖前5年，1=获奖后5年）"],
                                          ascending=[True, True])
        print(df_result)
        self.save_to_excel(df_result, save_file=f"{self.__tbl_name__}.xlsx")


if __name__ == "__main__":
    _input_file0 = DATASET_DIR.joinpath("S2.2-学者关联信息表-对照分组.xlsx")
    _input_file1 = OUTPUT_DIR.joinpath(f"{ScholarBasicMetricRaw.__tbl_name__}.xlsx")
    _input_file2 = DATASET_DIR.joinpath("S2.3-指标计算权重值.xlsx")
    _metric = ScholarBasicMetricIndex(_input_file0, data_path=_input_file1, weight_path=_input_file2)
    _metric.calc()
