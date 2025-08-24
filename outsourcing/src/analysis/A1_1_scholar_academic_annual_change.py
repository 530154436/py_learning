# -*- coding: utf-8 -*-
import pandas as pd
from collections import OrderedDict
from pathlib import Path
from config import TIME_WINDOW_1_END, TIME_WINDOW_0_START
from analysis.abstract_base import AbstractBase
from utils.pd_common_util import contains_in


class ScholarAcademicAnnualChange(AbstractBase):
    __tbl_name__ = "A1.1-学者学术能力年度趋势"

    def __init__(self, basic_info_path: Path,
                 data_paper_path: Path, data_patent_path: Path):
        super().__init__()
        self.basic_info_path = basic_info_path
        self.data_paper_path = data_paper_path
        self.data_patent_path = data_patent_path

    def calc_one_in_paper(self, df: pd.DataFrame, start_year: int, end_year: int) -> dict:
        """
        一个学者的论文数据年度趋势
        """
        years = range(start_year, end_year + 1)
        result = OrderedDict()
        for year in years:

            # 目标年份发表的论文
            df_year = df[df["Publication Year"] == year]

            # xxxx年度发文量
            year_total_pub = df_year["UT (Unique WOS ID)"].nunique(dropna=True)
            result[f"{year}年度发文量"] = year_total_pub

            # xxxx年度发文量（不含预印本）
            mask = contains_in(df_year["Web of Science Index"],
                               values=["Conference Proceedings Citation Index - Science (CPCI-S)",
                                       "Science Citation Index Expanded (SCI-EXPANDED)"]) \
                   & contains_in(df_year["Document Type"], ["Article", "Review", "Proceedings Paper", "preprint"])
            year_total_pub_no_pp = df_year[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
            result[f"{year}年度发文量（不含预印本）"] = year_total_pub_no_pp

            # xxxx年顶刊/会议论文数
            mask = df_year["is_top_journal_confer（1=yes,0=no,preprint=preprint,other=null）"] == 1
            year_total_top_pub = df_year[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
            result[f"{year}年顶刊/会议论文数"] = year_total_top_pub

            # xxx年度总被引次数（截止2024）：统计目标年份发表的论文，从发表到2024年累积的引用次数。
            sum_citations_per_paper = self.calc_citations_per_paper(df_year, start_year=year, end_year=TIME_WINDOW_1_END)
            year_total_cits = int(sum_citations_per_paper.sum())
            result[f"{year}年度总被引次数（截止2024）"] = year_total_cits

            # xxxx年度引用累积年数（截止2024）=2024-发表年份
            # xxxx年度年均引用率（截止2024）=年度总引用次数/年度引用累计年数总和
            result[f"{year}年度引用累积年数"] = 2024 - year + 1
            result[f"{year}年度年均引用率（截止2024）"] = round(year_total_cits/(2024 - year + 1), ndigits=2)

            # xxxx年度高影响力论文占比 = (xxxx年顶刊/会议论文数) / (xxxx年度发文总量不含预印本）)
            year_total_top_pub_ratio = year_total_top_pub / year_total_pub_no_pp if year_total_pub_no_pp else 0
            result[f"{year}年度高影响力论文占比"] = f"{int(round(year_total_top_pub_ratio, ndigits=2)) * 100}%"
            # print(result)

        return result

    def calc_one_in_patent(self, df: pd.DataFrame, start_year: int, end_year: int) -> dict:
        """
        一个学者的专利数据年度趋势
        """
        years = range(start_year, end_year + 1)
        result = OrderedDict()
        for year in years:
            # 指定申请年的专利数据
            df_year: pd.DataFrame = df[df["申请年"] == year]

            # xxxx年度专利族数量：学者在给定时间内拥有的DWPI同族专利数量
            year_patent_families_num = df_year["公开号"].nunique(dropna=True)
            result[f"{year}年度专利族数量"] = year_patent_families_num
        return result

    def calc_paper(self) -> pd.DataFrame:
        """
        论文数据年度趋势
        """
        df_basic_info = pd.read_excel(self.basic_info_path)
        df_paper = pd.read_excel(self.data_paper_path)
        df_paper = self.preprocessing_paper_data(df_paper)
        data = []
        for i, row in enumerate(df_basic_info.to_dict(orient="records"), start=1):
            _id, name = row["学者唯一ID"], row["姓名"]
            df = df_paper[df_paper["姓名"] == name]
            print(f"{i:03d}/{df_basic_info.shape[0]}: 学者唯一ID={_id}, 姓名={name}, 论文数量={df.shape[0]}")
            result = OrderedDict({"学者唯一ID": _id, "姓名": name})
            index = self.calc_one_in_paper(df, start_year=TIME_WINDOW_0_START, end_year=TIME_WINDOW_1_END)
            result.update(index)
            data.append(result)
        return pd.DataFrame(data)

    def calc_patent(self) -> pd.DataFrame:
        """
        专利数据年度趋势
        """
        df_basic_info = pd.read_excel(self.basic_info_path)
        df_patent = pd.read_excel(self.data_patent_path)
        data = []
        for i, row in enumerate(df_basic_info.to_dict(orient="records"), start=1):
            _id, name = row["学者唯一ID"], row["姓名"]
            df = df_patent[df_patent["姓名"] == name]
            print(f"{i:03d}/{df_basic_info.shape[0]}: 学者唯一ID={_id}, 姓名={name}, 专利数量={df.shape[0]}")
            result = {"学者唯一ID": _id, "姓名": name}
            index = self.calc_one_in_patent(df, start_year=TIME_WINDOW_0_START, end_year=TIME_WINDOW_1_END)
            result.update(index)
            data.append(result)
        return pd.DataFrame(data)

    def calc(self):
        df_paper = self.calc_paper()
        df_patent = self.calc_patent()
        df = pd.merge(df_paper, df_patent, how="inner", on=["学者唯一ID", "姓名"])
        self.save_to_excel(df)


if __name__ == "__main__":
    from config import DATASET_DIR, OUTPUT_DIR
    _input_file1 = DATASET_DIR.joinpath("S2.1-学者基本信息.xlsx")
    _input_file2 = DATASET_DIR.joinpath("S0.1-原始数据表-249人学术生涯论文数据汇总.xlsx")
    _input_file3 = DATASET_DIR.joinpath("S0.2-原始数据表-249人学术生涯专利数据汇总.xlsx")
    ScholarAcademicAnnualChange(_input_file1, data_paper_path=_input_file2, data_patent_path=_input_file3).calc()
