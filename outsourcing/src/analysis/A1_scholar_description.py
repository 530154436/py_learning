# -*- coding: utf-8 -*-
import re
import pandas as pd
from pathlib import Path
from dataclasses import dataclass, field
from dataclasses_json import config
from analysis import DataType
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
    avg_cits_per_paper_until_tw_0_end: float = field(metadata=config(field_name=f"{TIME_WINDOW_0_END}年之前论文篇均被引频次"))

    total_cits_10_years: int = field(metadata=config(field_name="10年论文总被引频次"))
    avg_cits_10_years: float = field(metadata=config(field_name="10年论文篇均被引频次"))
    total_corr_author_papers_10_years: int = field(metadata=config(field_name="10年通讯作者论文总数"))
    total_cits_corr_author_papers_10_years: int = field(metadata=config(field_name="10年通讯作者论文总被引频次"))
    avg_cits_corr_author_papers_10_years: float = field(metadata=config(field_name="10年通讯作者论文篇均被引频次"))

    career_patent_num: int = field(metadata=config(field_name="学者职业生涯专利总数"))
    career_patent_grant_num: int = field(metadata=config(field_name="学者职业生涯授权专利数量"))
    career_patent_first_inventor_patent_hum_10_years: int = field(metadata=config(field_name="职业生涯第一发明人授权专利数量"))
    patent_first_inventor_patent_hum_10_years: int = field(metadata=config(field_name="10年第一发明人授权专利数量"))

    career_patent_families_num: int = field(metadata=config(field_name="学者职业生涯专利族数量"))
    patent_families_num_10_years: int = field(metadata=config(field_name="10年专利族数量"))
    patent_citations_10_years: int = field(metadata=config(field_name="10年专利被引频次"))


