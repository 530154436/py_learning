#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
"""
import os
from pathlib import Path

# 根目录
BASE_DIR = Path(os.path.realpath(__file__)).parent
DATA_DIR = BASE_DIR.joinpath('data')
print(BASE_DIR)