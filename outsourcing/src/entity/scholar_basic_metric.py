# -*- coding: utf-8 -*-
from typing import List
import pandas as pd
from pydantic import BaseModel
from config import BEHIND_5_END_YEAR


class ScholarBasicMetric(BaseModel):
    """
    获奖学者时间窗口指标（获奖前5年 / 获奖后5年）
    """
    id: str                                               # 学者唯一ID
    name: str                                             # 姓名
    time_window: int                                      # 时间窗口（0=获奖前5年，1=获奖后5年）
    total_publications: int                               # 总发文量：统计学者在时间窗口内发表论文总数
    total_sci_publications: int                           # SCI论文数：统计学者在时间窗口内发表SCI论文数
    total_meeting_publications: int                       # 会议论文数：统计学者在时间窗口内发表会议论文数
    total_corresponding_author_papers: int                # 通讯作者论文数（A1）：学者在给定时间内作为通讯作者身份发表总论文数（SCI/会议/预印本）
    avg_citations_per_paper: float                        # 论文篇均被引频次（B1）：通讯作者论文篇均被引频次
    max_citations_single_paper: int                       # 单篇最高被引频次（B2）：在给定时间窗口内（5年）累计总被引频次最高的通讯作者论文引用次数
    top_10_percent_corresponding_papers_ratio: float      # Q1区通讯作者论文数量占比（B3）：各领域JCR前10%期刊或重要国际会议通讯作者论文数量占比

    # 中文字段名到英文属性名的映射
    __zh2en__ = {
        "学者唯一ID": "id",
        "姓名": "name",
        "时间窗口（0=获奖前5年，1=获奖后5年）": "time_window",
        "总发文量": "total_publications",
        "SCI论文数": "total_sci_publications",
        "会议论文数": "total_meeting_publications",
        "通讯作者论文数（A1）": "total_corresponding_author_papers",
        "论文篇均被引频次（B1）": "avg_citations_per_paper",
        "单篇最高被引频次（B2）": "max_citations_single_paper",
        "前10%高影响力期刊或会议通讯作者论文数量占比（B3）": "top_10_percent_corresponding_papers_ratio",
        "专利被引频次（B4）": "patent_citations",
    }
    # 英文属性名到中文字段名的映射（反向映射）
    __en2zh__ = {v: k for k, v in __zh2en__.items()}

    @classmethod
    def calc(cls, _id: str, name: str, df: pd.DataFrame) -> List['ScholarBasicMetric']:
        """
        从DataFrame创建ScholarBasicMetric实例
        计算论文相关基础指标
        """
        df["Cited Reference Count"] = df["Cited Reference Count"].fillna(0)

        mask_0_5_year = (BEHIND_5_END_YEAR - 10 < df["Publication Year"]) & (df["Publication Year"] <= BEHIND_5_END_YEAR - 5)    # 2015-2019
        mask_5_10_year = (BEHIND_5_END_YEAR - 5 < df["Publication Year"]) & (df["Publication Year"] <= BEHIND_5_END_YEAR)        # 2020-2024
        results = []
        for time_window, mask_time_window in zip([0, 1], [mask_0_5_year, mask_5_10_year]):
            df_sub: pd.DataFrame = df.loc[mask_time_window]
            print(_id, name, "时间窗口:", time_window)

            # TODO: UT (Unique WOS ID) 去空、作者+论文ID去重
            # 1、总发文量：统计学者在时间窗口内发表论文总数
            total_publications = df_sub["Publication Year"].count()
            print("总发文量:", total_publications)

            # 2、SCI论文数：统计学者在时间窗口内发表SCI论文数
            mask = df_sub["Web of Science Index"] == "Science Citation Index Expanded (SCI-EXPANDED)"
            total_sci_publications = df_sub[mask]["Publication Year"].count()
            print("SCI论文数:", total_sci_publications)

            # 3、会议论文数：统计学者在时间窗口内发表会议论文数
            mask = df_sub["Web of Science Index"] == "Conference Proceedings Citation Index - Science (CPCI-S)"
            total_meeting_publications = df_sub[mask]["Publication Year"].count()
            print("会议论文数:", total_meeting_publications)

            # 4、通讯作者论文数（A1）：学者在给定时间内作为通讯作者身份发表总论文数（SCI/会议/预印本）TODO包含
            mask = (df_sub["is_corresponding_author(except for math)"] == 1) \
                & (
                   (df_sub["Web of Science Index"] == "Conference Proceedings Citation Index - Science (CPCI-S)")
                   |(df_sub["Web of Science Index"] == "Science Citation Index Expanded (SCI-EXPANDED)")
                   |(df_sub["Web of Science Index"] == "preprint")
                )
            total_corresponding_author_papers = df_sub[mask]["Publication Year"].count()
            print("通讯作者论文数（SCI/会议/预印本）:", total_corresponding_author_papers)

            # 5、论文篇均被引频次（B1）：通讯作者论文篇均被引频次（TODO:通讯作者论文定义同第4点）
            # TODO: 前5年：2015	2016	2017	2018	2019，这五年求和；每篇被引用总数求和/发表论文数
            avg_citations_per_paper = round(df_sub[mask][].mean(), ndigits=3)
            print("论文篇均被引频次（B1）:", avg_citations_per_paper)

            # 6、单篇最高被引频次（B2）：在给定时间窗口内（5年）累计总被引频次最高的通讯作者论文引用次数（TODO:通讯作者论文定义同第4点？）
            # max
            max_ref = df_sub[mask][].max()
            max_citations_single_paper = 0 if pd.isnull(max_ref) else int(max_ref)
            print("单篇最高被引频次（B2）:", max_citations_single_paper)

            # 7、Q1区通讯作者论文数量占比（B3）：各领域JCR前10%期刊或重要国际会议通讯作者论文数量占比
            # 根据is_corresponding_author(except for math)和is_top_journal_confer两个字段筛选出研究者作为通讯作者且发表在顶级期刊或会议上的论文。
            mask = (df_sub["is_corresponding_author(except for math)"] == 1) \
                & (df_sub["is_top_journal_confer（1=yes,0=no,other=preprint）"] == 1) \
                & (
                   (df_sub["Web of Science Index"] == "Conference Proceedings Citation Index - Science (CPCI-S)")
                   | (df_sub["Web of Science Index"] == "Science Citation Index Expanded (SCI-EXPANDED)")
                )
            top_10_percent_corresponding_papers = df_sub[mask]["Publication Year"].count()
            # 分母：total_sci_publications + total_meeting_publications
            top_10_percent_corresponding_papers_ratio = round(top_10_percent_corresponding_papers / total_publications, 3)
            print("Q1区通讯作者论文数量/总论文数:", total_corresponding_author_papers, total_publications)
            print("Q1区通讯作者论文数量占比:", top_10_percent_corresponding_papers_ratio)

            results.append(cls(
                id=_id,
                name=name,
                time_window=time_window,
                total_publications=total_publications,
                total_sci_publications=total_sci_publications,
                total_meeting_publications=total_meeting_publications,
                total_corresponding_author_papers=total_corresponding_author_papers,
                avg_citations_per_paper=avg_citations_per_paper,
                max_citations_single_paper=max_citations_single_paper,
                top_10_percent_corresponding_papers_ratio=top_10_percent_corresponding_papers_ratio,
            ))
        return results
