# -*- coding: utf-8 -*-
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


def merge_table_column(table, col_idx: int = 0):
    """
    合并表格中某列的连续相同值或空值，并设置垂直居中、去除换行。
    :param table: Word 表格对象，docx.table.Table
    :param col_idx: 需要合并的列索引
    """
    if not table or col_idx >= len(table.columns):
        return

    start_row = 1  # 数据行从第1行开始（假设表头是第0行）
    prev_value = None

    for i in range(1, len(table.rows)):  # 从数据行第一行开始遍历
        cell = table.rows[i].cells[col_idx]
        current = cell.text.strip()

        # 处理空值：视为与上一个非空值相同
        if not current:
            current = prev_value if prev_value else ""

        # 初始情况处理
        if i == 1:
            prev_value = current
            continue

        # 如果当前值与前一个值不同，则合并上一个区间
        if current != prev_value:
            if i - start_row > 1:
                # 合并单元格
                merged_cell = table.cell(start_row, col_idx).merge(table.cell(i - 1, col_idx))
                # 设置垂直居中
                merged_cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                merged_cell.vertical_alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                merged_cell.text = merged_cell.text.strip()
            start_row = i
            prev_value = current

    # 处理最后一组合并
    if len(table.rows) - start_row > 1:
        merged_cell = table.cell(start_row, col_idx).merge(table.cell(len(table.rows) - 1, col_idx))
        # 设置垂直居中
        merged_cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        merged_cell.vertical_alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        merged_cell.text = merged_cell.text.strip()

    return table
