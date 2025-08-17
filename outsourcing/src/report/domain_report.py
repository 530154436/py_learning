# -*- coding: utf-8 -*-
import re
import pandas as pd
from docx import Document
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from config import DATASET_DIR, OUTPUT_DIR, CURRENT_YEAR
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

        # 构造表格数据
        table_data = []
        for _, row in winners.iterrows():
            table_data.append({
                'c1': row['姓名'],
                'c2': row['出生年'],
                'c3': row['工作单位'],
                'c4': row['主要研究方向'],
                'c5': extract_jq_year(row['学术奖励荣誉/资助'])
            })
        self.context.update({
            'section_1_description': description,
            'table_1_1': table_data
        })

    def section4_image_a2(self):
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

    def section4_image_a3(self):
        pass

    def run(self):
        self.section1()
        self.section4_image_a2()
        self.section4_image_a3()
        self.doc.render(self.context)
        save_file = f'2-届KT获奖人获奖前后学术能力量化评估——{self.domain}领域.docx'
        self.doc.save(self.save_dir.joinpath(save_file))
        print(save_file)


if __name__ == '__main__':
    _template_file = DATASET_DIR.joinpath("模板/2-届KT获奖人获奖前后学术能力量化评估——领域报告模板.docx")
    report = DomainReport('数学', template_file=str(_template_file))
    report.run()
    report = DomainReport('化学新材料', template_file=str(_template_file))
    report.run()
    report = DomainReport('天文和地学', template_file=str(_template_file))
    report.run()
