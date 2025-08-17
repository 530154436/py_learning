#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2025/7/26 10:50
# @function:
import pandas as pd
from typing import List, Union, Any
from dataclasses_json import DataClassJsonMixin
from pandas import DataFrame
from config import TIME_WINDOW_1_END, OUTPUT_DIR


class AbstractBase(object):
    __tbl_name__ = ""

    @staticmethod
    def calc_citations_per_paper(df: pd.DataFrame, start_year: int, end_year: int, verbose: bool = False) -> pd.DataFrame:
        """
        对每篇论文按年份列求和，得到每篇论文在时间窗口内的总被引次数
        """
        df_sub = df[(start_year <= df["Publication Year"]) & (df["Publication Year"] <= end_year)]
        years = list(str(year) for year in range(start_year, end_year + 1))
        sum_citations_per_paper = df_sub[years].sum(axis=1)
        if verbose:
         print(f"计算每篇论文在时间窗口内的总被引次数：年份={years},每篇文章总被引次数=\n{sum_citations_per_paper}")
        return sum_citations_per_paper

    @staticmethod
    def get_max_citations_paper(df: pd.DataFrame, start_year: int, end_year: int) -> list:
        """
        从指定年份区间内，筛选出被引用次数最高的论文。
        """
        df_sub = df[(start_year <= df["Publication Year"]) & (df["Publication Year"] <= end_year)]
        years = list(str(year) for year in range(start_year, end_year + 1))
        df_sub["sum_citations_per_paper"] = df_sub[years].sum(axis=1)
        result_cols = ["UT (Unique WOS ID)", "Publication Year", "Article Title", "Source Title", "sum_citations_per_paper"]
        df_result = df_sub[result_cols].copy()
        max_citation = df_result["sum_citations_per_paper"].max()
        top_papers = df_result[df_result["sum_citations_per_paper"] == max_citation]
        return [
            {
                "ut": row["UT (Unique WOS ID)"],
                "publication_year": int(row["Publication Year"]),
                "article_title": row["Article Title"],
                "source_title": row["Source Title"],
                "sum_citations_per_paper": int(row["sum_citations_per_paper"])
            }
            for _, row in top_papers.iterrows()
        ]

    @staticmethod
    def calc_h_index(citations: List[int]) -> int:
        """
        H-index是一个数字，由Jorge Hirsch于2005年开始使用，旨在描述科研人员的科学生产力和影响力。
        H-index是通过对同一个科研人员所发表的文章个数及每篇文章他引的次数不低于发表文章个数进行计算的。
        例如：H-index为17意味着该科研人员发表了至少17篇论文，且每篇论文被引用了至少17次。
            如果该科研人员被引用次数最多的第18次出版物仅被引用10次，则h指数将保持在17。
            如果该科研人员被引用次数最多的第18次出版物被18次或更多次引用，则h索引将升高到18。
        我们假设引用次数为m，引用次数大于等于m的论文有n篇，那么只要m>=n，那么一就能得到一个h指数=n（但这里的h指数不一定是最大）：
            h=min(m,n) if m>=n
        那么如何寻找最大的那个h指数呢？首先如果考虑暴力搜索，那么时间复杂度时O(n^2)
        但如果首先根据引用次数多少进行排序，对于第i个元素，我们就可以得到这个等式：
            h指数=论文引用次数大于等于citations[i]的数目=len(citations)-i
        从上面可知，从前往后遍历h指数只能是越来越小（因为i越来越大），于是只需找到第一个满足h指数条件对应的h即可。
        https://zhuanlan.zhihu.com/p/388589868
        """
        citations.sort()
        result = 0
        cite_num = len(citations)
        for i in range(0, cite_num):
            if citations[i] >= cite_num - i:
                result = cite_num - i
                break
        return result

    @staticmethod
    def preprocessing_paper_data(df: DataFrame) -> DataFrame:
        # 论文发表年份
        df["Publication Year"] = df["Publication Year"].astype(int)
        df.columns = df.columns.astype(str)

        # 论文ID: UT (Unique WOS ID)
        # 作者+论文ID：去空、去重
        if "UT (论文唯一标识)" in df.columns:
            df.rename(columns={"UT (论文唯一标识)": "UT (Unique WOS ID)"}, inplace=True)

        subset = ["UT (Unique WOS ID)", "姓名"]
        df = df.dropna(subset=subset)
        df = df.drop_duplicates(subset=subset, keep="first")

        # 论文发表时间截止到2024年
        df = df[df["Publication Year"] <= TIME_WINDOW_1_END].copy()
        return df

    @classmethod
    def save_to_excel(cls, df: DataFrame, save_file: str = None):
        # 保存excel
        if save_file is None:
            save_file = cls.__tbl_name__
            if not cls.__tbl_name__.endswith("xlsx"):
                save_file += ".xlsx"
        output_file = OUTPUT_DIR.joinpath(save_file)
        with pd.ExcelWriter(output_file) as writer:
            df.to_excel(writer, index=False)
        print(f"Saved to {output_file}")

    @classmethod
    def export_to_excel(cls, results: Union[List[dict], DataFrame],
                        clazz: type[DataClassJsonMixin], save_file: str = None,
                        fill_na: Any = None):
        """
        中英文字段映射后写入excel
        """
        if isinstance(results, DataFrame):
            results = results.to_dict(orient="records")
        # 转换为中文字段名
        data = []
        for result in results:
            entity = clazz.from_dict(result)
            print(entity)
            data.append(entity.to_dict())
        df_new = pd.DataFrame(data)
        if fill_na:
            df_new.fillna(value=fill_na, inplace=True)
        cls.save_to_excel(df_new, save_file=save_file)
