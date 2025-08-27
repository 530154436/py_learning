# -*- coding: utf-8 -*-
import pandas as pd
from collections import OrderedDict
from pathlib import Path
from config import TIME_WINDOW_1_END, TIME_WINDOW_0_START
from analysis.abstract_base import AbstractBase
from utils.pd_common_util import contains_in


class ScholarAcademicAnnualChange(AbstractBase):
    __tbl_name__ = "A1.1-学者学术能力年度趋势"
    __tbl_name_2__ = "A1.2-学者学术能力年度趋势-年维度"

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

            # xxxx年度发文量：在目标年份内发表的论文总数
            # 例如“2015年度发文总量”为学者在“2015”年发表的论文总数
            year_total_pub = df_year["UT (Unique WOS ID)"].nunique(dropna=True)
            result[f"{year}发文总量"] = year_total_pub

            # xxxx年度发文量（不含预印本）
            mask = contains_in(df_year["Web of Science Index"],
                               values=["Conference Proceedings Citation Index - Science (CPCI-S)",
                                       "Science Citation Index Expanded (SCI-EXPANDED)"]) \
                   & contains_in(df_year["Document Type"], ["Article", "Review", "Proceedings Paper", "preprint"])
            year_total_pub_no_pp = df_year[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
            result[f"{year}发文总量（不含预印本）"] = year_total_pub_no_pp

            # xxxx年顶刊/会议论文数
            mask = df_year["is_top_journal_confer（1=yes,0=no,preprint=preprint,other=null）"] == 1
            year_total_top_pub = df_year[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
            result[f"{year}顶刊/会议论文数"] = year_total_top_pub

            # xxxx年度高影响力论文占比 = (xxxx年顶刊/会议论文数) / (xxxx年度发文总量不含预印本）)
            year_total_top_pub_ratio = round(year_total_top_pub / year_total_pub_no_pp, ndigits=2) if year_total_pub_no_pp > 0 else 0
            result[f"{year}高影响力论文占比（%）"] = int(year_total_top_pub_ratio * 100)

            # xxx年度总被引次数（截止2024）：统计目标年份发表的论文，从发表到2024年累积的引用次数。
            sum_citations_per_paper = self.calc_citations_per_paper(df_year, start_year=year, end_year=TIME_WINDOW_1_END)
            year_total_cits = int(sum_citations_per_paper.sum())
            result[f"{year}总被引次数（截止{TIME_WINDOW_1_END}）"] = year_total_cits

            # xxx年度篇均被引频次（截止2024）：统计目标年份发表的论文，从发表到2024年的篇均引用次数。
            result[f"{year}篇均被引频次（截止{TIME_WINDOW_1_END}）"] =  round(sum_citations_per_paper.mean(), 2)

            # xxxx年度篇均暴露年数（截止2024）= 2024 - 发表年份 + 1
            # xxxx年度年均引用率（截止2024）=年度总被引次数（截止2024）/ 年度引用累积年数（截止2024）
            year_expose = (TIME_WINDOW_1_END - year + 1) * year_total_pub
            result[f"{year}总暴露年数（截止{TIME_WINDOW_1_END}）"] = year_expose
            result[f"{year}年均引用率（截止{TIME_WINDOW_1_END}）"] = round(year_total_cits/year_expose, ndigits=2) if year_expose > 0 else 0

            # xxxx年度当年被引次数：目标年份内发表的论文在同年获得的引用总次数
            # 例如：2015年度当年被引次数：学者在2015年发表的论文在2015年获得的总被引频次
            sum_citations_per_paper = self.calc_citations_per_paper(df_year, start_year=year, end_year=year)
            year_total_cits_now = int(sum_citations_per_paper.sum())
            result[f"{year}当年总被引次数"] = year_total_cits_now

            # （某年）年度当年篇均被引频次=（某年）当年被引次数/（某年）年度发文总量
            year_avg_cits_now = round(sum_citations_per_paper.mean(), 2)
            result[f"{year}当年篇均被引频次"] = year_avg_cits_now

            # ----------------------------------------------------------------------------
            # 滑动窗口计算：ACPP
            # 目标年份：计算某年（如2020年）的ACPP
            # 论文纳入范围：发表于该年前5年内（含当年）的论文
            # 论文发表年∈[y−4,y]，y为目标年份
            # 被引时间点：截至目标年份年底的被引频次
            # 例如，2016年ACPP = Σ(2012-2016年发表论文在2016年的总被引) / Σ(2012-2016年发文量)
            # ----------------------------------------------------------------------------
            # [y−4,y]年发表的论文
            df_pre5_year = df[(year-4 <= df["Publication Year"]) & (df["Publication Year"] <= year)]

            # 近5年发表论文2015年发文总量
            pre5_year_total_pub = df_pre5_year["UT (Unique WOS ID)"].nunique(dropna=True)
            result[f"{year}发文总量（5年时间窗口）"] = pre5_year_total_pub

            # 近5年发表论文2015年累积暴露年数
            pre5_year_expose = df_pre5_year["Publication Year"].apply(lambda x: year - x + 1)
            pre5_year_expose_sum = int(pre5_year_expose.sum())
            result[f"{year}总暴露年数（5年时间窗口）"] = pre5_year_expose_sum

            # 近5年发表论文2015年累计总被引次数
            sum_citations_per_paper = self.calc_citations_per_paper(df_pre5_year, start_year=year-4, end_year=year)
            pre5_year_total_cits = int(sum_citations_per_paper.sum())
            result[f"{year}总被引次数（5年时间窗口）"] = pre5_year_total_cits

            # 篇均被引频次（5年时间窗口）
            pre5_year_acpp = pre5_year_total_cits / pre5_year_total_pub if pre5_year_total_pub > 0 else 0
            result[f"{year}篇均被引频次（5年时间窗口）"] = round(pre5_year_acpp, ndigits=2)

            # 年均引用率（5年时间窗口）
            result[f"{year}年均引用率（5年时间窗口）"] = round(pre5_year_total_cits / pre5_year_expose_sum, ndigits=2) if pre5_year_expose_sum > 0 else 0

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
            result[f"{year}专利族数量"] = year_patent_families_num
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
            _id, name, scholar_type = row["学者唯一ID"], row["姓名"], row["学者类型（获奖人=1，0=对照学者）"]
            df = df_paper[df_paper["姓名"] == name]
            print(f"{i:03d}/{df_basic_info.shape[0]}: 学者唯一ID={_id}, 姓名={name}, 论文数量={df.shape[0]}")
            result = OrderedDict({"学者唯一ID": _id, "姓名": name, "学者类型（获奖人=1，0=对照学者）": scholar_type})
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
            _id, name, scholar_type = row["学者唯一ID"], row["姓名"], row["学者类型（获奖人=1，0=对照学者）"]
            df = df_patent[df_patent["姓名"] == name]
            print(f"{i:03d}/{df_basic_info.shape[0]}: 学者唯一ID={_id}, 姓名={name}, 专利数量={df.shape[0]}")
            result = OrderedDict({"学者唯一ID": _id, "姓名": name, "学者类型（获奖人=1，0=对照学者）": scholar_type})
            index = self.calc_one_in_patent(df, start_year=TIME_WINDOW_0_START, end_year=TIME_WINDOW_1_END)
            result.update(index)
            data.append(result)
        return pd.DataFrame(data)

    def calc_a1_1(self):
        df_paper = self.calc_paper()
        df_patent = self.calc_patent()
        df = pd.merge(df_paper, df_patent, how="inner", on=["学者唯一ID", "姓名", "学者类型（获奖人=1，0=对照学者）"])
        self.save_to_excel(df, save_file=self.__tbl_name__ + ".xlsx")

    def calc_a1_2(self):
        """ 宽表转长表（或称“数据透视”）
        """
        df = pd.read_excel(OUTPUT_DIR.joinpath(self.__tbl_name__ + ".xlsx"))
        id_vars = ['学者唯一ID', '姓名', '学者类型（获奖人=1，0=对照学者）']
        cols_to_transform = [col for col in df.columns if col not in id_vars]
        # 熔化数据，将所有年度列转换为长格式
        df_melted = df.melt(
            id_vars=id_vars,  # 保持不变的列
            value_vars=cols_to_transform,  # 要转换的列
            var_name='original_column',  # 熔化后，原列名所在的列名
            value_name='指标值'  # 熔化后，值所在的列名
        )
        # 提取年份：匹配开头的4位数字
        df_melted['年份'] = df_melted['original_column'].str.extract(r'(\d{4})')
        # 提取指标名称 (去掉年份和"年度"/"年")
        df_melted['指标'] = df_melted['original_column'].str.replace(r'^\d{4}', '', regex=True)

        # 使用 pivot 将 '指标' 列展开为多个列，pivot 的 index 是 ['姓名', '年份'], columns 是 '指标', values 是 '指标值'
        result_df = df_melted.pivot_table(
            index=['学者唯一ID', '姓名', '学者类型（获奖人=1，0=对照学者）', '年份'],  # 多级索引
            columns='指标',
            values='指标值',
            aggfunc='first'  # 因为每个组合唯一，用 first 即可
        ).reset_index()  # 将索引变回普通列

        # 清理列名 (pivot 后列名会变成 MultiIndex，我们需要扁平化)
        # 对于非 MultiIndex，这步可能不需要，但为了保险
        result_df.columns.name = None  # 移除列级别的名称
        # 按 学者唯一ID 和 年份 排序
        result_df = result_df.sort_values(['学者唯一ID', '姓名', '年份']).reset_index(drop=True)

        self.save_to_excel(result_df, save_file=self.__tbl_name_2__ + ".xlsx")


if __name__ == "__main__":
    from config import DATASET_DIR, OUTPUT_DIR
    _input_file1 = DATASET_DIR.joinpath("S2.1-学者基本信息.xlsx")
    _input_file2 = DATASET_DIR.joinpath("S0.1-原始数据表-249人学术生涯论文数据汇总.xlsx")
    _input_file3 = DATASET_DIR.joinpath("S0.2-原始数据表-249人学术生涯专利数据汇总.xlsx")
    _object = ScholarAcademicAnnualChange(_input_file1, data_paper_path=_input_file2, data_patent_path=_input_file3)
    _object.calc_a1_1()
    _object.calc_a1_2()
