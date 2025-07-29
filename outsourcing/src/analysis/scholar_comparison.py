# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from dataclasses_json import config
from analysis.scholar_base import ScholarIdGroupEntity


@dataclass
class ScholarComparisonEntity(ScholarIdGroupEntity):
    """
    用于学者对比的扩展实体
    """
    id: int = field(metadata=config(field_name="学者唯一ID"))
    group_id: int = field(metadata=config(field_name="分组ID"))
    linked_id: str = field(metadata=config(field_name="关联ID"))
    scholar_type: int = field(metadata=config(field_name="学者类型（获奖人=1，0=对照学者）"))
    award_winner_name: str = field(metadata=config(field_name="分组获奖人姓名"))
    name: str = field(metadata=config(field_name="姓名"))
    research_field: str = field(metadata=config(field_name="研究领域"))  # 注意：你写的是 int，但“研究领域”通常是字符串
    research_type: int = field(metadata=config(field_name="研究类型（1=基础科学，0=工程技术，2=前沿交叉）"))


# print(ScholarComparisonEntity.schema().load_fields)