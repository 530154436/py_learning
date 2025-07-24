# -*- coding: utf-8 -*-
import pandas as pd
from pydantic import BaseModel
from config import END_YEAR


class ScholarDescription(BaseModel):
    """
    学者描述性统计（综合报告附表1，领域报告表1-1、附表1)
    """
    id: str                                          # 学者唯一ID
    name: str                                        # 姓名
    scholar_career_length: int                       # 学者职业生涯长度（2024-首篇论文发表年份+1）
    scholar_active_years: int                        # 学者活跃年数（发表≥1篇论文的年份数）
    scholar_career_total_wos_publications: str       # 学者职业生涯总发文量
    scholar_career_total_sci_publications: str       # 学者职业生涯SCI论文总发文量
    scholar_career_total_meeting_publications: str   # 学者职业生涯会议论文总发文量
    scholar_h_index_before_5year: str                # 2019年学者H指数（截止到2019年）
    scholar_h_index_behind_5year: str                # 学者H指数（截止到2024年）
    scholar_10_years_total_publications: str         # 10年总发文量
    scholar_10_years_total_sci_publications: str     # 10年SCI论文总发文量
    scholar_10_years_total_meeting_publications: str # 10年会议论文总发文量
    scholar_10_years_total_patents: str              # 10年申请专利
    scholar_10_years_total_granted_patents: str      # 10年授权专利
    scholar_10_years_total_patent_families: str      # 10年专利族数量

    # 中文字段名到英文属性名的映射
    __zh2en__ = {
        "学者唯一ID": "id",
        "姓名": "name",
        '学者职业生涯长度': 'scholar_career_length',
        '学者活跃年数': 'scholar_active_years',
        '学者职业生涯总发文量': 'scholar_career_total_wos_publications',
        '学者职业生涯SCI论文总发文量': 'scholar_career_total_sci_publications',
        '学者职业生涯会议论文总发文量': 'scholar_career_total_meeting_publications',
        f'{END_YEAR-5}年学者H指数（截止到{END_YEAR-5}年）': 'scholar_h_index_before_5year',
        f'学者H指数（截止到{END_YEAR}年）': 'scholar_h_index_behind_5year',
        '10年总发文量': 'scholar_10_years_total_publications',
        '10年SCI论文总发文量': 'scholar_10_years_total_sci_publications',
        '10年会议论文总发文量': 'scholar_10_years_total_meeting_publications',
        '10年申请专利': 'scholar_10_years_total_patents',
        '10年授权专利': 'scholar_10_years_total_granted_patents',
        '10年专利族数量': 'scholar_10_years_total_patent_families'
    }
    # 英文属性名到中文字段名的映射（反向映射）
    __en2zh__ = {v: k for k, v in __zh2en__.items()}

    @classmethod
    def from_dataframe(cls,  df: pd.DataFrame) -> 'ScholarDescription':
        """
        从DataFrame创建ScholarDescription实例
        """
        # 论文发表年份
        df["Publication Year"] = df["Publication Year"].astype(int)

        # 1、学者职业生涯长度：2024-首篇论文发表年份+1
        first_paper_year = df["Publication Year"].astype(int).min()
        scholar_career_length = END_YEAR - int(first_paper_year) + 1
        print("学者职业生涯长度:", scholar_career_length)

        # 2、学者活跃年数：发表≥1篇论文的年份数（TODO:截止2024年？）
        active_years = df["Publication Year"].nunique()
        print("学者活跃年数:", active_years)

        # 3、学者职业生涯总发文量：截止2024年发表论文总量
        mask = df["Publication Year"] <= END_YEAR
        scholar_career_total_wos_publications = df[mask]["Publication Year"].count()
        print("学者职业生涯总发文量:", scholar_career_total_wos_publications)

