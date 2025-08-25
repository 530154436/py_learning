# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from pandas import DataFrame, Series
from scipy import stats

from analysis import RESEARCH_TYPE_MAPPING
from config import DATASET_DIR, OUTPUT_DIR, CURRENT_YEAR, TIME_WINDOW_0_START, TIME_WINDOW_0_END, TIME_WINDOW_1_START, \
    TIME_WINDOW_1_END
from utils.plot_util import plot_line_chart


class GeneralReport:

    def __init__(self, template_file: str):
        self.doc: DocxTemplate = DocxTemplate(template_file)
        self.save_dir = OUTPUT_DIR.joinpath("00-综合报告")
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
        if not self.save_dir.exists():
            self.save_dir.mkdir(parents=True)

    def section_3_2_image(self):
        input_file = OUTPUT_DIR.joinpath("A1.3-群体学术能力年度趋势.xlsx")
        df = pd.read_excel(input_file)

        # 1、计算指标
        for year in range(TIME_WINDOW_0_START, TIME_WINDOW_1_END + 1):
            df[f"{year}平均发文量/篇"] = np.round(df[f"{year}年度发文总量"] / df["学者人数"], 2)
            df[f"{year}年均引用率（截止{TIME_WINDOW_1_END}）"] = df[f"群体{year}年均引用率（截止{TIME_WINDOW_1_END}）"]
            df[f"{year}ACPP"] = df[f"群体{year}ACPP"]
            df[f"{year}年度当年篇均被引频次"] = df[f"{year}年度当年篇均被引频次"]
            df[f"{year}年度高影响力论文占比/百分比"] = df[f"{year}年度高影响力论文占比"].apply(lambda x: int(x * 100))
            df[f"{year}年平均专利族数量"] = np.round(df[f"{year}年度专利族数量"] / df["学者人数"], 2)

        # 2、绘制折线图
        metrics = [
            # 图3-1. 获奖人与对照学者发文量年度变化
            ("{year}平均发文量/篇", self.save_dir.joinpath("image_3_1.png")),
            # 图3-2-1. 获奖人与对照学者年均引用率（截止2024）
            ("{year}年均引用率"+f"（截止{TIME_WINDOW_1_END}）", self.save_dir.joinpath("image_3_2_1.png")),
            # 图3-2-2. 获奖人与对照学者ACPP
            ("{year}ACPP", self.save_dir.joinpath("image_3_2_2.png")),
            # 图3-2-3. 获奖人与对照学者年度当年篇均被引频次
            ("{year}年度当年篇均被引频次", self.save_dir.joinpath("image_3_2_3.png")),
            # 图3-3. 获奖人与对照学者高影响力论文占比年度变化
            ("{year}年度高影响力论文占比/百分比", self.save_dir.joinpath("image_3_3.png")),
            # 图3-4. 获奖人与对照学者专利族数量年度变化
            ("{year}年平均专利族数量", self.save_dir.joinpath("image_3_4.png")),
        ]
        x_data = list(map(lambda x: str(x), range(TIME_WINDOW_0_START, TIME_WINDOW_1_END + 1)))
        labels = ["获奖人", "对照学者"]
        for y_label, save_file in metrics:
            print(f"折线图: {y_label}")
            # 组装数据
            y_data = []
            for scholar_type, label in zip([1, 0], labels):
                row = df[df["学者类型（获奖人=1，0=对照学者）"] == scholar_type].iloc[0]
                y_data_i = []
                for year in x_data:
                    y_data_i.append(row[y_label.format(year=year)])
                y_data.append(y_data_i)
            # 调用绘图函数
            y_label_show = y_label.format(year="")
            plot_line_chart(
                x_data=x_data,
                y_data=y_data,
                labels=labels,
                title=None,
                x_label="年份",
                y_label=y_label_show,
                output_path=save_file,
            )
            self.context.update({save_file.stem: InlineImage(self.doc, str(save_file), width=Mm(140))})

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
        df = pd.read_excel(input_file)
        # 只保留获奖人（学者类型 = 1）
        df = df[df['学者类型（获奖人=1，0=对照学者）'] == 1].reset_index(drop=True)

        table_appendix_3 = []
        for idx, row in enumerate(df.to_dict(orient="records"), start=1):
            table_appendix_3.append({
                'a1': idx,
                'a2': row['姓名'],
                'a3': row['研究领域'],
                'a4': f"{row['差值-综合分数0']: .2f}",
                'a5': f"{row['差值-学术生产力0']: .2f}",
                'a6': f"{row['差值-学术影响力0']: .2f}",
                'a7': f"{row['差值-综合分数1']: .2f}",
                'a8': f"{row['差值-学术生产力1']: .2f}",
                'a9': f"{row['差值-学术影响力1']: .2f}",
                'a10': row['成长模式'],
            })
        self.context.update({
            'table_appendix_3': table_appendix_3
        })

    def calc_ttest_rel(self, label, pre_diff: Series, post_diff: Series):
        """ 计算：获奖人相对于对照组的“差距变化”是否显著
            即：检验 (差值-综合分数1) vs (差值-综合分数0) 是否有显著变化
        """
        # 计算“差距的变化”：post_diff - pre_diff
        diff_change = post_diff - pre_diff

        n = len(diff_change)
        mean_diff = diff_change.mean()
        std_dev = diff_change.std()
        std_err = std_dev / np.sqrt(n)

        # 95% 置信区间
        ci = stats.t.interval(0.95, df=n - 1, loc=mean_diff, scale=std_err)
        ci_lower, ci_upper = ci

        # 配对样本 t 检验：检验“差距变化”是否显著不为0
        t_stat, p_value = stats.ttest_rel(post_diff, pre_diff)  # 等价于 ttest_1samp(diff_change, 0)
        return {
            'a1': label,                # 指标
            'a2': round(mean_diff, 2),  # 均值差值
            'a3': round(std_dev, 2),    # 标准差
            'a4': round(std_err, 2),    # 均值的标准误差
            'a5': round(ci_lower, 2),   # CI下限
            'a6': round(ci_upper, 2),   # CI上限
            'a7': round(t_stat, 2),     # t
            'a8': n - 1,                # df
            'a9': round(p_value, 2)     # Sig.(双侧)
        }

    def appendix_4(self):
        input_file = OUTPUT_DIR.joinpath("A3-差值分析数据集.xlsx")
        df = pd.read_excel(input_file)
        df = df[df['学者类型（获奖人=1，0=对照学者）'] == 1].copy()
        # 定义要检验的指标
        changes = {
            '综合分数1-\r综合分数0': ('差值-综合分数0', '差值-综合分数1'),
            '学术生产力1-\r学术生产力0': ('差值-学术生产力0', '差值-学术生产力1'),
            '学术影响力1-\r学术影响力0': ('差值-学术影响力0', '差值-学术影响力1')
        }
        table_appendix_4 = []
        for label, (pre_diff_col, post_diff_col) in changes.items():
            pre_diff = df[pre_diff_col]     # 获奖前，获奖人比对照组高/低多少
            post_diff = df[post_diff_col]   # 获奖后，获奖人比对照组高/低多少
            table_appendix_4.append(self.calc_ttest_rel(label, pre_diff, post_diff))
        self.context.update({
            'table_appendix_4': table_appendix_4
        })

    def appendix_5(self):
        # 表格
        input_file = OUTPUT_DIR.joinpath("A4-胜率分析数据集.xlsx")
        df = pd.read_excel(input_file)
        df = df[df['学者类型（获奖人=1，0=对照学者）'] == 1].copy()
        print(df.shape)

        labels = ["胜率-综合分数0", "胜率-综合分数1"]
        keys = ["获奖前5年", "获奖后5年"]
        table_appendix_5 = []
        # 分析文本中用到的变量
        appendix_5_text = dict()
        for key, label in zip(keys, labels):
            df["胜率"] = df[label].apply(lambda x: float(x.strip("%")))
            num_50_100 = (df["胜率"] > 50).sum()
            table_appendix_5.append({
                'a1': key,
                'a2': f'{(df["胜率"] <= 0).sum()}人',
                'a3': f'{((df["胜率"] > 0) & (df["胜率"] <= 50)).sum()}人',
                'a4': f'{num_50_100}人',
            })
            if key == "获奖前5年":
                appendix_5_text["b1"] = num_50_100
                appendix_5_text["b2"] = f"{int(round(num_50_100/df.shape[0], 2) * 100)}%"
            elif key == "获奖后5年":
                appendix_5_text["c1"] = num_50_100
                appendix_5_text["c2"] = f"{int(round(num_50_100 / df.shape[0], 2) * 100)}%"
        appendix_5_text["d"] = "提高" if appendix_5_text["c1"] > appendix_5_text["b1"] else "降低"

        self.context.update({
            'appendix_5_table': table_appendix_5,
            'appendix_5_text': appendix_5_text,
        })

    def run(self):
        self.section_3_2_image()

        self.appendix_1()  # 第1列合并有问题
        self.appendix_2()
        self.appendix_3()
        self.appendix_4()
        self.appendix_5()

        self.doc.render(self.context)
        save_file = f'1-首届获奖人获奖前后学术能力量化评估综合报告.docx'
        self.doc.save(self.save_dir.joinpath(save_file))
        print(save_file)


if __name__ == '__main__':
    _template_file = DATASET_DIR.joinpath("模板/1-首届获奖人获奖前后学术能力量化评估综合报告-模板.docx")
    report = GeneralReport(template_file=str(_template_file))
    report.run()
