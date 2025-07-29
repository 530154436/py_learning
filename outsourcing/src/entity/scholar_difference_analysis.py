# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path
from pydantic import BaseModel, Field
from config import TIME_WINDOW_0_END, TIME_WINDOW_1_END, TIME_WINDOW_0_START, TIME_WINDOW_1_START
from config import DATASET_DIR, OUTPUT_DIR
from entity.abstract_base import AbstractBase
from entity.scholar_basic_metric import ScholarBasicMetric
from utils.pd_common_util import contains_in


# class ScholarDifferenceAnalysisEntity(BaseModel):
#     id: str = Field(serialization_alias="学者唯一ID")
#     name: str = Field(serialization_alias="姓名")
#     career_length: int = Field(serialization_alias="学者职业生涯长度（2024-首篇论文发表年份+1）")
#     active_years: int = Field(serialization_alias="学者活跃年数（发表≥1篇论文的年份数）")
#     career_total_wos_publications: int = Field(serialization_alias="学者职业生涯总发文量")
#     h_index_tw_0_years: int = Field(serialization_alias=f"{TIME_WINDOW_0_END}年学者H指数（截止到{TIME_WINDOW_0_END}年）")
#     h_index_tw_1_years: int = Field(serialization_alias=f"{TIME_WINDOW_1_END}年学者H指数（截止到{TIME_WINDOW_1_END}年）")
#     total_publications_10_years: int = Field(serialization_alias="10年总发文量")
#     total_sci_publications_10_years: int = Field(serialization_alias="10年SCI论文总发文量")
#     total_meeting_publications_10_years: int = Field(serialization_alias="10年会议论文总发文量")
#     total_preprint_publications_10_years: int = Field(serialization_alias="10年预印本总发文量")


class ScholarDifferenceAnalysis(AbstractBase):
    __tbl_name__ = "差值分析"

    def __init__(self, basic_info_path: Path, data_path: Path):
        super().__init__()
        self.basic_info_path = basic_info_path
        self.data_path = data_path
    def calc(self) -> pd.DataFrame:

        data_columns = ["学者唯一ID", "姓名", "研究类型（1=基础科学，0=工程技术，2=前沿交叉）",
                        "时间窗口（0=获奖前5年，1=获奖后5年）", "学术生产力", "学术影响力", "综合分数"]
        df_data = pd.read_excel(self.data_path)[data_columns]
        df_data["学者唯一ID"] = df_data["学者唯一ID"].astype(str)
        print(df_data.head())

        info_columns = ["学者唯一ID", "分组ID", "关联ID", "学者类型（获奖人=1，0=对照学者）", "分组获奖人姓名", "姓名", "工作单位",
                        "出生年", "年龄（截至统计年份-2025年）", "研究领域"]
        df_basic_info = pd.read_excel(self.basic_info_path)[info_columns]
        df_basic_info["学者唯一ID"] = df_basic_info["学者唯一ID"].astype(str)
        print(df_basic_info.head())

        df = pd.merge(df_basic_info, df_data, on=["学者唯一ID", "姓名"], how="left")

        # 分组计算差值
        df_winner =
        for i, row in enumerate(df_winner.to_dict(orient="records"), start=1):

            # 时间窗口
            mask = (df["时间窗口（0=获奖前5年，1=获奖后5年）"]==tw) & (df["学者类型（获奖人=1，0=对照学者）"]==1)
            df_winner_tw = df[mask]
            time_windows = [0, 1]
            for tw in time_windows:

                print(f"{i:02}/{df_winner_tw.shape[0]}")
                scholar_id = row.get("学者唯一ID")
                scholar_name = row.get("姓名")
                group_id = row.get("分组ID")
                academic_prod = row.get("学术生产力")
                academic_impact = row.get("学术影响力")
                overall_score = row.get("综合分数")

                # 对照组
                mask_compare = (df["时间窗口（0=获奖前5年，1=获奖后5年）"] == tw) \
                                & (df["学者类型（获奖人=1，0=对照学者）"] == 0) \
                                & (df["分组获奖人姓名"] == scholar_name)
                df_compare = df[mask_compare]
                print(f"{i:02}/{df_winner_tw.shape[0]}: 时间窗口={tw}, 分组ID={group_id}, 获奖人={scholar_name}, "
                      f"学术生产力={academic_prod}, 学术影响力={academic_impact}, 综合分数{overall_score}")
                print("对照组: \n", df_compare)

                academic_prod_compare = df_compare["学术生产力"].mean()
                academic_impact_compare = df_compare["学术影响力"].mean()
                overall_score_compare = df_compare["综合分数"].mean()

                # 计算差值
                academic_prod_diff = academic_prod - academic_prod_compare
                academic_impact_diff = academic_impact - academic_impact_compare
                overall_score_diff = overall_score - overall_score_compare
                print("差值: " f"学术生产力={academic_prod_diff}, 学术影响力={academic_impact_diff}, 综合分数={overall_score_diff}")


if __name__ == "__main__":
    # 设置 Pandas 打印选项
    pd.set_option('display.max_rows', 20)  # 显示所有行
    pd.set_option('display.max_columns', None)  # 显示所有列
    pd.set_option('display.width', 800)  # 不折叠单元格
    pd.set_option('display.max_colwidth', None)  # 显示完整的单元格内容

    _input_file0 = DATASET_DIR.joinpath("S0.0-获奖人基础信息表.xlsx")
    _input_file1 = OUTPUT_DIR.joinpath(ScholarBasicMetric.__tbl_name__ + ".xlsx")
    _metric = ScholarDifferenceAnalysis(_input_file0, data_path=_input_file1)
    _metric.calc()
