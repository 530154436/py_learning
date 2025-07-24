# -*- coding: utf-8 -*-
from typing import Any, Dict

import pandas as pd
from pandas import DataFrame
from config import DATASET_DIR, OUTPUT_DIR
from entity.patent_basic_metric import PatentBasicMetric
from entity.scholar_base import ScholarBase
from entity.scholar_basic_metric import ScholarBasicMetric
from entity.scholar_description import ScholarDescription


def calc_scholar_description():
    print("学者描述性统计")
    file = DATASET_DIR.joinpath("S2-统计分析数据集.xlsx")
    df_scholar_description: DataFrame = pd.read_excel(file, sheet_name="学者描述性统计")
    # print(df_scholar_description.head())

    df_raw: DataFrame = pd.read_excel(DATASET_DIR.joinpath("S0.1-原始数据表-249人学术生涯论文数据汇总.xlsx"))
    descriptions = []
    for i, row in enumerate(df_scholar_description.to_dict(orient="records"), start=1):
        _id = str(row["学者唯一ID"])
        name = row["姓名"]
        scholar = ScholarBase.from_dict(row)
        print(scholar.model_dump())

        df_scholar = df_raw[df_raw["姓名"] == name]
        print(f"{i}/{df_scholar.shape[0]}", name)
        print(df_scholar.head())
        description = ScholarDescription.calc(_id, name, df_scholar.copy())
        descriptions.append(description.model_dump())

    output_file = OUTPUT_DIR.joinpath("学者描述性统计.xlsx")
    with pd.ExcelWriter(output_file) as writer:
        res = pd.DataFrame(descriptions).rename(columns=ScholarDescription.__en2zh__)
        res.to_excel(writer, index=False)


def calc_basic_metrics_paper():
    print("基础指标计算-论文")
    file = DATASET_DIR.joinpath("S2-统计分析数据集.xlsx")
    df_scholar_metric: DataFrame = pd.read_excel(file, sheet_name="二级指标归一化值（2015-2024年）")
    print(df_scholar_metric.head())

    df_raw: DataFrame = pd.read_excel(DATASET_DIR.joinpath("S1.1-目标数据表-249人获奖前后10年论文数据汇总.xlsx"))
    data = []
    for i, row in enumerate(df_scholar_metric.to_dict(orient="records"), start=1):
        _id = str(row["学者唯一ID"])
        name = row["姓名"]

        df_scholar = df_raw[df_raw["姓名"] == name]
        print(f"{i}/{df_scholar.shape[0]}", name)
        print(df_scholar.head())
        _objects = ScholarBasicMetric.calc(_id, name, df_scholar.copy())
        for _object in _objects:
            data.append(_object.model_dump())

    output_file = OUTPUT_DIR.joinpath("二级指标（2015-2024年）-论文.xlsx")
    with pd.ExcelWriter(output_file) as writer:
        res = pd.DataFrame(data).rename(columns=ScholarBasicMetric.__en2zh__)
        res.to_excel(writer, index=False)


def calc_basic_metrics_patent():
    print("基础指标计算-专利")
    file = DATASET_DIR.joinpath("S2-统计分析数据集.xlsx")
    df_patent_metric: DataFrame = pd.read_excel(file, sheet_name="二级指标归一化值（2015-2024年）")
    print(df_patent_metric.head())

    df_raw: DataFrame = pd.read_excel(DATASET_DIR.joinpath("S1.2-目标数据集-249人获奖前后10年专利数据汇总.xlsx"))
    data: list[Dict] = []
    for i, row in enumerate(df_patent_metric.to_dict(orient="records"), start=1):
        _id, name = str(row["学者唯一ID"]), row["姓名"]
        df_patent = df_raw[df_raw["姓名"] == name]
        print(f"{i}/{df_patent.shape[0]}", name)
        print(df_patent.head())
        _objects = PatentBasicMetric.calc(_id, name, df_patent.copy())
        for _object in _objects:
            data.append(_object.model_dump())

    output_file = OUTPUT_DIR.joinpath("二级指标（2015-2024年）-专利.xlsx")
    with pd.ExcelWriter(output_file) as writer:
        res = pd.DataFrame(data).rename(columns=PatentBasicMetric.__en2zh__)
        res.to_excel(writer, index=False)


if __name__ == '__main__':
    # calc_scholar_description()
    # calc_basic_metrics_paper()
    calc_basic_metrics_paper()