class ScholarDescription(AbstractBase):
    __tbl_name__ = "A1-学者描述性统计"

    def __init__(self, basic_info_path: Path,
                 data_paper_path: Path, data_patent_path: Path):
        super().__init__()
        self.basic_info_path = basic_info_path
        self.data_paper_path = data_paper_path
        self.data_patent_path = data_patent_path

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
        mask = mask_10_year \
            & (
                 contains_in(df["Web of Science Index"], ["Conference Proceedings Citation Index - Science (CPCI-S)"]) \
                 & contains_in(df["Document Type"], ["Proceedings Paper"])
               ) \
            & (~contains_in(df["Web of Science Index"], ["Science Citation Index Expanded (SCI-EXPANDED)"]))
        total_meeting_pub_10_years = df[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"10年会议论文总发文量:", total_meeting_pub_10_years)

        # 9、10年预印本总发文量：统计Web of Science Index中的preprint，即预印本
        mask = mask_10_year \
               & contains_in(df["Web of Science Index"], ["preprint"])
        total_preprint_pub_10_years = df[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"10年预印本总发文量:", total_preprint_pub_10_years)

        # 10、2019年之前总发文量
        df_sub = df[df["Publication Year"] <= TIME_WINDOW_0_END]
        total_pub_until_tw_0_end = df_sub["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"{TIME_WINDOW_0_END}年之前总发文量:", total_pub_until_tw_0_end)

        # 11、2019年之前总被引频次
        sum_citations_per_paper = self.calc_citations_per_paper(df_sub, start_year=1900, end_year=TIME_WINDOW_0_END)
        total_cits_until_tw_0_end = sum_citations_per_paper.sum()
        print(f"{TIME_WINDOW_0_END}年之前总被引频次:", total_cits_until_tw_0_end)

        # 12、2019年之前篇均被引频次
        avg_cits_per_paper_until_tw_0_end = sum_citations_per_paper.mean()
        print(f"{TIME_WINDOW_0_END}年之前篇均被引频次:", avg_cits_per_paper_until_tw_0_end)

        # 13、10年论文总被引频次
        df_sub = df[(df["Publication Year"] >= TIME_WINDOW_0_START) & (df["Publication Year"] <= TIME_WINDOW_1_END)]
        sum_citations_per_paper = self.calc_citations_per_paper(df_sub, start_year=TIME_WINDOW_0_START, end_year=TIME_WINDOW_1_END)
        total_cits_10_years = sum_citations_per_paper.sum()
        print("10年论文总被引频次:", total_cits_10_years)
        
        # 14、10年论文篇均被引频次
        avg_cits_10_years = round(sum_citations_per_paper.mean(), ndigits=2)
        print("10年论文篇均被引频次:", avg_cits_10_years)

        # 15、10年通讯作者论文数
        mask_corr = (TIME_WINDOW_0_START <= df["Publication Year"]) & (df["Publication Year"] <= TIME_WINDOW_1_END) \
            & (df["is_corresponding_author(except for math)"] == 1) \
            & contains_in(df["Web of Science Index"],
                              values=["Conference Proceedings Citation Index - Science (CPCI-S)",
                                      "Science Citation Index Expanded (SCI-EXPANDED)",
                                      "preprint"])\
            & contains_in(df["Document Type"], ["Article", "Review", "Proceedings Paper", "preprint"])
        df_sub = df[mask_corr]
        total_corr_author_papers_10_years = df_sub["UT (Unique WOS ID)"].nunique(dropna=True)
        print("10年通讯作者论文数:", total_corr_author_papers_10_years)

        # 16、10年通讯作者论文总被引频次
        sum_citations_per_paper = self.calc_citations_per_paper(df_sub, start_year=TIME_WINDOW_0_START, end_year=TIME_WINDOW_1_END)
        total_cits_corr_author_papers_10_years = sum_citations_per_paper.sum()
        print("10年通讯作者论文数:", total_cits_corr_author_papers_10_years)

        # 17、10年通讯作者论文篇均被引
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

    def calc_one_in_patent(self, df: pd.DataFrame) -> dict:

        # 筛选时间窗口内数据，如 x-2024
        df = df.loc[df["申请年"] <= TIME_WINDOW_1_END]

        # 1、学者职业生涯专利总数
        career_patent_num = df["公开号"].nunique(dropna=True)
        print("学者职业生涯专利总数:", career_patent_num)

        # 2、学者职业生涯授权专利数量
        df_sub = df[df["专利类型（申请-0，授权-1）"] == 1]
        career_patent_grant_num = df_sub["公开号"].nunique(dropna=True)
        print("学者职业生涯授权专利数量:", career_patent_grant_num)

        # 3、职业生涯第一发明人授权专利数量
        mask = (df["申请年"] <= TIME_WINDOW_1_END) \
            & (df["第一发明人（是-1，否-0）"] == 1) \
            & (df["专利类型（申请-0，授权-1）"] == 1)
        career_patent_first_inventor_patent_hum_10_years = df[mask]["公开号"].nunique(dropna=True)
        print("职业生涯第一发明人授权专利数量:", career_patent_first_inventor_patent_hum_10_years)

        # 4、10年第一发明人授权专利数量
        mask = (TIME_WINDOW_0_START <= df["申请年"]) & (df["申请年"] <= TIME_WINDOW_1_END) \
            & (df["第一发明人（是-1，否-0）"] == 1) \
            & (df["专利类型（申请-0，授权-1）"] == 1)
        patent_first_inventor_patent_hum_10_years = df[mask]["公开号"].nunique(dropna=True)
        print("10年第一发明人授权专利数量:", patent_first_inventor_patent_hum_10_years)

        return dict(
            career_patent_num=career_patent_num,
            career_patent_grant_num=career_patent_grant_num,
            career_patent_first_inventor_patent_hum_10_years=career_patent_first_inventor_patent_hum_10_years,
            patent_first_inventor_patent_hum_10_years=patent_first_inventor_patent_hum_10_years
        )

    def calc_one_in_patent_famailies(self, df: pd.DataFrame) -> dict:

        # 筛选时间窗口内数据，如 x-2024
        df = df.loc[df["申请年"] <= TIME_WINDOW_1_END]

        # 1、学者职业生涯专利族数量
        career_patent_families_num: pd.DataFrame = df["公开号"].nunique(dropna=True)
        print("学者职业生涯专利族数量:", career_patent_families_num)

        # 2、10年专利族数量
        mask_10_years = (TIME_WINDOW_0_START <= df["申请年"]) & (df["申请年"] <= TIME_WINDOW_1_END)
        patent_families_num_10_years: pd.DataFrame = df[mask_10_years]["公开号"].nunique(dropna=True)
        print("10年专利族数量:", patent_families_num_10_years)

        # 3、10年专利被引频次
        df_sub = df[mask_10_years].drop_duplicates(subset=["公开号"])
        patent_citations_10_years = df_sub["施引专利计数 - DPCI"].fillna(0).sum()
        print("10年专利被引频次:", patent_citations_10_years)

        return dict(
            career_patent_families_num=career_patent_families_num,
            patent_families_num_10_years=patent_families_num_10_years,
            patent_citations_10_years=patent_citations_10_years,
        )

    def calc_by_data_type(self, data_type: str) -> pd.DataFrame:
        # 读取基础信息表和数据表
        df_basic_info = pd.read_excel(self.basic_info_path)
        if data_type == DataType.paper:
            df_data = pd.read_excel(self.data_paper_path)
        elif data_type == DataType.patent:
            df_data = pd.read_excel(self.data_patent_path)
        elif data_type == DataType.patent_families:
            df_data = pd.read_excel(self.data_patent_path, sheet_name="DWPI同族专利合并")
        else:
            raise ValueError("data_type must be 'paper' or 'patent'")

        print(f"计算 {data_type} 相关指标")
        print(df_basic_info.head())
        print(df_data.head())

        # 计算
        data = []
        for i, row in enumerate(df_basic_info.to_dict(orient="records"), start=1):
            _id = row["学者唯一ID"]
            name = row["姓名"]
            df_data_subset = df_data[df_data["姓名"] == name]
            print(f"{i:03d}/{df_basic_info.shape[0]}: "
                  f"学者唯一ID={_id}, 姓名={name}, "
                  f"任务类型={data_type}, 数据行数={df_data_subset.shape[0]}")

            result = {"id": _id, "name": name}
            if data_type == DataType.paper:
                metric = self.calc_one_in_paper(df_data_subset.copy())
            elif data_type == DataType.patent:
                metric = self.calc_one_in_patent(df_data_subset.copy())
            elif data_type == DataType.patent_families:
                metric = self.calc_one_in_patent_famailies(df_data_subset.copy())
            else:
                raise ValueError("data_type must be 'paper' or 'patent'、'patent_families'")
            result.update(metric)
            data.append(result)
        df = pd.DataFrame(data)
        df.drop_duplicates(subset=["id", "name"], inplace=True)  # 去重
        self.save_to_excel(df, save_file=f"{self.__tbl_name__}-{data_type}.xlsx")
        return df

    def calc(self):
        df_paper = self.calc_by_data_type(DataType.paper)
        df_patent = self.calc_by_data_type(DataType.patent)
        df_patent_families = self.calc_by_data_type(DataType.patent_families)
        # df_paper = pd.read_excel(OUTPUT_DIR.joinpath(f"{self.__tbl_name__}-{DataType.paper}.xlsx"))
        # df_patent = pd.read_excel(OUTPUT_DIR.joinpath(f"{self.__tbl_name__}-{DataType.patent}.xlsx"))
        # df_patent_families = pd.read_excel(OUTPUT_DIR.joinpath(f"{self.__tbl_name__}-{DataType.patent_families}.xlsx"))

        df_data = pd.merge(df_paper, df_patent, on=["id", "name"], how="inner")
        df_data = pd.merge(df_data, df_patent_families, on=["id", "name"], how="inner")

        self.export_to_excel(df_data, clazz=ScholarDescriptionEntity)


if __name__ == "__main__":
    from config import DATASET_DIR, OUTPUT_DIR
    _input_file1 = DATASET_DIR.joinpath("S2.1-学者基本信息.xlsx")
    _input_file2 = DATASET_DIR.joinpath("S0.1-原始数据表-249人学术生涯论文数据汇总.xlsx")
    _input_file3 = DATASET_DIR.joinpath("S0.2-原始数据表-249人学术生涯专利数据汇总.xlsx")
    ScholarDescription(_input_file1, data_paper_path=_input_file2, data_patent_path=_input_file3).calc()
