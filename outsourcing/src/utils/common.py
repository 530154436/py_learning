# -*- coding: utf-8 -*-
from typing import Dict
from pydantic import BaseModel


def get_field_en2zh(model: BaseModel) -> Dict[str, str]:
    """
    生成模型字段名到 serialization_alias 的映射字典
    :parameter model Pydantic 模型类
    :return 字典，键为字段名，值为 serialization_alias 的值
    """
    mapping = {}
    for field_name, field_info in model.model_fields.items():
        # 获取 serialization_alias，如果未设置则使用字段名本身
        alias = field_info.alias or field_name
        mapping[field_name] = alias
    return mapping


def get_field_zh2en(model: BaseModel) -> Dict[str, str]:
    """
    生成模型serialization_alias到字段名的映射字典
    :parameter model Pydantic 模型类
    :return 字典，键为字段名，值为 serialization_alias 的值
    """
    mapping = {}
    for field_name, field_info in model.model_fields.items():
        # 获取 serialization_alias，如果未设置则使用字段名本身
        alias = field_info.alias or field_name
        mapping[alias] = field_name
    return mapping
