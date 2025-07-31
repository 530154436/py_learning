# -*- coding: utf-8 -*-
import re
import pandas as pd
from pathlib import Path
from dataclasses import dataclass, field
from dataclasses_json import config
from config import TIME_WINDOW_1_END, TIME_WINDOW_0_END, TIME_WINDOW_0_START, CURRENT_YEAR
from analysis.abstract_base import AbstractBase
from analysis.scholar_base import ScholarIdGroupEntity
from utils.pd_common_util import contains_in


@dataclass
class ScholarDescriptionEntity(ScholarIdGroupEntity):
    """
    学者描述信息（包含统计指标）
    """
    # 统计类指标
    career_length: int = field(metadata=config(field_name=f"学者职业生涯长度"))
    active_years: int = field(metadata=config(field_name="学者活跃年数"))
    career_total_pub: int = field(metadata=config(field_name="学者职业生涯总发文量"))
    # career_total_sci_pub: int = field(metadata=config(field_name="学者职业生涯SCI论文总发文量"))
    # career_total_meeting_pub: int = field(metadata=config(field_name="学者职业生涯会议论文总发文量"))
    h_index_tw_0_years: int = field(metadata=config(field_name=f"{TIME_WINDOW_0_END}年学者H指数（截止到{TIME_WINDOW_0_END}年）"))
    h_index_tw_1_years: int = field(metadata=config(field_name=f"{TIME_WINDOW_1_END}年学者H指数（截止到{TIME_WINDOW_1_END}年）"))
    total_pub_10_years: int = field(metadata=config(field_name="10年总发文量"))
    total_sci_pub_10_years: int = field(metadata=config(field_name="10年SCI论文总发文量"))
    total_meeting_pub_10_years: int = field(metadata=config(field_name="10年会议论文总发文量"))
    total_preprint_pub_10_years: int = field(metadata=config(field_name="10年预印本总发文量"))
    total_pub_until_tw_0_end: int = field(metadata=config(field_name=f"{TIME_WINDOW_0_END}年之前总发文量"))
    total_cits_until_tw_0_end: int = field(metadata=config(field_name=f"{TIME_WINDOW_0_END}年之前论文总被引频次"))
    avg_cits_per_paper_until_tw_0_end: int = field(metadata=config(field_name=f"{TIME_WINDOW_0_END}年之前论文篇均被引频次"))

    total_cits_10_years: int = field(metadata=config(field_name="10年论文总被引频次"))
    avg_cits_10_years: float = field(metadata=config(field_name="10年论文篇均被引频次"))
    total_corr_author_papers_10_years: int = field(metadata=config(field_name="10年通讯作者论文总数"))
    total_cits_corr_author_papers_10_years: int = field(metadata=config(field_name="10年通讯作者论文总被引频次"))
    avg_cits_corr_author_papers_10_years: float = field(metadata=config(field_name="10年通讯作者论文篇均被引频次"))


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
        sum_citations_per_paper = self.calc_citations_per_paper(df, start_year=1900, end_year=TIME_WINDOW_0_END)
        h_index_tw_0_years = self.calc_h_index(sum_citations_per_paper.tolist())
        print(f"学者H指数：截止到{TIME_WINDOW_0_END}年:", h_index_tw_0_years)

        # 5、学者H指数：截止到2024年
        sum_citations_per_paper = self.calc_citations_per_paper(df, start_year=1900, end_year=TIME_WINDOW_1_END)
        h_index_tw_1_years = self.calc_h_index(sum_citations_per_paper.tolist())
        print(f"学者H指数：截止到{TIME_WINDOW_1_END}年:", h_index_tw_1_years)

        # 6、10年总发文量
        mask_10_year = (TIME_WINDOW_0_START <= df["Publication Year"]) & \
                       (df["Publication Year"] <= TIME_WINDOW_1_END)
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

        # 10、2019年之前总发文量
        mask = df["Publication Year"] <= TIME_WINDOW_0_END
        total_pub_until_tw_0_end = df[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"{TIME_WINDOW_0_END}年之前总发文量:", total_pub_until_tw_0_end)

        # 11、2019年之前总被引频次
        sum_citations_per_paper = self.calc_citations_per_paper(df, start_year=1900, end_year=TIME_WINDOW_0_END)
        total_cits_until_tw_0_end = sum_citations_per_paper.sum()
        print(f"{TIME_WINDOW_0_END}年之前总被引频次:", total_cits_until_tw_0_end)

        # 12、2019年之前篇均被引频次
        sum_citations_per_paper = self.calc_citations_per_paper(df, start_year=1900, end_year=TIME_WINDOW_0_END)
        avg_cits_per_paper_until_tw_0_end = round(sum_citations_per_paper.mean(), ndigits=2)
        print(f"{TIME_WINDOW_0_END}年之前篇均被引频次:", avg_cits_per_paper_until_tw_0_end)

        # 13、10年论文总被引频次
        sum_citations_per_paper = self.calc_citations_per_paper(df, start_year=TIME_WINDOW_0_END, end_year=TIME_WINDOW_1_END)
        total_cits_10_years = sum_citations_per_paper.sum()
        print("10年论文总被引频次:", total_cits_10_years)
        
        # 14、10年论文篇均被引频次
        sum_citations_per_paper = self.calc_citations_per_paper(df, start_year=TIME_WINDOW_0_END, end_year=TIME_WINDOW_1_END)
        avg_cits_10_years = round(sum_citations_per_paper.mean(), ndigits=2)
        print("10年论文篇均被引频次:", avg_cits_10_years)

        # 15、10年通讯作者论文数
        mask_corr = (TIME_WINDOW_0_END <= df["Publication Year"]) & (df["Publication Year"] <= TIME_WINDOW_1_END) \
            & (df["is_corresponding_author(except for math)"] == 1) \
            & contains_in(df["Web of Science Index"],
                              values=["Conference Proceedings Citation Index - Science (CPCI-S)",
                                      "Science Citation Index Expanded (SCI-EXPANDED)",
                                      "preprint"])
            # & contains_in(df["Document Type"], ["Article", "Review"])
        df_sub = df[mask_corr]
        total_corr_author_papers_10_years = df_sub["UT (Unique WOS ID)"].nunique(dropna=True)
        print("10年通讯作者论文数:", total_corr_author_papers_10_years)

        # 16、10年通讯作者论文总被引频次
        sum_citations_per_paper = self.calc_citations_per_paper(df_sub, start_year=TIME_WINDOW_0_END, end_year=TIME_WINDOW_1_END)
        total_cits_corr_author_papers_10_years = sum_citations_per_paper.sum()
        print("10年通讯作者论文数:", total_cits_corr_author_papers_10_years)

        # 17、10年通讯作者论文篇均被引
        sum_citations_per_paper = self.calc_citations_per_paper(df_sub, start_year=TIME_WINDOW_0_END, end_year=TIME_WINDOW_1_END)
        avg_cits_corr_author_papers_10_years = round(sum_citations_per_paper.mean(), ndigits=2)
        print("10年通讯作者论文篇均被引:", avg_cits_corr_author_papers_10_years)

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
            total_pub_until_tw_0_end=total_pub_until_tw_0_end,
            total_cits_until_tw_0_end=total_cits_until_tw_0_end,
            avg_cits_per_paper_until_tw_0_end=avg_cits_per_paper_until_tw_0_end,
            total_cits_10_years=total_cits_10_years,
            avg_cits_10_years=avg_cits_10_years,
            total_corr_author_papers_10_years=total_corr_author_papers_10_years,
            total_cits_corr_author_papers_10_years=total_cits_corr_author_papers_10_years,
            avg_cits_corr_author_papers_10_years=avg_cits_corr_author_papers_10_years,
        )

    def calc(self):

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
            df_data_subset = df_data[df_data["姓名"] == name]
            print(f"{i:03d}/{df_basic_info.shape[0]}: 学者唯一ID={_id}, 姓名={name}, 数据行数={df_data_subset.shape[0]}")

            result: dict = self.calc_one_in_paper(df_data_subset.copy())
            row.update(result)
            results.append(row)
        self.export_to_excel(results, clazz=ScholarDescriptionEntity, fill_na=0)


if __name__ == "__main__":
    from config import DATASET_DIR, OUTPUT_DIR
    _input_file1 = DATASET_DIR.joinpath("S2.1-学者基本信息.xlsx")
    _input_file2 = DATASET_DIR.joinpath("S0.1-原始数据表-249人学术生涯论文数据汇总.xlsx")
    ScholarDescription(_input_file1, _input_file2).calc()
