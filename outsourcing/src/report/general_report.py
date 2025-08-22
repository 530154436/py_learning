# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from docxtpl import DocxTemplate
from analysis import RESEARCH_TYPE_MAPPING
from config import DATASET_DIR, OUTPUT_DIR, CURRENT_YEAR, TIME_WINDOW_0_START, TIME_WINDOW_0_END, TIME_WINDOW_1_START, \
    TIME_WINDOW_1_END


class GeneralReport:

    def __init__(self, template_file: str):
        self.doc: DocxTemplate = DocxTemplate(template_file)
        self.context = dict()
        self.winners = []
        self.init()

    def init(self):
        self.context = {
            "CURRENT_YEAR": CURRENT_YEAR,
            'TIME_WINDOW_0_START': TIME_WINDOW_0_START,
            'TIME_WINDOW_0_END': TIME_WINDOW_0_END,
            'TIME_WINDOW_1_START': TIME_WINDOW_1_START,
            'TIME_WINDOW_1_END': TIME_WINDOW_1_END,
        }

    def appendix_1(self):
        input_file = DATASET_DIR.joinpath("S2.2-学者关联信息表-对照分组.xlsx")
        df = pd.read_excel(input_file)
        df = df[df["学者类型（获奖人=1，0=对照学者）"] == 1]
        df = df[["姓名", "研究领域", "研究类型（1=基础科学，0=工程技术，2=前沿交叉）"]]
        df['研究类型名称'] = df['研究类型（1=基础科学，0=工程技术，2=前沿交叉）'].map(
            lambda x: RESEARCH_TYPE_MAPPING[str(x)])
        print(df.head())

        # 按研究类型、研究领域分组统计
        research_types = df["研究类型名称"].drop_duplicates(keep="first").tolist()
        self.winners = df["姓名"].drop_duplicates(keep="first").tolist()
        table_appendix_1 = []
        for research_type in research_types:
            df_research_type = df[df["研究类型名称"] == research_type]
            research_domains = df_research_type["研究领域"].drop_duplicates(keep="first").tolist()
            b_list, num_names = [], 0
            for research_domain in research_domains:
                chunk = df_research_type[df_research_type["研究领域"] == research_domain]
                names = chunk["姓名"].tolist()
                b_list.append({
                    "b1": research_domain,
                    "b2": len(names),
                    "b3": "\n".join(names),
                })
                num_names += len(names)
            table_appendix_1.append({
                "a": research_type,
                "b_list": b_list,
                "c": num_names,
            })
        print(table_appendix_1)
        self.context.update({
            'table_appendix_1': table_appendix_1,
            "num_winners": len(self.winners)
        })

    def appendix_2(self):
        def calculate_stats(df, time_window) -> list:
            """ 计算统计值
            """
            stats_df = df[df['时间窗口（0=获奖前5年，1=获奖后5年）'] == time_window]
            stats = {
                '发文量': ['总发文量'],
                '通讯作者论文数(A1)': ['通讯作者论文数（A1）'],
                '专利族数量(A2)': ['专利族数量（A2）'],
                '第一发明人授权专利数量(A3)': ['第一发明人授权专利数量（A3）'],
                '论文篇均被引频次(B1)': ['论文篇均被引频次（B1）'],
                'Q1区通讯作者论文数量占比(B2)': ['前10%高影响力期刊或会议通讯作者论文数量占比（B3）'],
                '单篇最高被引频次(B3)': ['单篇最高被引频次（B2）'],
                '专利被引频次(B4)': ['专利被引频次（B4）']
            }
            data = []
            for key, cols in stats.items():
                series = stats_df[cols].values.flatten()
                _min, _max, _mean, _std = series.min(), series.max(), series.mean(), series.std()
                _time_window_str = '获奖前5年' if time_window == 0 else '获奖后5年'
                if key in ['Q1区通讯作者论文数量占比(B2)']:
                    result = {
                        'a1': _time_window_str,
                        'a2': key,
                        'a3': f'{int(_min * 100)}%',
                        'a4': f'{int(_max * 100)}%',
                        'a5': f'{int(_mean * 100)}%',
                        'a6': f'{int(_std * 100)}%',
                    }
                else:
                    result = {
                        'a1': _time_window_str,
                        'a2': key,
                        'a3': int(_min) if isinstance(_min, np.int64) else round(float(_min), 2),
                        'a4': int(_max) if isinstance(_max, np.int64) else round(float(_max), 2),
                        'a5': int(_mean) if isinstance(_mean, np.int64) else round(float(_mean), 2),
                        'a6': int(_std) if isinstance(_std, np.int64) else round(float(_std), 2),
                    }
                data.append(result)
            return data

        input_file = OUTPUT_DIR.joinpath("A2-评价指标数据集.xlsx")
        _df = pd.read_excel(input_file)
        _df = _df[_df["学者类型（获奖人=1，0=对照学者）"] == 1]

        table_appendix_2_1 = calculate_stats(_df, 0)
        table_appendix_2_2 = calculate_stats(_df, 1)
        print(table_appendix_2_1)
        self.context.update({
            'table_appendix_2_1': table_appendix_2_1,
            'table_appendix_2_2': table_appendix_2_2
        })

    def appendix_3(self):
        input_file = OUTPUT_DIR.joinpath("A3-差值分析数据集.xlsx")
        _df = pd.read_excel(input_file)


    def run(self):
        # self.appendix_1()  # 第1列合并有问题
        self.appendix_2()

        self.doc.render(self.context)
        save_file = f'1-首届获奖人获奖前后学术能力量化评估综合报告.docx'
        self.doc.save(OUTPUT_DIR.joinpath(save_file))
        print(save_file)


if __name__ == '__main__':
    _template_file = DATASET_DIR.joinpath("模板/1-首届获奖人获奖前后学术能力量化评估综合报告-模板.docx")
    report = GeneralReport(template_file=str(_template_file))
    report.run()
