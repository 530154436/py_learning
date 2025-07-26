#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2021/9/15 14:01
# @function:    pandas 类型转换工具
from typing import Union, List, Any

import pandas as pd
import numpy as np


class Converter(object):

    @classmethod
    def convert_np_type_2_json_type(cls, data: Union[List[Any], dict]):
        """
        numpy数据类型 => json数据类型
        """
        def convert(value: Any):
            if isinstance(value, (set, tuple, list)):
                value = list(value)
            elif isinstance(value, (np.int8, np.int16, np.int32, np.int64)):
                value = int(value)
            elif isinstance(value, (np.float16, np.float32, np.float64)):
                value = float(value)
            elif pd.isna(value):
                value = None
            elif isinstance(value, pd.Timestamp):
                value = str(value)
            return value

        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = convert(v)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, dict):
                    for k, v in item.items():
                        item[k] = convert(v)
                else:
                    data[i] = convert(item)
        return data
