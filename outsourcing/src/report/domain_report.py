# -*- coding: utf-8 -*-
import json

import pandas as pd
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from pypinyin import lazy_pinyin
from config import DATASET_DIR, OUTPUT_DIR, CURRENT_YEAR, \
    TIME_WINDOW_0_START, TIME_WINDOW_1_START, TIME_WINDOW_0_END, TIME_WINDOW_1_END
from utils.plot_util import plot_grouped_bar


class DomainReport:

    def __init__(self, domain: str, template_file: str):
        self.domain = domain
        self.doc: DocxTemplate = DocxTemplate(template_file)
        self.context = dict()
        self.save_dir = OUTPUT_DIR.joinpath(self.domain)
        self.winers = []
        self.init()

    def init(self):
        self.context = {
            "domain": self.domain,
            "CURRENT_YEAR": CURRENT_YEAR,
            'TIME_WINDOW_0_START': TIME_WINDOW_0_START,
            'TIME_WINDOW_0_END': TIME_WINDOW_0_END,
            'TIME_WINDOW_1_START': TIME_WINDOW_1_START,
            'TIME_WINDOW_1_END': TIME_WINDOW_1_END,
        }
        if not self.save_dir.exists():
            self.save_dir.mkdir(parents=True)

    def section1(self):
        input_file = DATASET_DIR.joinpath("S2.1-学者基本信息.xlsx")
        df = pd.read_excel(input_file)

        # 筛选获奖人（学者类型 == 1）
        winners = df[(df['学者类型（获奖人=1，0=对照学者）'] == 1)&(df['研究领域'] == self.domain)].copy()

        # 按姓名拼音排序
        winners["pinyin"] = winners["姓名"].apply(lazy_pinyin)
        winners = winners.sort_values("pinyin", ascending=True)

        self.winers = winners.values.tolist()
        num_winners = len(winners)
        avg_age = int(round(winners[f'年龄（截至统计年份-{CURRENT_YEAR}年）'].mean()))
        youngest = winners.loc[winners[f'年龄（截至统计年份-{CURRENT_YEAR}年）'].idxmin()]
        oldest = winners.loc[winners[f'年龄（截至统计年份-{CURRENT_YEAR}年）'].idxmax()]
        has_nscf = winners['是否获得杰青项目资助（1=是，0=否或者未查询到信息）'] == 1
        have_nscf_num = has_nscf.sum()
        description = (
            f"{self.domain}领域2020届获奖人一共有{num_winners}人。获奖人基本信息见表1-1。"
            f"{have_nscf_num}名获奖人均获得国家杰出青年基金项目资助。目前，获奖人的平均年龄约为{avg_age}岁，"
            f"年龄最小的是{youngest['姓名']}{youngest[f'年龄（截至统计年份-{CURRENT_YEAR}年）']}岁，"
            f"最大是{oldest['姓名']}{oldest[f'年龄（截至统计年份-{CURRENT_YEAR}年）']}岁。"
        )
        # print(description)

        # 表1-1.{{domain}}领域首届获奖人基本信息
        table_data = []
        for _, row in winners.iterrows():
            table_data.append({
                'c1': row['姓名'],
                'c2': row['出生年'],
                'c3': row['工作单位'],
                'c4': row['主要研究方向'],
                'c5': row['学术奖励荣誉/资助'],
            })
        self.context.update({
            'section_1_description': description,
            'num_winners': num_winners,
            'table_1_1': table_data
        })

    def section4_1_image(self):
        input_file = OUTPUT_DIR.joinpath("A2-评价指标数据集.xlsx")
        df = pd.read_excel(input_file)
        # 筛选获奖人（学者类型 == 1）
        df = df[(df['学者类型（获奖人=1，0=对照学者）'] == 1)&(df['研究领域'] == self.domain)].copy()
        # 按姓名拼音排序
        df["pinyin"] = df["姓名"].apply(lazy_pinyin)
        df = df.sort_values("pinyin", ascending=True)
        df["通讯作者论文数（A1）"] = df["通讯作者论文数（A1）"].astype(int)
        df["专利族数量（A2）"] = df["专利族数量（A2）"].astype(int)
        df["第一发明人授权专利数量（A3）"] = df["第一发明人授权专利数量（A3）"].astype(int)

        before = df[df["时间窗口（0=获奖前5年，1=获奖后5年）"] == 0].copy()
        after = df[df["时间窗口（0=获奖前5年，1=获奖后5年）"] == 1].copy()

        # 一级指标绘图
        names = before["姓名"].values.tolist()
        metrics = [
            # 图4-1. 获奖人获奖前后5年学术能力综合得分
            ("综合分数", self.save_dir.joinpath("image_4_1.png")),
            # 图4-2. 获奖人获奖前后5年学术生产力比较
            ("学术生产力", self.save_dir.joinpath("image_4_2.png")),
            # 图4-4. 获奖人获奖前后5年学术影响力比较
            ("学术影响力", self.save_dir.joinpath("image_4_4.png")),
        ]
        for key, save_file in metrics:
            plot_grouped_bar(
                names,
                [before[key].values.tolist(), after[key].values.tolist()],
                labels=["获奖前5年", "获奖后5年"],
                x_label=None,
                y_label=None,
                output_path=save_file
            )
            self.context.update({save_file.stem: InlineImage(self.doc, str(save_file), width=Mm(140))})

        # 二级指标绘图
        metrics = [
            # 图4-3. 获奖人获奖前后5年学术生产力二级指标比较
            (["通讯作者论文数（A1）", "专利族数量（A2）", "第一发明人授权专利数量（A3）"], self.save_dir.joinpath("image_4_3.png")),
            # 图4-5. 获奖人获奖前后5年论文篇均被引频次比较
            (["论文篇均被引频次（B1）"], self.save_dir.joinpath("image_4_5.png")),
            # 图4-6. 获奖人获奖前后5年通讯作者论文单篇最高被引频次比较
            (["单篇最高被引频次（B2）"], self.save_dir.joinpath("image_4_6.png")),
        ]
        for x_data, save_file in metrics:
            y_data_before_list, y_data_after_list = [], []
            for name in names:
                row = before[before["姓名"] == name].iloc[0]
                y_data = [row[key] for key in x_data]
                y_data_before_list.append(y_data)
            for name in names:
                row = after[after["姓名"] == name].iloc[0]
                y_data = [row[key] for key in x_data]
                y_data_after_list.append(y_data)
            plot_grouped_bar(
                x_data,
                y_data_before_list, y_data_after_list,
                labels=names,
                titles=["获奖前5年", "获奖后5年"],
                x_label=None,
                y_label=None,
                fig_size=(14, 6),
                output_path=save_file
            )
            self.context.update({save_file.stem: InlineImage(self.doc, str(save_file), width=Mm(140))})

    def section4_1_table(self):
        input_file = OUTPUT_DIR.joinpath("A2-评价指标数据集.xlsx")
        df = pd.read_excel(input_file)
        # 筛选获奖人（学者类型 == 1）
        df = df[(df['学者类型（获奖人=1，0=对照学者）'] == 1) & (df['研究领域'] == self.domain)].copy()
        # 按姓名拼音排序
        df["pinyin"] = df["姓名"].apply(lazy_pinyin)
        df = df.sort_values("pinyin", ascending=True)

        before = df[df["时间窗口（0=获奖前5年，1=获奖后5年）"] == 0].copy()
        after = df[df["时间窗口（0=获奖前5年，1=获奖后5年）"] == 1].copy()
        names = before["姓名"].values.tolist()

        # 表4-1. 获奖人获奖前后5年以通讯作者身份发表的单篇最高被引论文
        table_4_1_data = []
        for name in names:
            row1 = before[before["姓名"] == name].iloc[0]
            papers1 = json.loads(row1["单篇最高被引频次的论文信息"])
            paper_info1 = papers1[0] if papers1 else dict()
            record = {
                "a": name,
                "b1": paper_info1.get("article_title", "/"),
                "b2": paper_info1.get("source_title", "/"),
                "b3": paper_info1.get("publication_year", "/"),
                "b4": paper_info1.get("sum_citations_per_paper", "/"),
                "b5": "/",
            }
            row2 = after[after["姓名"] == name].iloc[0]
            papers2 = json.loads(row2["单篇最高被引频次的论文信息"])
            paper_info2 = papers2[0] if papers2 else dict()
            record.update({
                "c1": paper_info2.get("article_title", "/"),
                "c2": paper_info2.get("source_title", "/"),
                "c3": paper_info2.get("publication_year", "/"),
                "c4": "/",
                "c5": paper_info2.get("sum_citations_per_paper", "/"),
            })
            table_4_1_data.append(record)
        self.context.update({
            'table_4_1': table_4_1_data
        })

    def section4_2_image(self):
        input_file = OUTPUT_DIR.joinpath("A3-差值分析数据集.xlsx")
        df = pd.read_excel(input_file)
        # 筛选获奖人（学者类型 == 1）
        df = df[(df['学者类型（获奖人=1，0=对照学者）'] == 1)&(df['研究领域'] == self.domain)].copy()
        # 按姓名拼音排序
        df["pinyin"] = df["姓名"].apply(lazy_pinyin)
        df = df.sort_values("pinyin", ascending=True)

        # 图4-13. 获奖人与对照学者获奖前后5年学术影响力差值比较
        metrics = [
            # 图4-11.获奖人与对照学者获奖前后5年学术能力综合得分差值比较
            (["差值-综合分数0", "差值-综合分数1"], self.save_dir.joinpath("image_4_11.png")),
            # 图4-12. 获奖人与对照学者获奖前后5年学术生产力差值比较
            (["差值-学术生产力0", "差值-学术生产力1"], self.save_dir.joinpath("image_4_12.png")),
            # 图4-13. 获奖人与对照学者获奖前后5年学术影响力差值比较
            (["差值-学术影响力0", "差值-学术影响力1"], self.save_dir.joinpath("image_4_13.png"))
        ]
        for key, save_file in metrics:
            names, y_data_before_list, y_data_after_list = [], [], []
            for row in df.to_dict(orient='records'):
                names.append(row['姓名'])
                y_data_before_list.append(row[key[0]])
                y_data_after_list.append(row[key[1]])
            plot_grouped_bar(
                names,
                [y_data_before_list, y_data_after_list],
                labels=["获奖前5年", "获奖后5年"],
                x_label=None,
                y_label=None,
                output_path=save_file
            )
            self.context.update({save_file.stem: InlineImage(self.doc, str(save_file), width=Mm(140))})

    def section4_2_table(self):
        input_file = OUTPUT_DIR.joinpath("A3-差值分析数据集.xlsx")
        df = pd.read_excel(input_file)
        # 筛选获奖人（学者类型 == 1）
        df = df[(df['学者类型（获奖人=1，0=对照学者）'] == 1) & (df['研究领域'] == self.domain)].copy()

        # 表4-2. 获奖人与对照学者获奖前后5年指标得分情况
        table_4_2_data = []
        for index, row in df.iterrows():
            table_4_2_data.append({
                'a1': row['姓名'],
                'a2': round(row['综合分数0'], ndigits=2),
                'a3': round(row['学术生产力0'], ndigits=2),
                'a4': round(row['学术影响力0'], ndigits=2),
                'a5': round(row['综合分数1'], ndigits=2),
                'a6': round(row['学术生产力1'], ndigits=2),
                'a7': round(row['学术影响力1'], ndigits=2),
                'b2': round(row['对照学者均值-综合分数0'], ndigits=2),
                'b3': round(row['对照学者均值-学术生产力0'], ndigits=2),
                'b4': round(row['对照学者均值-学术影响力0'], ndigits=2),
                'b5': round(row['对照学者均值-综合分数1'], ndigits=2),
                'b6': round(row['对照学者均值-学术生产力1'], ndigits=2),
                'b7': round(row['对照学者均值-学术影响力1'], ndigits=2),
                'c2': round(row['差值-综合分数0'], ndigits=2),
                'c3': round(row['差值-学术生产力0'], ndigits=2),
                'c4': round(row['差值-学术影响力0'], ndigits=2),
                'c5': round(row['差值-综合分数1'], ndigits=2),
                'c6': round(row['差值-学术生产力1'], ndigits=2),
                'c7': round(row['差值-学术影响力1'], ndigits=2)
            })
        self.context.update({
            'table_4_2': table_4_2_data
        })

    def appendix_1(self):
        """ 附表1. 对照学者基本信息
        """
        input_file = DATASET_DIR.joinpath("S0.0-获奖人基础信息表.xlsx")
        df = pd.read_excel(input_file)

        # 筛选对照学者（学者类型 == 0）
        df = df[(df['学者类型（获奖人=1，0=对照学者）'] == 0) & (df['研究领域'] == self.domain)].copy()

        # 统计对照学者对应的获奖人
        mapping_series = (
            df.groupby('姓名')['分组获奖人姓名']
            .apply(lambda x: '、'.join(sorted(x.drop_duplicates())))  # 去重 + 排序 + 顿号连接
            .astype(str)
        )
        data = []
        df = df[["姓名", "工作单位", "出生年", "主要研究方向", "学术奖励荣誉/资助"]].drop_duplicates(subset=['姓名'])
        for _, row in df.iterrows():
            data.append({
                'c1': mapping_series.get(row['姓名'], "/"),
                'c2': row['姓名'],
                'c3': row['工作单位'],
                'c4': row['出生年'],
                'c5': row['主要研究方向'],
                'c6': row['学术奖励荣誉/资助']
            })
        self.context.update({'table_appendix_1': data})

    def appendix_2(self):
        input_file = OUTPUT_DIR.joinpath("A2-评价指标数据集.xlsx")
        df = pd.read_excel(input_file)
        df = df[df['研究领域'] == self.domain].copy()
        names = df[df["时间窗口（0=获奖前5年，1=获奖后5年）"] == 0]["姓名"].values.tolist()

        data = []
        keys = [
            "总发文量", "通讯作者论文数（A1）", "专利族数量（A2）", "第一发明人授权专利数量（A3）",
            "论文篇均被引频次（B1）", "单篇最高被引频次（B2）", "前10%高影响力期刊或会议通讯作者论文数量占比（B3）",
            "专利被引频次（B4）"
        ]
        for name in names:
            chunk_0 = df[(df["时间窗口（0=获奖前5年，1=获奖后5年）"] == 0) & (df["姓名"] == name)].iloc[0]
            item = {"c1": chunk_0["姓名"]}
            i = 2
            for key in keys:
                item[f"c{i}"] = chunk_0[key]
                if key == "前10%高影响力期刊或会议通讯作者论文数量占比（B3）":
                    item[f"c{i}"] = str(round(item[f"c{i}"] * 100)) + "%"
                i += 1
            chunk_1 = df[(df["时间窗口（0=获奖前5年，1=获奖后5年）"] == 1) & (df["姓名"] == name)].iloc[0]
            for key in keys:
                item[f"c{i}"] = chunk_1[key]
                if key == "前10%高影响力期刊或会议通讯作者论文数量占比（B3）":
                    item[f"c{i}"] = str(round(item[f"c{i}"] * 100)) + "%"
                i += 1
            data.append(item)

        self.context.update({
            'table_appendix_2': data
        })

    def appendix_3(self):
        input_file = DATASET_DIR.joinpath("S0.0-获奖人基础信息表.xlsx")
        df_basic = pd.read_excel(input_file)[["姓名", "工作单位"]]
        mapping = df_basic.set_index("姓名")["工作单位"].to_dict()

        input_file = OUTPUT_DIR.joinpath("A2-评价指标数据集.xlsx")
        df = pd.read_excel(input_file)
        df = df[df['研究领域'] == self.domain].copy()
        names = df[df["时间窗口（0=获奖前5年，1=获奖后5年）"] == 0]["姓名"].values.tolist()
        data = []
        keys = ["综合分数", "学术生产力", "学术影响力"]
        for name in names:
            chunk_0 = df[(df['时间窗口（0=获奖前5年，1=获奖后5年）'] == 0) & (df['姓名'] == name)].iloc[0]
            item = {
                "c1": chunk_0['分组ID'],
                "c2": chunk_0['姓名'],
                "c3": "获奖人" if chunk_0['学者类型（获奖人=1，0=对照学者）'] == 1 else "对照学者",
                "c4": mapping.get(chunk_0['姓名']),
            }
            for i, key in zip([5, 6, 7], keys):
                item[f"c{i}"] = round(chunk_0[key], ndigits=2)
            chunk_1 = df[(df['时间窗口（0=获奖前5年，1=获奖后5年）'] == 1) & (df['姓名'] == name)].iloc[0]
            for i, key in zip([8, 9, 10], keys):
                item[f"c{i}"] = round(chunk_1[key], ndigits=2)
            # 袁祥岩
            if item["c5"] > 0:
                item["c11"] = str(int((item["c8"] - item["c5"]) / item["c5"] * 100)) + '%'
            else:
                item["c11"] = "/"
            data.append(item)
        data.sort(key=lambda x: x["c1"])
        self.context.update({'table_appendix_3': data})

    def run(self):
        self.section1()
        self.section4_1_image()
        self.section4_1_table()
        self.section4_2_image()
        self.section4_2_table()
        self.appendix_1()
        self.appendix_2()
        self.appendix_3()
        self.doc.render(self.context)
        save_file = f'2-届KT获奖人获奖前后学术能力量化评估——{self.domain}领域.docx'
        self.doc.save(self.save_dir.joinpath(save_file))
        print(save_file)


if __name__ == '__main__':
    _template_file = DATASET_DIR.joinpath("模板/2-届KT获奖人获奖前后学术能力量化评估——领域报告模板.docx")
    _domains = [
        # "数学",
        # "物理学",
        # "化学新材料",
        # "天文和地学",
        # "生命科学",
        # "信息电子",
        # "能源环境",
        # "先进制造",
        "交通建筑",
        # "前沿交叉"
    ]
    for _domain in _domains:
        print(_domain)
        report = DomainReport(_domain, template_file=str(_template_file))
        report.run()
