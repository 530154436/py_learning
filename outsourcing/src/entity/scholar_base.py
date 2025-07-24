# -*- coding: utf-8 -*-
# from dataclasses import dataclass
from pydantic import BaseModel
from entity.scholar_description import ScholarDescription


class ScholarBase(BaseModel):
    """
    学者基础信息
    """
    id: str                                          # 学者唯一ID
    group_id: str                                    # 分组ID
    related_id: str                                  # 关联ID
    scholar_type: str                                # 学者类型（获奖人=1，0=对照学者）
    group_name: str                                  # 分组获奖人姓名
    name: str                                        # 姓名
    company: str                                     # 工作单位
    birth_year: str                                  # 出生年
    age: int                                         # 年龄（截至统计年份-2025年）
    research_field: str                              # 研究领域
    research_type: int                               # 研究类型（1=基础科学，0=工程技术，2=前沿交叉）
    main_research_direction: str                     # 主要研究方向
    academic_honors: str                             # 学术奖励荣誉/资助

    # 中文字段名到英文属性名的映射
    __zh2en__ = {
        "学者唯一ID": "id",
        "分组ID": "group_id",
        "关联ID": "related_id",
        "学者类型": "scholar_type",
        "分组获奖人姓名": "group_name",
        "姓名": "name",
        "工作单位": "company",
        "出生年": "birth_year",
        "年龄": "age",
        "研究领域": "research_field",
        "研究类型": "research_type",
        "主要研究方向": "main_research_direction",
        "学术奖励荣誉/资助": "academic_honors"
    }
    __en2zh__ = {v: k for k, v in __zh2en__.items()}

    @classmethod
    def from_dict(cls, data: dict) -> 'ScholarBase':
        """
        从字典创建 ScholarBase 实例，字典键为中文字段名称
        Args:
            data: 包含学者信息的字典，键为中文字段名
        Returns:
            ScholarBase 实例
        """
        # 获取模型字段信息
        field_info = cls.model_fields

        # 构建参数字典
        kwargs = {}
        for chinese_name, english_name in cls.__zh2en__.items():
            # 获取字段类型
            field_type = field_info[english_name].annotation
            value = data.get(chinese_name, "")

            # 根据字段类型进行转换
            if field_type == int and isinstance(value, str):
                try:
                    value = int(value) if value.strip() else 0
                except ValueError:
                    value = 0
            elif field_type == str:
                value = str(value) if value is not None else ""
            kwargs[english_name] = value
        return cls(**kwargs)
