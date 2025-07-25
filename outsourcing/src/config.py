# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATASET_DIR = BASE_DIR.joinpath("data/dataset")
OUTPUT_DIR = BASE_DIR.joinpath("data/output")

CURRENT_YEAR = datetime.now().year
TIME_WINDOW_0_START = CURRENT_YEAR - 10
TIME_WINDOW_0_END = CURRENT_YEAR - 6
TIME_WINDOW_1_START = CURRENT_YEAR - 5
TIME_WINDOW_1_END = CURRENT_YEAR - 1

# 2015-2019、2020-2024
print(f"当前年份={CURRENT_YEAR}, 时间窗口="
      f"[{TIME_WINDOW_0_START},{TIME_WINDOW_0_END}], "
      f"[{TIME_WINDOW_1_START},{TIME_WINDOW_1_END}]")
# print(list(range(TIME_WINDOW_0_START, TIME_WINDOW_0_END + 1)))
# print(list(range(TIME_WINDOW_1_START, TIME_WINDOW_1_END + 1)))

if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir(parents=True)

