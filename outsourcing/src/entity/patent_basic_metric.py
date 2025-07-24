# -*- coding: utf-8 -*-
from pydantic import BaseModel


class PatentBasicMetric(BaseModel):
    """
    获奖学者时间窗口指标（获奖前5年 / 获奖后5年）
    """
    id: str  # 学者唯一ID
    name: str  # 姓名
    time_window: int  # 时间窗口（0=获奖前5年，1=获奖后5年）
    patent_families_num: int                              # 专利族数量（A2）
    patent_first_inventor_patent_hum: int                 # 第一发明人授权专利数量（A3）

    # 中文字段名到英文属性名的映射
    __zh2en__ = {
        "学者唯一ID": "id",
        "姓名": "name",
        "时间窗口（0=获奖前5年，1=获奖后5年）": "time_window",
        "专利族数量（A2）": "patent_families_num",
        "第一发明人授权专利数量（A3）": "patent_first_inventor_patent_hum",
    }
    # 英文属性名到中文字段名的映射（反向映射）
    __en2zh__ = {v: k for k, v in __zh2en__.items()}
