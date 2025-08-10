# -*- coding: utf-8 -*-
import pandas as pd
from docx import Document
from docx.shared import Pt, Inches

from analysis import RESEARCH_TYPE_MAPPING
from config import DATASET_DIR, OUTPUT_DIR
from utils.doc_tpl_util import merge_table_column, set_table_column_font, set_heading_font_style


def appendix_1(doc: Document):
    """
    附表1. 获奖人按研究类型归类
    """
    input_file = DATASET_DIR.joinpath("S2.2-学者关联信息表-对照分组.xlsx")
    df = pd.read_excel(input_file)
    df = df[df["学者类型（获奖人=1，0=对照学者）"] == 1]
    df = df[["姓名", "研究领域", "研究类型（1=基础科学，0=工程技术，2=前沿交叉）"]]
    df['研究类型名称'] = df['研究类型（1=基础科学，0=工程技术，2=前沿交叉）'].map(lambda x: RESEARCH_TYPE_MAPPING[str(x)])
    print(df)

    # 按研究领域分组统计
    df = df.groupby(['研究类型名称', '研究领域']).agg(
        获奖人数量=('姓名', 'count'),
        获奖人名单=('姓名', lambda x: '\n'.join(x))
    ).reset_index()
    print(df)

    # 创建表格（先只建表头）
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'  # 可选样式

    # 设置表头
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '研究类型'
    hdr_cells[1].text = '研究领域'
    hdr_cells[2].text = '获奖人数量（人）'
    hdr_cells[3].text = '获奖人名单'

    # 存储每个“研究类型”开始的行索引，用于后续合并
    type_start_rows = {}
    current_type = None
    row_index = 1  # 当前是第1行（表头是第0行）

    # 第一步：遍历数据，添加所有行
    for _, row in df.iterrows():
        if row['研究类型名称'] != current_type:
            current_type = row['研究类型名称']
            type_start_rows[current_type] = row_index  # 记录这个类型的第一行索引

        # 添加数据行
        new_row = table.add_row()
        new_row.cells[1].text = row['研究领域']
        new_row.cells[2].text = str(row['获奖人数量'])
        new_row.cells[3].text = row['获奖人名单'].replace('\n', '\n')

        row_index += 1

        # 添加合计行（在每个类型结束后）
        if _ == df.index[-1] or (df['研究类型名称'].iloc[_ + 1] != current_type if _ < len(df) - 1 else True):
            total_row = table.add_row()
            total_row.cells[1].text = '合计'
            total_row.cells[2].text = str(df[df['研究类型名称'] == current_type]['获奖人数量'].sum())
            total_row.cells[3].text = '/'
            row_index += 1

    # 添加数据行：合计
    new_row = table.add_row()
    new_row.cells[0].text = '/'
    new_row.cells[1].text = '总计'
    new_row.cells[2].text = str(df['获奖人数量'].sum())
    new_row.cells[3].text = '/'

    # 第二步：合并“研究类型”列的单元格
    current_type = None
    for i, row in enumerate(table.rows[1:], start=1):  # 跳过表头
        type_text = row.cells[1].text  # 通过“研究领域”判断是否是新类型的第一行

        # 如果当前行是某个研究类型的起始行
        if type_text in df['研究领域'].values and df[df['研究领域'] == type_text]['研究类型名称'].iloc[0] != current_type:
            current_type = df[df['研究领域'] == type_text]['研究类型名称'].iloc[0]
            start_row = i
            # 找到该类型对应的合计行（下个类型开始前）
            next_type_start = None
            for j in range(i + 1, len(table.rows)):
                if table.rows[j].cells[1].text in df['研究领域'].values or table.rows[j].cells[1].text == '合计':
                    next_type_start = j
                    break
            end_row = next_type_start - 1  # 合并到“合计”前一行

            # 合并 cells[0] 从 start_row 到 end_row
            if end_row > start_row:
                cell_to_merge = table.cell(start_row, 0)
                cell_end = table.cell(end_row, 0)
                cell_to_merge.merge(cell_end)
            table.rows[start_row].cells[0].text = current_type
    return table


def add_all_appendix_tables():
    doc = Document()

    # 附件
    set_heading_font_style(doc.add_paragraph('附件'))
    set_heading_font_style(doc.add_heading('附表1. 获奖人按研究类型归类'))
    appendix_1(doc)

    # 获取表格并合并单元格
    for i, table in enumerate(doc.tables):
        table = doc.tables[0]  # 假设要处理的是第一个表格
        doc.tables[i] = merge_table_column(table, col_idx=0)  # 合并第 0 列（时间窗口列）
        set_table_column_font(table)

    doc.save('获奖人分类统计表.docx')
    print("Word表格已生成：获奖人分类统计表.docx")



if __name__ == '__main__':
    add_all_appendix_tables()
