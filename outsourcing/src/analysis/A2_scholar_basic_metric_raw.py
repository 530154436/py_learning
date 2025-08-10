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


@dataclass
class ScholarBasicMetricRawEntity(ScholarIdGroupEntity):
    """
    学者描述信息（包含统计指标）
    """
    time_window: int = field(metadata=config(field_name="时间窗口（0=获奖前5年，1=获奖后5年）"))

    # 相关指标
    total_pub: int = field(metadata=config(field_name="总发文量", metadata={"description": "统计学者在时间窗口内发表论文总数"}))
    total_sci_pub: int = field(metadata=config(field_name="SCI论文数", metadata={"description": "统计学者在时间窗口内发表SCI论文数"}))
    total_meeting_pub: int = field(metadata=config(field_name="会议论文数", metadata={"description": "统计学者在时间窗口内发表会议论文数"}))
    top_10p_corr_paper_num: int = field(metadata=config(field_name="前10%高影响力期刊或会议通讯作者论文数量"))

    total_corresponding_author_papers: int = field(metadata=config(field_name="通讯作者论文数（A1）", metadata={"description": "学者在给定时间内作为通讯作者身份发表总论文数（SCI/会议/预印本）"}))
    total_corresponding_author_papers_no_pp: int = field(metadata=config(field_name="通讯作者论文数（不含预印本）", metadata={"description": "学者在给定时间内作为通讯作者身份发表总论文数（SCI/会议）"}))
    patent_families_num: int = field(metadata=config(field_name="专利族数量（A2）", metadata={"description": "学者在给定时间内拥有的DWPI同族专利数量"}))
    patent_first_inventor_patent_hum: int = field(metadata=config(field_name="第一发明人授权专利数量（A3）", metadata={"description": "学者在给定时间内作为第一发明人授权的发明专利数量"}))
    avg_citations_per_paper: float = field(metadata=config(field_name="论文篇均被引频次（B1）", metadata={"description": "通讯作者论文篇均被引频次"}))
    max_citations_single_paper: int = field(metadata=config(field_name="单篇最高被引频次（B2）", metadata={"description": "在给定时间窗口内累计总被引频次最高的通讯作者论文引用次数"}))
    top_10p_corr_paper_ratio: float = field(metadata=config(field_name="前10%高影响力期刊或会议通讯作者论文数量占比（B3）", metadata={"description": "各领域JCR前10%期刊或重要国际会议通讯作者论文数量占比"}))
    patent_citations: int = field(metadata=config(field_name="专利被引频次（B4）", metadata={"description": "指专利族截至数据采集时间的总被引用次数"}))


