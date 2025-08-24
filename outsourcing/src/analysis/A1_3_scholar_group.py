# -*- coding: utf-8 -*-
from typing import List
import pandas as pd
from collections import OrderedDict
from config import TIME_WINDOW_1_END, TIME_WINDOW_0_START
from analysis.abstract_base import AbstractBase


class ScholarAcademicAnnualChange(AbstractBase):
    __tbl_name__ = "A1.3-群体学术能力年度趋势"

    def __init__(self,):
        super().__init__()

    @staticmethod
    def clac_common_paper_year(paper_year_list: List[str], ascending:bool = True):
        common_paper_year = set()
        for paper_year in paper_year_list:
            paper_year_set = set(paper_year.split(";"))
            if len(common_paper_year) == 0:
                common_paper_year = paper_year_set
            common_paper_year &= paper_year_set
        common_paper_year_list = list(common_paper_year)
        if ascending:
            common_paper_year_list.sort()
        return "、".join(i for i in common_paper_year_list)

    def calc(self):
        """ 群体（获奖人、对照学者）特征
        """
        df_1 = pd.read_excel(OUTPUT_DIR.joinpath("A1-学者描述性统计.xlsx"))
        df_2 = pd.read_excel(OUTPUT_DIR.joinpath("A1.1-学者学术能力年度趋势.xlsx"))
        df = pd.merge(df_1, df_2, on=['学者唯一ID', '姓名', '学者类型（获奖人=1，0=对照学者）'], how="inner")
        # print(df)
        # assert df.shape[0] == 249

        data = []
        years = range(TIME_WINDOW_0_START, TIME_WINDOW_1_END + 1)
        for scholar_type in [1, 0]:
            df_scholar_type = df[df["学者类型（获奖人=1，0=对照学者）"] == scholar_type]
            result = OrderedDict({
                "学者类型（获奖人=1，0=对照学者）": scholar_type,
                "学者人数": df_scholar_type["姓名"].nunique(),
                "职业生涯最早发表年份": df_scholar_type["首篇论文发表年份"].min(),
                "10年最早发表年份": df_scholar_type["10年首篇论文发表年份"].min(),
                "10年共同年份范围": self.clac_common_paper_year(df_scholar_type["10年论文发表年份集合"]),
            })
            for year in years:
                year_total_pub = df_scholar_type[f"{year}年度发文总量"].sum()
                result[f"{year}年度发文总量"] = year_total_pub

                # 被引次数（累计）
                year_total_cits = df_scholar_type[f"{year}年度总被引次数（截止{TIME_WINDOW_1_END}）"].sum()
                result[f"{year}年度总被引次数（截止{TIME_WINDOW_1_END}）"] = year_total_cits
                result[f"{year}年度篇均被引频次（截止{TIME_WINDOW_1_END}）"] = round(year_total_cits / year_total_pub, 2)

                year_cited_accum = df_scholar_type[f"{year}年度引用累积年数"].sum()
                result[f"{year}年度引用累积年数"] = year_cited_accum
                result[f"群体{year}年均引用率"] = round(year_total_cits / year_cited_accum, 2)

                # 被引次数（当年）
                # （某年）年度当年篇均被引频次=（某年）当年被引次数/（某年）年度发文总量
                year_total_cits_now = df_scholar_type[f"{year}年度当年被引次数"].sum()
                result[f"{year}年度当年被引次数"] = year_total_cits_now
                result[f"{year}年度当年篇均被引频次"] = round(year_total_cits_now / year_total_pub, 2)

                # 滑动窗口
                pre5_year_total_pub = df_scholar_type[f"近5年发表论文{year}年发文总量"].sum()
                pre5_year_total_cits = df_scholar_type[f"近5年发表论文{year}年累计总被引次数"].sum()
                result[f"近5年发表论文{year}年发文总量"] = pre5_year_total_pub
                result[f"近5年发表论文{year}年累计总被引次数"] = pre5_year_total_cits
                result[f"群体{year}ACPP"] = round(pre5_year_total_cits / pre5_year_total_pub, 2)

                # 高影响力论文占比
                year_total_top_pub = df_scholar_type[f"{year}年顶刊/会议论文数"].sum()
                year_total_pub_no_pp = df_scholar_type[f"{year}年度发文总量（不含预印本）"].sum()
                result[f"{year}年顶刊/会议论文数"] = year_total_top_pub
                result[f"{year}年度发文总量（不含预印本）"] = year_total_pub_no_pp
                result[f"{year}年度高影响力论文占比"] = round(year_total_top_pub / year_total_pub_no_pp, ndigits=2) if year_total_pub_no_pp > 0 else 0

                result[f"{year}年度专利族数量"] = df_scholar_type[f"{year}年度专利族数量"].sum()

            data.append(result)
        df_res = pd.DataFrame(data)
        print(df_res)
        self.save_to_excel(df_res, save_file=self.__tbl_name__ + ".xlsx")




if __name__ == "__main__":
    from config import DATASET_DIR, OUTPUT_DIR
    _object = ScholarAcademicAnnualChange()
    _object.calc()
