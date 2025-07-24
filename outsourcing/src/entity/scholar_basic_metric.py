# -*- coding: utf-8 -*-
import pandas as pd
from pydantic import BaseModel
from config import END_YEAR


class ScholarBasicMetric(BaseModel):
    """
    获奖学者时间窗口指标（获奖前5年 / 获奖后5年）
    """
    id: str                                               # 学者唯一ID
    name: str                                             # 姓名
    time_window: int                                      # 时间窗口（0=获奖前5年，1=获奖后5年）
    total_publications: int                               # 总发文量
    total_sci_publications: int                           # SCI论文数
    total_meeting_publications: int                       # 会议论文数
    total_corresponding_author_papers: int                # 通讯作者论文数（A1）
    avg_citations_per_paper: float                        # 论文篇均被引频次（B1）
    max_citations_single_paper: int                       # 单篇最高被引频次（B2）
    top_10_percent_corresponding_papers_ratio: float      # 前10%高影响力期刊或会议通讯作者论文数量占比（B3）
    patent_citations: int                                 # 专利被引频次（B4）

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
    def from_dataframe(cls, _id: str, name: str, df: pd.DataFrame) -> 'ScholarBasicMetric':
        """
        从DataFrame创建ScholarBasicMetric实例
        """
        # 一、计算论文相关基础指标
        mask_0_5_year = (END_YEAR - 10 < df["Publication Year"]) & (df["Publication Year"] <= END_YEAR - 5)    # 2015-2019
        mask_5_10_year = (END_YEAR - 5 < df["Publication Year"]) & (df["Publication Year"] <= END_YEAR)        # 2020-2024
        for time_window, mask in zip([(0, 1), (mask_0_5_year, mask_5_10_year)]):

            df_sub: pd.DataFrame = df.loc[mask]
            print(_id, name, "时间窗口:", time_window)

            total_publications = df_sub.count()
            print("总发文量:", total_publications)


        # 3、学者职业生涯总发文量：截止2024年发表论文总量
        df_sub = df[df["Publication Year"] <= END_YEAR]
        career_total_wos_publications = df_sub["Publication Year"].count()
        print("学者职业生涯总发文量:", career_total_wos_publications)

        # 4、2019年学者H指数（截止到2019年）
        df_sub = df[df["Publication Year"] <= END_YEAR - 5]
        h_index_before_5year = cls.calc_h_index(df_sub["Cited Reference Count"].tolist())
        print(f"学者H指数：截止到{END_YEAR - 5}年:", h_index_before_5year)

        # 5、学者H指数：截止到2024年
        df_sub = df[df["Publication Year"] <= END_YEAR]
        h_index_behind_5year = cls.calc_h_index(df_sub["Cited Reference Count"].tolist())
        print(f"学者H指数：截止到{END_YEAR}年:", h_index_behind_5year)

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

        # return cls(
        #     id=_id,
        #     name=name,
        #     career_length=career_length,
        #     active_years=active_years,
        #     career_total_wos_publications=career_total_wos_publications,
        #     h_index_before_5year=h_index_before_5year,
        #     h_index_behind_5year=h_index_behind_5year,
        #     total_publications_10_years=total_publications_10_years,
        #     total_sci_publications_10_years=total_sci_publications_10_years,
        #     total_meeting_publications_10_years=total_meeting_publications_10_years,
        #     total_preprint_publications_10_years=total_preprint_publications_10_years,
        # )
