# -*- coding: utf-8 -*-
import re
import pandas as pd
from docx import Document
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from config import DATASET_DIR, OUTPUT_DIR, CURRENT_YEAR, TIME_WINDOW_0_START, TIME_WINDOW_1_START, TIME_WINDOW_0_END, \
    TIME_WINDOW_1_END
from utils.doc_tpl_util import set_font_style
from utils.plot_util import plot_grouped_bar


class DomainReport:

    def __init__(self, domain: str, template_file: str):
        self.domain = domain
        self.doc: DocxTemplate = DocxTemplate(template_file)
        self.context = {
            "domain": self.domain,
            "CURRENT_YEAR": CURRENT_YEAR
        }
        self.save_dir = OUTPUT_DIR.joinpath(self.domain)
        if not self.save_dir.exists():
            self.save_dir.mkdir(parents=True)

    @staticmethod
    def extract_jq_year(funding_text):
        """从资助文本中提取杰青/国家杰出青年的年份
        """
        if not isinstance(funding_text, str):
            return "/"
        # 匹配 2022年杰青、2018杰青、国家杰出青年基金（2014）等
        patterns = [
            r'(?:20|19)\d{2}[年\-]?\s*(?:获)?(?:杰青|国家杰出青年)',
            r'(?:杰青|国家杰出青年).*?(?:20|19)\d{2}',
        ]
        for pattern in patterns:
            match = re.search(pattern, funding_text)
            if match:
                year_match = re.search(r'(?:20|19)\d{2}', match.group())
                if year_match:
                    return year_match.group() + "年"
        return "/"

    def section1(self):
        input_file = DATASET_DIR.joinpath("S0.0-获奖人基础信息表.xlsx")
        df = pd.read_excel(input_file)

        # 筛选获奖人（学者类型 == 1）
        winners = df[(df['学者类型（获奖人=1，0=对照学者）'] == 1)&(df['研究领域'] == self.domain)].copy()
        num_winners = len(winners)
        avg_age = int(round(winners[f'年龄（截至统计年份-{CURRENT_YEAR}年）'].mean()))
        youngest = winners.loc[winners[f'年龄（截至统计年份-{CURRENT_YEAR}年）'].idxmin()]
        oldest = winners.loc[winners[f'年龄（截至统计年份-{CURRENT_YEAR}年）'].idxmax()]
        has_nscf = winners['学术奖励荣誉/资助'].str.contains('杰青|优青', case=False, na=False)
        have_nscf_num = has_nscf.sum()
        description = (
            f"{self.domain}领域***届获奖人一共有{num_winners}人。获奖人基本信息见表1-1。"
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
                'c5': self.extract_jq_year(row['学术奖励荣誉/资助'])
            })
        self.context.update({
            'section_1_description': description,
            'table_1_1': table_data
        })

    def section4_1_image_a2(self):
        input_file = OUTPUT_DIR.joinpath("A2-评价指标数据集.xlsx")
        df = pd.read_excel(input_file)
        # 筛选获奖人（学者类型 == 1）
        df = df[(df['学者类型（获奖人=1，0=对照学者）'] == 1)&(df['研究领域'] == self.domain)].copy()
        before = df[df["时间窗口（0=获奖前5年，1=获奖后5年）"] == 0].copy()
        after = df[df["时间窗口（0=获奖前5年，1=获奖后5年）"] == 1].copy()

        # 一级指标绘图
        y_data_before_1 = before.set_index("姓名")
        y_data_after_1 = after.set_index("姓名")
        names = y_data_before_1.index.tolist()
        metrics = [
            ("学术生产力", self.save_dir.joinpath("image_4_1.png")),
            ("学术影响力", self.save_dir.joinpath("image_4_2.png")),
            # 图4-4. 获奖人获奖前后5年学术影响力比较
            ("综合分数", self.save_dir.joinpath("image_4_4.png"))
        ]
        for key, save_file in metrics:
            plot_grouped_bar(
                names,
                [y_data_before_1[key].values.tolist(), y_data_after_1[key].values.tolist()],
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
            y_data_before_list, y_data_after_list, labels = [], [], []
            # 按姓名分组，提取每位获奖人的数据
            for name, group in before.groupby("姓名"):
                row = group.iloc[0]
                y_data = [row[key] for key in x_data]
                y_data_before_list.append(y_data)
                labels.append(name)
            for name, group in after.groupby("姓名"):
                row = group.iloc[0]
                y_data = [row[key] for key in x_data]
                y_data_after_list.append(y_data)
            plot_grouped_bar(
                x_data,
                y_data_before_list, y_data_after_list,
                labels=labels,
                titles=["获奖前5年", "获奖后5年"],
                x_label=None,
                y_label=None,
                fig_size=(12, 6),
                output_path=save_file
            )
            self.context.update({save_file.stem: InlineImage(self.doc, str(save_file), width=Mm(140))})

    def section4_1_image_a3(self):
        input_file = OUTPUT_DIR.joinpath("A3-差值分析数据集.xlsx")
        df = pd.read_excel(input_file)
        # 筛选获奖人（学者类型 == 1）
        df = df[(df['学者类型（获奖人=1，0=对照学者）'] == 1)&(df['研究领域'] == self.domain)].copy()

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

    def section4_2_table_a3(self):
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
                'c1': row['姓名'],
                'c2': row['工作单位'],
                'c3': mapping_series.get(row['姓名'], "/"),
                'c4': row['出生年'],
                'c5': row['主要研究方向'],
                'c6': self.extract_jq_year(row['学术奖励荣誉/资助'])
            })
        self.context.update({'table_appendix_1': data})

    def appendix_2(self):
        input_file = OUTPUT_DIR.joinpath("A2-评价指标数据集.xlsx")
        df = pd.read_excel(input_file)
        df = df[df['研究领域'] == self.domain].copy()

        data = []
        keys = [
            "SCI论文数", "通讯作者论文数（A1）", "专利族数量（A2）", "第一发明人授权专利数量（A3）",
            "论文篇均被引频次（B1）", "前10%高影响力期刊或会议通讯作者论文数量占比（B3）", "单篇最高被引频次（B2）",
            "专利被引频次（B4）"
        ]
        for _, chunk in df.groupby(by=['姓名']):
            chunk_0 = chunk[chunk['时间窗口（0=获奖前5年，1=获奖后5年）'] == 0].iloc[0]
            item = {"c1": chunk_0["姓名"]}
            i = 2
            for key in keys:
                item[f"c{i}"] = chunk_0[key]
                i += 1
            chunk_1 = chunk[chunk['时间窗口（0=获奖前5年，1=获奖后5年）'] == 1].iloc[0]
            for key in keys:
                item[f"c{i}"] = chunk_1[key]
                i += 1
            data.append(item)
        self.context.update({
            'TIME_WINDOW_0_START': TIME_WINDOW_0_START,
            'TIME_WINDOW_0_END': TIME_WINDOW_0_END,
            'TIME_WINDOW_1_START': TIME_WINDOW_1_START,
            'TIME_WINDOW_1_END': TIME_WINDOW_1_END,
            'table_appendix_2': data
        })

    def appendix_3(self):
        input_file = DATASET_DIR.joinpath("S0.0-获奖人基础信息表.xlsx")
        df_basic = pd.read_excel(input_file)[["姓名", "工作单位"]]
        mapping = df_basic.set_index("姓名")["工作单位"].to_dict()

        input_file = OUTPUT_DIR.joinpath("A2-评价指标数据集.xlsx")
        df = pd.read_excel(input_file)
        df = df[df['研究领域'] == self.domain].copy()
        data = []
        keys = ["综合分数", "学术生产力", "学术影响力"]
        for _, chunk in df.groupby(by=['姓名']):
            chunk_0 = chunk[chunk['时间窗口（0=获奖前5年，1=获奖后5年）'] == 0].iloc[0]
            item = {
                "c1": chunk_0['分组ID'],
                "c2": chunk_0['姓名'],
                "c3": "获奖人" if chunk_0['学者类型（获奖人=1，0=对照学者）'] == 1 else "对照学者",
                "c4": mapping.get(chunk_0['姓名']),
            }
            for i, key in zip([5, 6, 7], keys):
                item[f"c{i}"] = round(chunk_0[key], ndigits=2)
            chunk_1 = chunk[chunk['时间窗口（0=获奖前5年，1=获奖后5年）'] == 1].iloc[0]
            for i, key in zip([8, 9, 10], keys):
                item[f"c{i}"] = round(chunk_1[key], ndigits=2)
            # 袁祥岩
            if item["c5"] > 0:
                item["c11"] = str(int((item["c8"] - item["c5"]) / item["c5"] * 100)) + '%'
            else:
                item["c11"] = "/"
            data.append(item)
        self.context.update({'table_appendix_3': data})


    def run(self):
        self.section1()
        self.section4_1_image_a2()
        self.section4_1_image_a3()
        self.section4_2_table_a3()
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
        "数学",
        "物理学",
        "化学新材料",
        "天文和地学",
        "生命科学",
        "信息电子",
        "能源环境",
        "先进制造",
        "交通建筑",
        "前沿交叉"
    ]
    for domain in _domains:
        print(domain)
        report = DomainReport(domain, template_file=str(_template_file))
        report.run()
