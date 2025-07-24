# -*- coding: utf-8 -*-
from typing import List
import pandas as pd
from pydantic import BaseModel
from config import END_YEAR


class ScholarDescription(BaseModel):
    """
    学者描述性统计（综合报告附表1，领域报告表1-1、附表1)
    """
    id: str                                     # 学者唯一ID
    name: str                                   # 姓名
    career_length: int                          # 学者职业生涯长度（2024-首篇论文发表年份+1）
    active_years: int                           # 学者活跃年数（发表≥1篇论文的年份数）
    career_total_wos_publications: int          # 学者职业生涯总发文量
    h_index_before_5_years: int                   # 2019年学者H指数（截止到2019年）
    h_index_behind_5_years: int                   # 学者H指数（截止到2024年）
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
        f'{END_YEAR-5}年学者H指数（截止到{END_YEAR-5}年）': 'h_index_before_5_years',
        f'学者H指数（截止到{END_YEAR}年）': 'h_index_behind_5_years',
        '10年总发文量': 'total_publications_10_years',
        '10年SCI论文总发文量': 'total_sci_publications_10_years',
        '10年会议论文总发文量': 'total_meeting_publications_10_years',
        '10年预印本总发文量': 'total_preprint_publications_10_years',
    }
    # 英文属性名到中文字段名的映射（反向映射）
    __en2zh__ = {v: k for k, v in __zh2en__.items()}

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

    @classmethod
    def from_dataframe(cls, _id: str, name: str, df: pd.DataFrame) -> 'ScholarDescription':
        """
        从DataFrame创建ScholarDescription实例
        """
        # 论文发表年份
        df["Publication Year"] = df["Publication Year"].astype(int)
        df["Cited Reference Count"] = df["Cited Reference Count"].fillna(0).astype(int)

        # 1、学者职业生涯长度：2024-首篇论文发表年份+1
        first_paper_year = df["Publication Year"].astype(int).min()
        career_length = END_YEAR - int(first_paper_year) + 1
        print("学者职业生涯长度:", career_length)

        # 2、学者活跃年数：发表≥1篇论文的年份数（TODO:截止2024年？）
        active_years = df["Publication Year"].nunique()
        print("学者活跃年数:", active_years)

        # 3、学者职业生涯总发文量：截止2024年发表论文总量
        df_sub = df[df["Publication Year"] <= END_YEAR]
        career_total_wos_publications = df_sub["Publication Year"].count()
        print("学者职业生涯总发文量:", career_total_wos_publications)

        # 4、2019年学者H指数（截止到2019年）
        df_sub = df[df["Publication Year"] <= END_YEAR - 5]
        h_index_before_5_years = cls.calc_h_index(df_sub["Cited Reference Count"].tolist())
        print(f"学者H指数：截止到{END_YEAR - 5}年:", h_index_before_5_years)

        # 5、学者H指数：截止到2024年
        df_sub = df[df["Publication Year"] <= END_YEAR]
        h_index_behind_5_years = cls.calc_h_index(df_sub["Cited Reference Count"].tolist())
        print(f"学者H指数：截止到{END_YEAR}年:", h_index_behind_5_years)

        # 6、10年总发文量：不区分Document Type
        mask_10_year = (END_YEAR - 5 <= df["Publication Year"]) & (df["Publication Year"] <= END_YEAR)
        total_publications_10_years = df[mask_10_year]["Publication Year"].count()
        print(f"10年总发文量（不区分Document Type）：", total_publications_10_years)

        # 7、10年SCI论文总发文量：统计Web of Science Index中的Science Citation Index Expanded (SCI-EXPANDED)，即SCI论文
        mask = mask_10_year \
            & (df["Web of Science Index"] == "Science Citation Index Expanded (SCI-EXPANDED)")
        total_sci_publications_10_years = df[mask]["Publication Year"].count()
        print(f"10年SCI论文总发文量:", total_sci_publications_10_years)

        # 8、10年会议论文总发文量：统计Web of Science Index中的Conference Proceedings Citation Index - Science (CPCI-S)，即会议论文
        mask = mask_10_year \
            & (df["Web of Science Index"] == "Conference Proceedings Citation Index - Science (CPCI-S)")
        total_meeting_publications_10_years = df[mask]["Publication Year"].count()
        print(f"10年会议论文总发文量:", total_meeting_publications_10_years)

        # 9、10年预印本总发文量：统计Web of Science Index中的preprint，即预印本
        mask = mask_10_year \
            & (df["Web of Science Index"] == "preprint")
        total_preprint_publications_10_years = df[mask]["Publication Year"].count()
        print(f"10年预印本总发文量:", total_preprint_publications_10_years)

        return cls(
            id=_id,
            name=name,
            career_length=career_length,
            active_years=active_years,
            career_total_wos_publications=career_total_wos_publications,
            h_index_before_5_years=h_index_before_5_years,
            h_index_behind_5_years=h_index_behind_5_years,
            total_publications_10_years=total_publications_10_years,
            total_sci_publications_10_years=total_sci_publications_10_years,
            total_meeting_publications_10_years=total_meeting_publications_10_years,
            total_preprint_publications_10_years=total_preprint_publications_10_years,
        )
