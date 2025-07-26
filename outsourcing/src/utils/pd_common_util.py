#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @time: 2021/9/15 14:01
# @function:    通用方法
import pandas as pd
from typing import Union, List


def contains_in(series: pd.Series, values: Union[List[str], str]) -> pd.Series:
    """
    判断series中是否包含多个指定的值（不区分大小写）
    """
    series = series.str.lower().copy()  # 不修改原始值
    if isinstance(values, str):
        return series.str.contains(values.lower(), na=False)
    elif isinstance(values, (list, tuple, set)):
        return series.apply(lambda x: any(val.lower() in x for val in values))
    else:
        raise TypeError("Unsupported type for 'values': {}".format(type(values)))
