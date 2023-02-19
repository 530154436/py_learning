#!/usr/bin/env python3
# -*- coding:utf-8 -*--
import uuid

import pandas as pd

from framework.web_flask import BASE_DIR

total = 20
column_num = 3

rows = []
columns = []
columns.append({"field": "id", "title": "id", "align": "center", "sortable": True})
for i in range(total):
    _id = i
    row = {
        "id": i
    }

    for j in range(column_num):
        column_name = f"column{j}"
        row[column_name] = i
        if i == 0:
            columns.append({
                "field": column_name,
                "title": column_name,
                "align": "center",
                "sortable": True  # 设置ID列可以排序
            })

    df = pd.DataFrame([row])
    file = BASE_DIR.joinpath("data", "result", f"{_id}.xlsx")
    with pd.ExcelWriter(file, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)

    rows.append(row)

boostrap_table_data = {
    "rows": rows,
    "columns": columns,
    "total": total
}
