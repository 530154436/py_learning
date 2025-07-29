# -*- coding: utf-8 -*-
import re

import pandas as pd
from typing import List
from pathlib import Path
from pydantic import BaseModel, Field
from config import TIME_WINDOW_1_END, TIME_WINDOW_0_END, TIME_WINDOW_0_START, CURRENT_YEAR
from analysis.abstract_base import AbstractBase
from utils.pd_common_util import contains_in


class ScholarDescriptionEntity(BaseModel):
    """
    学者唯一ID
    姓名
    工作单位
    出生年
    年龄（截至统计年份-2025年）
    研究领域
    研究类型（1=基础科学，0=工程技术，2=前沿交叉）
    主要研究方向
    学术奖励荣誉/资助
    学者职业生涯长度（2024-首篇论文发表年份+1）
    学者活跃年数（发表≥1篇论文的年份数）
    学者职业生涯总发文量（截至2024年，wos核心合集SCI、CPCI-S，article、review、proceeding paper）
    学者职业生涯SCI论文总发文量
    学者职业生涯会议论文总发文量
    2019年学者H指数（截止到2019年）
    2024年学者H指数（截止到2024年）
    10年总发文量
    10年SCI论文总发文量
    10年会议论文总发文量
    10年申请专利
    10年授权专利
    10年专利族数量
    """
    # 基础信息
    id: str = Field(serialization_alias="学者唯一ID")
    name: str = Field(serialization_alias="姓名")
    company: str = Field(serialization_alias="工作单位")
    birth_year: str = Field(serialization_alias="出生年")
    age: str = Field(serialization_alias=f"年龄（截至统计年份-{CURRENT_YEAR}年）")
    research_field: str = Field(serialization_alias="研究领域")
    research_type: str = Field(serialization_alias="研究类型（1=基础科学，0=工程技术，2=前沿交叉）")
    main_research_direction: str = Field(serialization_alias="主要研究方向")
    academic_honors: str = Field(serialization_alias="学术奖励荣誉/资助")

    # 统计类指标
    career_length: int = Field(serialization_alias=f"学者职业生涯长度（{TIME_WINDOW_1_END}-首篇论文发表年份+1）")
    active_years: int = Field(serialization_alias="学者活跃年数（发表≥1篇论文的年份数）")
    career_total_pub: int = Field(serialization_alias="学者职业生涯总发文量")
    career_total_sci_pub: int = Field(serialization_alias="学者职业生涯SCI论文总发文量")
    career_total_meeting_pub: int = Field(serialization_alias="学者职业生涯会议论文总发文量")
    h_index_tw_0_years: int = Field(serialization_alias=f"{TIME_WINDOW_0_END}年学者H指数（截止到{TIME_WINDOW_0_END}年）")
    h_index_tw_1_years: int = Field(serialization_alias=f"{TIME_WINDOW_1_END}年学者H指数（截止到{TIME_WINDOW_1_END}年）")
    total_pub_10_years: int = Field(serialization_alias="10年总发文量")
    total_sci_pub_10_years: int = Field(serialization_alias="10年SCI论文总发文量")
    total_meeting_pub_10_years: int = Field(serialization_alias="10年会议论文总发文量")
    # total_preprint_pub_10_years: int = Field(serialization_alias="10年预印本总发文量")
    patent_apply_num_10_years: int = Field(serialization_alias="10年申请专利")
    patent_grant_num_10_years: int = Field(serialization_alias="10年授权专利")
    patent_families_num_10_years: int = Field(serialization_alias="10年专利族数量")


