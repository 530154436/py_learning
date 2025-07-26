# -*- coding: utf-8 -*-
import pandas as pd
from config import TIME_WINDOW_1_END, TIME_WINDOW_0_END, TIME_WINDOW_0_START
from entity.abstract_base import AbstractBase
from utils.pd_common_util import contains_in


class ScholarDescription(AbstractBase):
    """
    学者描述性统计（综合报告附表1，领域报告表1-1、附表1)
    """
    id: str                                     # 学者唯一ID
    name: str                                   # 姓名
    career_length: int                          # 学者职业生涯长度（2024-首篇论文发表年份+1）
    active_years: int                           # 学者活跃年数（发表≥1篇论文的年份数）
    career_total_wos_publications: int          # 学者职业生涯总发文量
    h_index_tw_0_years: int                     # 2019年学者H指数（截止到2019年）：时间窗口0
    h_index_tw_1_years: int                     # 2024年学者H指数（截止到2024年）：时间窗口1
    total_publications_10_years: int            # 10年总发文量：不区分Document Type
    total_sci_publications_10_years: int        # 10年SCI论文总发文量：统计Web of Science Index中的Science Citation Index Expanded (SCI-EXPANDED)，即SCI论文
    total_meeting_publications_10_years: int    # 10年会议论文总发文量：统计Web of Science Index中的Conference Proceedings Citation Index - Science (CPCI-S)，即会议论文
    total_preprint_publications_10_years: int   # 10年预印本总发文量：统计Web of Science Index中的preprint，即预印本

    # 中文字段名到英文属性名的映射
    __zh2en__ = {
        "学者唯一ID": "id",
        "姓名": "name",
        '学者职业生涯长度': 'career_length',
        '学者活跃年数': 'active_years',
        '学者职业生涯总发文量': 'career_total_wos_publications',
        f'{TIME_WINDOW_0_END}年学者H指数（截止到{TIME_WINDOW_0_END}年）': 'h_index_tw_0_years',
        f'{TIME_WINDOW_1_END}年学者H指数（截止到{TIME_WINDOW_1_END}年）': 'h_index_tw_1_years',
        '10年总发文量': 'total_publications_10_years',
        '10年SCI论文总发文量': 'total_sci_publications_10_years',
        '10年会议论文总发文量': 'total_meeting_publications_10_years',
        '10年预印本总发文量': 'total_preprint_publications_10_years',
    }
    # 英文属性名到中文字段名的映射（反向映射）
    __en2zh__ = {v: k for k, v in __zh2en__.items()}

    @classmethod
    def calc(cls, _id: str, name: str, df: pd.DataFrame) -> 'ScholarDescription':
        """
        从DataFrame创建ScholarDescription实例
        """
        # 预处理
        df = cls.preprocessing(df)

        # 1、学者职业生涯长度：2024-首篇论文发表年份+1
        first_paper_year = df["Publication Year"].astype(int).min()
        career_length = TIME_WINDOW_1_END - int(first_paper_year) + 1
        print("学者职业生涯长度:", career_length)

        # 2、学者活跃年数：发表≥1篇论文的年份数
        active_years = df["Publication Year"].nunique(dropna=True)
        print("学者活跃年数:", active_years)

        # 3、学者职业生涯总发文量：截止2024年发表论文总量
        career_total_wos_publications = df["UT (Unique WOS ID)"].nunique(dropna=True)
        print("学者职业生涯总发文量:", career_total_wos_publications)

        # 4、2019年学者H指数（截止到2019年）
        df_sub = df[df["Publication Year"] <= TIME_WINDOW_0_END]
        h_index_tw_0_years = cls.calc_h_index(df_sub["Cited Reference Count"].tolist())
        print(f"学者H指数：截止到{TIME_WINDOW_0_END}年:", h_index_tw_0_years)

        # 5、学者H指数：截止到2024年
        df_sub = df[df["Publication Year"] <= TIME_WINDOW_1_END]
        h_index_tw_1_years = cls.calc_h_index(df_sub["Cited Reference Count"].tolist())
        print(f"学者H指数：截止到{TIME_WINDOW_1_END}年:", h_index_tw_1_years)

        # 6、10年总发文量
        mask_10_year = (TIME_WINDOW_0_START <= df["Publication Year"]) & (df["Publication Year"] <= TIME_WINDOW_1_END)
        total_publications_10_years = df[mask_10_year]["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"10年总发文量（不区分Document Type）：", total_publications_10_years)

        # 7、10年SCI论文总发文量：统计Web of Science Index中的Science Citation Index Expanded (SCI-EXPANDED)，即SCI论文
        mask = mask_10_year \
            & contains_in(df["Web of Science Index"], ["Science Citation Index Expanded (SCI-EXPANDED)"]) \
            & contains_in(df["Document Type"], ["Article", "Review"])
        total_sci_publications_10_years = df[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"10年SCI论文总发文量:", total_sci_publications_10_years)

        # 8、10年会议论文总发文量：统计Web of Science Index中的Conference Proceedings Citation Index - Science (CPCI-S)，即会议论文
        # TODO: （多个会议的情况，id+优先级SCI-E>CPCI-S>preprint）
        mask = mask_10_year \
            & contains_in(df["Web of Science Index"], ["Conference Proceedings Citation Index - Science (CPCI-S)"]) \
            & (~contains_in(df["Web of Science Index"], ["Science Citation Index Expanded (SCI-EXPANDED)"])) \
            & contains_in(df["Document Type"], ["Article", "Review"])
        total_meeting_publications_10_years = df[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"10年会议论文总发文量:", total_meeting_publications_10_years)

        # 9、10年预印本总发文量：统计Web of Science Index中的preprint，即预印本
        mask = mask_10_year \
               & contains_in(df["Web of Science Index"], ["preprint"])
        total_preprint_publications_10_years = df[mask]["UT (Unique WOS ID)"].nunique(dropna=True)
        print(f"10年预印本总发文量:", total_preprint_publications_10_years)

        return cls(
            id=_id,
            name=name,
            career_length=career_length,
            active_years=active_years,
            career_total_wos_publications=career_total_wos_publications,
            h_index_tw_0_years=h_index_tw_0_years,
            h_index_tw_1_years=h_index_tw_1_years,
            total_publications_10_years=total_publications_10_years,
            total_sci_publications_10_years=total_sci_publications_10_years,
            total_meeting_publications_10_years=total_meeting_publications_10_years,
            total_preprint_publications_10_years=total_preprint_publications_10_years,
        )
