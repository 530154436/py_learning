# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATASET_DIR = BASE_DIR.joinpath("data/dataset")
OUTPUT_DIR = BASE_DIR.joinpath("data/output")

CURRENT_YEAR = datetime.now().year
END_YEAR = CURRENT_YEAR - 1
START_YEAR = END_YEAR - 10
print(START_YEAR, END_YEAR)

if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir(parents=True)