class ScholarDescription(AbstractBase):
    __tbl_name__ = "A1-学者描述性统计"

    def __init__(self, basic_info_path: Path, data_paper_path: Path):
        super().__init__()
        self.basic_info_path = basic_info_path
        self.data_paper_path = data_paper_path

    def calc_one_in_paper(self, df: pd.DataFrame) -> dict:
        """
        从DataFrame创建ScholarDescription实例
        """
        # 预处理
        df = self.preprocessing_paper_data(df)

        # 1、学者职业生涯长度：2024-首篇论文发表年份+1
        first_paper_year = df["Publication Year"].astype(int).min()
        career_length = TIME_WINDOW_1_END - int(first_paper_year) + 1
        print("学者职业生涯长度:", career_length)

        # 2、学者活跃年数：发表≥1篇论文的年份数
        active_years = df["Publication Year"].nunique(dropna=True)
        print("学者活跃年数:", active_years)

        # 3、学者职业生涯总发文量：截止2024年发表论文总量
        career_total_pub = df["UT (Unique WOS ID)"].nunique(dropna=True)
        print("学者职业生涯总发文量:", career_total_pub)

        # 4、2019年学者H指数（截止到2019年）
        df_sub = df[df["Publication Year"] <= TIME_WINDOW_0_END]
        h_index_tw_0_years = self.calc_h_index(df_sub["Cited Reference Count"].tolist())
        print(f"学者H指数：截止到{TIME_WINDOW_0_END}年:", h_index_tw_0_years)

        # 5、学者H指数：截止到2024年
        df_sub = df[df["Publication Year"] <= TIME_WINDOW_1_END]
        h_index_tw_1_years = self.calc_h_index(df_sub["Cited Reference Count"].tolist())
        print(f"学者H指数：截止到{TIME_WINDOW_1_END}年:", h_index_tw_1_years)

        # 6、10年总发文量
        mask_10_year = (TIME_WINDOW_0_START <= df["Publication Year"]) & (df["Publication Year"] <= TIME_WINDOW_1_END)
        total_pub_10_years = df[mask_10_year]["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"10年总发文量（不区分Document Type）：", total_pub_10_years)

        # 7、10年SCI论文总发文量：统计Web of Science Index中的Science Citation Index Expanded (SCI-EXPANDED)，即SCI论文
        mask = mask_10_year \
            & contains_in(df["Web of Science Index"], ["Science Citation Index Expanded (SCI-EXPANDED)"]) \
            & contains_in(df["Document Type"], ["Article", "Review"])
        total_sci_pub_10_years = df[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"10年SCI论文总发文量:", total_sci_pub_10_years)

        # 8、10年会议论文总发文量：统计Web of Science Index中的Conference Proceedings Citation Index - Science (CPCI-S)，即会议论文
        # TODO: （多个会议的情况，id+优先级SCI-E>CPCI-S>preprint）
        mask = mask_10_year \
            & contains_in(df["Web of Science Index"], ["Conference Proceedings Citation Index - Science (CPCI-S)"]) \
            & (~contains_in(df["Web of Science Index"], ["Science Citation Index Expanded (SCI-EXPANDED)"]))
        total_meeting_pub_10_years = df[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"10年会议论文总发文量:", total_meeting_pub_10_years)

        # 9、10年预印本总发文量：统计Web of Science Index中的preprint，即预印本
        mask = mask_10_year \
               & contains_in(df["Web of Science Index"], ["preprint"])
        total_preprint_pub_10_years = df[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"10年预印本总发文量:", total_preprint_pub_10_years)

        return dict(
            career_length=career_length,
            active_years=active_years,
            career_total_pub=career_total_pub,
            h_index_tw_0_years=h_index_tw_0_years,
            h_index_tw_1_years=h_index_tw_1_years,
            total_pub_10_years=total_pub_10_years,
            total_sci_pub_10_years=total_sci_pub_10_years,
            total_meeting_pub_10_years=total_meeting_pub_10_years,
            total_preprint_pub_10_years=total_preprint_pub_10_years,
        )

    def output_to_excel(self, data: List[dict]):

        # join基础信息表
        # 1、存英文字段
        # 2、输出中文字段

        # # 保存结果
        # entity = ScholarDescriptionEntity(**result)
        # results.append(entity.model_dump(mode='json', by_alias=True))
        # print()
        # df = pd.DataFrame(results)
        # self.save_to_excel(df)
        # return df
        pass

    def calc(self) -> pd.DataFrame:

        # 读取基础信息表和数据表
        df_basic_info = pd.read_excel(self.basic_info_path)
        df_data = pd.read_excel(self.data_paper_path)
        print(df_basic_info.head())
        print(df_data.head())

        # 按学者维度分析
        results = []
        for i, row in enumerate(df_basic_info.to_dict(orient="records"), start=1):
            _id = row["学者唯一ID"]
            name = row["姓名"]
            print(row["出生年"])
            age = int(re.search(r"\d+", str(row["出生年"])).group())  # 计算年龄
            result = {
                "id": _id,
                "name": name,
                "age": age,
            }
            df_data_subset = df_data[df_data["姓名"] == name]
            print(f"{i:03d}/{df_basic_info.shape[0]}: 学者唯一ID={_id}, 姓名={name}, 数据行数={df_data_subset.shape[0]}")
            stats: dict = self.calc_one_in_paper(df_data_subset.copy())
            result.update(stats)

        self.output_to_excel(results)


if __name__ == "__main__":
    from config import DATASET_DIR, OUTPUT_DIR
    _input_file1 = DATASET_DIR.joinpath("S2.1-学者基本信息.xlsx")
    _input_file2 = DATASET_DIR.joinpath("S0.1-原始数据表-249人学术生涯论文数据汇总.xlsx")
    ScholarDescription(_input_file1, _input_file2).calc()