class ScholarBasicMetricRaw(AbstractBase):
    __tbl_name__ = f"A2-评价指标数据集-原始数据"

    def __init__(self, basic_info_path: Path,
                 data_paper_path: Path, data_patent_path: Path, **kwargs):
        super().__init__()
        self.basic_info_path = basic_info_path
        self.data_paper_path = data_paper_path
        self.data_patent_path = data_patent_path
        self.data_weight_path = kwargs.get("data_weight_path")

    def calc_one_in_paper(self, df: pd.DataFrame, start_year: int, end_year: int) -> dict:
        """
        计算论文相关基础指标
        """
        # 预处理
        df = self.preprocessing_paper_data(df)

        # 筛选时间窗口内数据，如2015-2019
        mask_time_window = (start_year <= df["Publication Year"]) & (df["Publication Year"] <= end_year)

        # 1、总发文量：统计学者在时间窗口内发表论文总数
        total_pub = df[mask_time_window]["UT (Unique WOS ID)"].nunique(dropna=True)
        print("总发文量:", total_pub)

        # 2、SCI论文数：统计学者在时间窗口内发表SCI论文数
        mask = mask_time_window \
            & contains_in(df["Web of Science Index"], ["Science Citation Index Expanded (SCI-EXPANDED)"]) \
            & contains_in(df["Document Type"], ["Article", "Review"])
        total_sci_pub = df[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
        print("SCI论文数:", total_sci_pub)

        # 3、会议论文数：统计学者在时间窗口内发表会议论文数
        mask = mask_time_window \
            & (
                  contains_in(df["Web of Science Index"], ["Conference Proceedings Citation Index - Science (CPCI-S)"]) \
                  & contains_in(df["Document Type"], ["Proceedings Paper"])
            ) \
            & (~contains_in(df["Web of Science Index"], ["Science Citation Index Expanded (SCI-EXPANDED)"]))
        total_meeting_pub = df[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
        print("会议论文数:", total_meeting_pub)

        # 4、通讯作者论文数（A1）：学者在给定时间内作为通讯作者身份发表总论文数（SCI/会议/预印本）
        mask_corr = mask_time_window \
            & (df["is_corresponding_author(except for math)"] == 1) \
            & contains_in(df["Web of Science Index"],
                          values=["Conference Proceedings Citation Index - Science (CPCI-S)",
                                  "Science Citation Index Expanded (SCI-EXPANDED)",
                                  "preprint"]) \
            & contains_in(df["Document Type"], ["Article", "Review", "Proceedings Paper", "preprint"])
        total_corresponding_author_papers = df[mask_corr]["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"通讯作者论文数（A1）：: {total_corresponding_author_papers}")

        # 5、通讯作者论文数（不含预印本）
        mask_corr1 = mask_time_window \
            & (df["is_corresponding_author(except for math)"] == 1) \
            & contains_in(df["Web of Science Index"],
                          values=["Conference Proceedings Citation Index - Science (CPCI-S)",
                                  "Science Citation Index Expanded (SCI-EXPANDED)"]) \
            & contains_in(df["Document Type"], ["Article", "Review", "Proceedings Paper", "preprint"])
        total_corresponding_author_papers_no_pp = df[mask_corr1]["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"通讯作者论文数（不含预印本）：: {total_corresponding_author_papers_no_pp}")

        # 6、前10%高影响力期刊或会议通讯作者论文数量
        # top_10p_corr_paper: int = field(metadata=config(field_name="前10%高影响力期刊或会议通讯作者论文数量"))
        mask = mask_corr \
               & (df["is_top_journal_confer（1=yes,0=no,preprint=preprint,other=null）"] == 1)
        top_10p_corr_paper_num = df[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"前10%高影响力期刊或会议通讯作者论文数量：: {top_10p_corr_paper_num}")

        # 7、论文篇均被引频次（B1）：通讯作者论文篇均被引频次（通讯作者论文定义同第4点）
        # 计算方式:
        # 前5年：2015、2016、2017、2018、2019，这五年求和；每篇被引用总数求和/发表论文数
        # 后5年：2020、2021、2022、2023、2024，这五年求和；每篇被引用总数求和/发表论文数
        df_sub = df[mask_corr]
        sum_citations_per_paper = self.calc_citations_per_paper(df_sub, start_year=start_year, end_year=end_year)
        avg_citations_per_paper = round(sum_citations_per_paper.mean(), ndigits=2)
        print(f"论文篇均被引频次（B1）: {avg_citations_per_paper}")

        # 8、单篇最高被引频次（B2）：在给定时间窗口内（5年）累计总被引频次最高的通讯作者论文引用次数（通讯作者论文定义同第4点）
        max_citations_single_paper = sum_citations_per_paper.max()
        print("单篇最高被引频次（B2）:", max_citations_single_paper)

        # 9、前10%高影响力期刊或会议通讯作者论文数量占比（B3）：各领域JCR前10%期刊或重要国际会议通讯作者论文数量占比
        # 根据is_corresponding_author(except for math)和is_top_journal_confer两个字段筛选出研究者作为通讯作者且发表在顶级期刊或会议上的论文。
        top_10p_corr_paper_ratio = 0
        if total_corresponding_author_papers > 0:
            top_10p_corr_paper_ratio = round(top_10p_corr_paper_num / total_corresponding_author_papers_no_pp, 3)
        print("前10%高影响力期刊或会议通讯作者论文数量/总论文数:", top_10p_corr_paper_num, total_corresponding_author_papers_no_pp)
        print("前10%高影响力期刊或会议通讯作者论文数量占比（B3）:", top_10p_corr_paper_ratio)

        return dict(
            total_pub=total_pub,
            total_sci_pub=total_sci_pub,
            total_meeting_pub=total_meeting_pub,
            top_10p_corr_paper_num=top_10p_corr_paper_num,
            total_corresponding_author_papers=total_corresponding_author_papers,
            total_corresponding_author_papers_no_pp=total_corresponding_author_papers_no_pp,
            avg_citations_per_paper=avg_citations_per_paper,
            max_citations_single_paper=0 if pd.isnull(max_citations_single_paper) else int(max_citations_single_paper),
            top_10p_corr_paper_ratio=top_10p_corr_paper_ratio,
        )

    def calc_one_in_patent(self, df: pd.DataFrame, start_year: int, end_year: int) -> dict:

        # 筛选时间窗口内数据，如2015-2019
        mask_time_window = (start_year <= df["申请年"]) & (df["申请年"] <= end_year)

        # 申请年：用于筛选给定时间内的专利（例如，获奖前5年或获奖后5年）。
        df_sub: pd.DataFrame = df.loc[mask_time_window]

        # 1、第一发明人授权专利数量（A3）：学者在给定时间内作为第一发明人授权的发明专利数量
        mask = (df_sub["第一发明人（是-1，否-0）"] == 1) \
            & (df_sub["专利类型（申请-0，授权-1）"] == 1)
        patent_first_inventor_patent_hum = df_sub[mask]["公开号"].nunique(dropna=True)
        print("第一发明人授权专利数量（A3）:", patent_first_inventor_patent_hum)

        return dict(
            patent_first_inventor_patent_hum=patent_first_inventor_patent_hum
        )

    def calc_one_in_patent_famailies(self, df: pd.DataFrame, start_year: int, end_year: int) -> dict:

        # 筛选时间窗口内数据，如2015-2019
        mask_time_window = (start_year <= df["申请年"]) & (df["申请年"] <= end_year)

        # 申请年：用于筛选给定时间内的专利（例如，获奖前5年或获奖后5年）。
        df_sub: pd.DataFrame = df.loc[mask_time_window]

        # 1、专利族数量（A2）：学者在给定时间内拥有的DWPI同族专利数量
        patent_families_num = df_sub["公开号"].nunique(dropna=True)
        print("专利族数量（A2）:", patent_families_num)

        # 2、专利被引次数（B4）：指专利族截至数据采集时间的总被引用次数
        df_sub = df[mask_time_window].drop_duplicates(subset=["公开号"])
        patent_citations = df_sub["施引专利计数 - DPCI"].fillna(0).sum()
        print("专利被引次数（B4）:", patent_citations)

        return dict(
            patent_families_num=patent_families_num,
            patent_citations=patent_citations
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

            # 时间窗口
            time_windows = [(0, (TIME_WINDOW_0_START, TIME_WINDOW_0_END)),
                            (1, (TIME_WINDOW_1_START, TIME_WINDOW_1_END))]
            for time_window, (start_year, end_year) in time_windows:
                result = {"id": _id, "name": name, "time_window": time_window}
                if data_type == DataType.paper:
                    metric = self.calc_one_in_paper(df_data_subset.copy(), start_year=start_year, end_year=end_year)
                elif data_type == DataType.patent:
                    metric = self.calc_one_in_patent(df_data_subset.copy(), start_year=start_year, end_year=end_year)
                elif data_type == DataType.patent_families:
                    metric = self.calc_one_in_patent_famailies(df_data_subset.copy(), start_year=start_year, end_year=end_year)
                else:
                    raise ValueError("data_type must be 'paper' or 'patent'")
                result.update(metric)
                data.append(result)
        df = pd.DataFrame(data)
        df.drop_duplicates(subset=["id", "name", "time_window"], inplace=True)  # 去重
        self.save_to_excel(df, save_file=f"{self.__tbl_name__}-{data_type}.xlsx")
        return df

    def calc(self):
        df_paper = self.calc_by_data_type(DataType.paper)
        df_patent = self.calc_by_data_type(DataType.patent)
        df_patent_families = self.calc_by_data_type(DataType.patent_families)
        # df_paper = pd.read_excel(OUTPUT_DIR.joinpath(f"{self.__tbl_name__}-{DataType.paper}.xlsx"))
        # df_patent = pd.read_excel(OUTPUT_DIR.joinpath(f"{self.__tbl_name__}-{DataType.patent}.xlsx"))
        # df_patent_families = pd.read_excel(OUTPUT_DIR.joinpath(f"{self.__tbl_name__}-{DataType.patent_families}.xlsx"))
        df_data = pd.merge(df_paper, df_patent, on=["id", "name", "time_window"], how="inner")
        df_data = pd.merge(df_data, df_patent_families, on=["id", "name", "time_window"], how="inner")

        self.export_to_excel(df_data, clazz=ScholarBasicMetricRawEntity)


if __name__ == "__main__":
    _input_file0 = DATASET_DIR.joinpath("S2.1-学者基本信息.xlsx")
    _input_file1 = DATASET_DIR.joinpath("S0.1-原始数据表-249人学术生涯论文数据汇总.xlsx")
    _input_file2 = DATASET_DIR.joinpath("S0.2-原始数据表-249人学术生涯专利数据汇总.xlsx")
    _input_file3 = DATASET_DIR.joinpath("S2.3-指标计算权重值.xlsx")
    _metric = ScholarBasicMetricRaw(_input_file0, data_paper_path=_input_file1,
                                    data_patent_path=_input_file2, data_weight_path=_input_file3)
    _metric.calc()
