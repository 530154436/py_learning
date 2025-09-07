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
            num_scholar = df_scholar_type["姓名"].nunique()
            result = OrderedDict({
                "学者类型（获奖人=1，0=对照学者）": scholar_type,
                "学者人数": df_scholar_type["姓名"].nunique(),
                "职业生涯最早发表年份": df_scholar_type["首篇论文发表年份"].min(),
                "10年最早发表年份": df_scholar_type["10年首篇论文发表年份"].min(),
                "10年共同年份范围": self.clac_common_paper_year(df_scholar_type["10年论文发表年份集合"]),
            })
            for year in years:
                year_total_pub = df_scholar_type[f"{year}发文总量"].sum()
                result[f"{year}发文总量"] = year_total_pub
                result[f"{year}平均发文量/篇"] = round(year_total_pub / num_scholar, 2)

                # 总被引次数（累计）
                year_total_cits = df_scholar_type[f"{year}总被引次数（截止{TIME_WINDOW_1_END}）"].sum()
                result[f"{year}总被引次数（截止{TIME_WINDOW_1_END}）"] = year_total_cits
                result[f"{year}篇均被引频次（截止{TIME_WINDOW_1_END}）"] = round(year_total_cits / year_total_pub, 2)

                # 被引次数（当年）
                # （某年）年度当年篇均被引频次=（某年）当年被引次数/（某年）年度发文总量
                year_total_cits_now = df_scholar_type[f"{year}当年总被引次数"].sum()
                result[f"{year}当年总被引次数"] = year_total_cits_now
                result[f"{year}当年篇均被引频次"] = round(year_total_cits_now / year_total_pub, 2)

                # 年度引用率
                year_expose = (TIME_WINDOW_1_END - year + 1) * year_total_pub
                result[f"{year}总暴露年数（截止{TIME_WINDOW_1_END}）"] = year_expose
                result[f"{year}年均引用率（截止{TIME_WINDOW_1_END}）"] = round(year_total_cits / year_expose, 2)

                # 滑动窗口
                pre5_year_total_pub = df_scholar_type[f"{year}发文总量（5年时间窗口）"].sum()
                pre5_year_total_expose = df_scholar_type[f"{year}总暴露年数（5年时间窗口）"].sum()
                pre5_year_total_cits = df_scholar_type[f"{year}总被引次数（5年时间窗口）"].sum()
                result[f"{year}发文总量（5年时间窗口）"] = pre5_year_total_pub
                result[f"{year}总暴露年数（5年时间窗口）"] = pre5_year_total_expose
                result[f"{year}总被引次数（5年时间窗口）"] = pre5_year_total_cits
                result[f"{year}篇均被引频次（5年时间窗口）"] = round(pre5_year_total_cits / pre5_year_total_pub, 2)
                result[f"{year}年均引用率（5年时间窗口）"] = round(pre5_year_total_cits / pre5_year_total_expose, 2)

                # 高影响力论文占比
                year_total_top_pub = df_scholar_type[f"{year}顶刊/会议论文数"].sum()
                year_total_pub_no_pp = df_scholar_type[f"{year}发文总量（不含预印本）"].sum()
                result[f"{year}顶刊/会议论文数"] = year_total_top_pub
                result[f"{year}发文总量（不含预印本）"] = year_total_pub_no_pp
                result[f"{year}顶级期刊/会议发文占比"] = int(round(year_total_top_pub / year_total_pub_no_pp, ndigits=2) * 100) if year_total_pub_no_pp > 0 else 0

                num_patent_family = df_scholar_type[f"{year}专利族数量"].sum()
                result[f"{year}专利族数量"] =num_patent_family
                result[f"{year}平均专利族数量"] = round(num_patent_family / num_scholar, 2)

            data.append(result)
        df_res = pd.DataFrame(data)
        print(df_res)
        self.save_to_excel(df_res, save_file=self.__tbl_name__ + ".xlsx")


if __name__ == "__main__":
    from config import DATASET_DIR, OUTPUT_DIR
    _object = ScholarAcademicAnnualChange()
    _object.calc()
