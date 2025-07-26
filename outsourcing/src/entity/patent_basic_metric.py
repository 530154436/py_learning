# -*- coding: utf-8 -*-
from typing import List
import pandas as pd
from pydantic import BaseModel


class PatentBasicMetric(BaseModel):
    """
    获奖学者时间窗口指标（获奖前5年 / 获奖后5年）
    """
    id: str  # 学者唯一ID
    name: str  # 姓名
    time_window: int                            # 时间窗口（0=获奖前5年，1=获奖后5年）
    patent_families_num: int                    # 专利族数量（A2）：学者在给定时间内拥有的DWPI同族专利数量
    patent_first_inventor_patent_hum: int       # 第一发明人授权专利数量（A3）：学者在给定时间内作为第一发明人授权的发明专利数量
    patent_citations: int                       # 专利被引次数（B4）：指专利族截至数据采集时间的总被引用次数

    # 中文字段名到英文属性名的映射
    __zh2en__ = {
        "学者唯一ID": "id",
        "姓名": "name",
        "时间窗口（0=获奖前5年，1=获奖后5年）": "time_window",
        "专利族数量（A2）": "patent_families_num",
        "第一发明人授权专利数量（A3）": "patent_first_inventor_patent_hum",
        "专利被引次数（B4）": "patent_citations",
    }
    # 英文属性名到中文字段名的映射（反向映射）
    __en2zh__ = {v: k for k, v in __zh2en__.items()}

    @classmethod
    def calc(cls, _id: str, name: str, df: pd.DataFrame) -> List['PatentBasicMetric']:
        """
        从DataFrame创建PatentBasicMetric实例
        计算专利相关基础指标
        """
        mask_0_5_year = (BEHIND_5_END_YEAR - 10 < df["申请年"]) & (df["申请年"] <= BEHIND_5_END_YEAR - 5)  # 2015-2019
        mask_5_10_year = (BEHIND_5_END_YEAR - 5 < df["申请年"]) & (df["申请年"] <= BEHIND_5_END_YEAR)  # 2020-2024
        results = []
        for time_window, mask_time_window in zip([0, 1], [mask_0_5_year, mask_5_10_year]):
            # 申请年：用于筛选给定时间内的专利（例如，获奖前5年或获奖后5年）。
            df_sub: pd.DataFrame = df.loc[mask_time_window]

            # 1、专利族数量（A2）：学者在给定时间内拥有的DWPI同族专利数量
            # DWPI 入藏号：每个专利族在DWPI中的唯一标识符（Accession Number），用于区分不同的专利族。
            # DWPI 同族专利成员计数：表示该专利族包含的成员专利数量，但A2是计数专利族本身（不是成员数量），因此需基于DWPI 入藏号去重计数。
            patent_families_num = df_sub["DWPI 入藏号"].nunique(dropna=True)
            print("专利族数量（A2）:", patent_families_num)
            # TODO: DWPI同族专利合并 sheet： 直接计数

            # 2、第一发明人授权专利数量（A3）：学者在给定时间内作为第一发明人授权的发明专利数量
            mask = (df_sub["第一发明人（是-1，否-0）"] == 1) \
                & (df_sub["专利类型（申请-0，授权-1）"] == 1)
            patent_first_inventor_patent_hum = df_sub[mask]["公开号"].nunique(dropna=True)
            print("第一发明人授权专利数量（A3）:", patent_first_inventor_patent_hum)

            # 3、专利被引次数（B4）：指专利族截至数据采集时间的总被引用次数
            # 施引专利计数 - DPCI：表示该专利族被引用的总次数（DPCI 是 Derwent Patent Citation Index 的缩写，提供标准化引用数据）。
            # DWPI 入藏号：用于关联专利族（B4是基于专利族计算的，因此同一族的所有成员共享同一个被引次数）。
            df_res = df_sub.drop_duplicates(subset=["公开号"])
            patent_citations = df_res["施引专利计数 - DPCI"].fillna(0).sum()
            print("专利被引次数（B4）:", patent_first_inventor_patent_hum)

            results.append(cls(
                id=_id,
                name=name,
                time_window=time_window,
                patent_families_num=patent_families_num,
                patent_first_inventor_patent_hum=patent_first_inventor_patent_hum,
                patent_citations=patent_citations,
            ))
        return results

