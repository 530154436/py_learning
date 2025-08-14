# -*- coding: utf-8 -*-
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, RGBColor
from docx.table import Table
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph


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


def set_table_column_font(table: Table,
                          font_name_ch: str = '仿宋_GB2312',
                          font_name_en: str = 'Times New Roman',
                          size_pt: float = 10.5):
    """
    设置表格某一列的字体（中英文分别指定），支持数字与非数字差异化字体。
    本函数会遍历该列所有数据行（从第1行开始，跳过表头），自动判断内容是否为纯数字：
        - 纯数字：使用 Times New Roman（英文），中文仍用指定中文字体
        - 其他文本：使用指定中文字体 + 英文对应字体

    :param table: Word 表格对象 (docx.table.Table)
    :param font_name_ch: 中文字体名称，如 '仿宋_GB2312'、'宋体' 等
    :param font_name_en: 对应的英文字体名称，如 'FangSong_GB2312' 或 'Times New Roman'
    :param size_pt: 字号（磅值），默认五号 = 10.5 pt
    """
    if not table:
        return

    for i in range(len(table.rows)):
        for cell in table.rows[i].cells:
            text = cell.text.strip()
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            # cell.vertical_alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

            for paragraph in cell.paragraphs:
                paragraph.vertical_alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                for run in paragraph.runs:
                    run.font.size = Pt(size_pt)  # 设置字号
                    if text.isdigit():
                        # 纯数字：英文字体用 Times New Roman
                        run.font.name = font_name_en
                    else:
                        run.font.name = font_name_en  # 必须先设置font.name, 只对英文文有效
                        # 对中文设置的方法：
                        run.element.rPr.rFonts.set(qn('w:eastAsia'), font_name_ch)


def set_heading_font_style(paragraph: Paragraph,
                           font_name_ch: str = '黑体'):
    # 遍历段落中的所有 run（通常只有一个）
    for run in paragraph.runs:
        run.font.size = Pt(14)  # 四号字 ≈ 14 磅
        run.font.name = 'SimHei'  # 黑体的英文名
        run.font.color.rgb = RGBColor(0, 0, 0)
        run.element.rPr.rFonts.set(qn('w:eastAsia'), font_name_ch)  # 设置中文字体为黑体
        run.bold = False  # 可选：取消加粗（默认 heading 会加粗）
