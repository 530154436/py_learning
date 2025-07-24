# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame
from config import DATASET_DIR
from entity.scholar_base import ScholarBase
from entity.scholar_description import ScholarDescription


def pipeline():
    print("计算 学者描述性统计")
    file = DATASET_DIR.joinpath("S2-统计分析数据集.xlsx")
    df_scholar_description: DataFrame = pd.read_excel(file, sheet_name="学者描述性统计")
    # print(df_scholar_description.head())

    df_raw: DataFrame = pd.read_excel(DATASET_DIR.joinpath("S0.1-原始数据表-249人学术生涯论文数据汇总.xlsx"))
    for i, row in enumerate(df_scholar_description.to_dict(orient="records"), start=1):
        name = row["姓名"]
        scholar = ScholarBase.from_dict(row)
        print(scholar.model_dump())

        df_scholar = df_raw[df_raw["姓名"] == name]
        print(f"{i}/{df_scholar.shape[0]}", name)
        print(df_scholar.head())
        scholar_description = ScholarDescription.from_dataframe(df_scholar)

        break


if __name__ == '__main__':
    pipeline()
