# -*- coding: utf-8 -*-
import json
import pandas as pd
from pathlib import Path
from dataclasses import dataclass, field
from dataclasses_json import config
from analysis import GrowthPattern
from analysis.A2_scholar_basic_metric_index import ScholarBasicMetricIndex
from analysis.abstract_base import AbstractBase
from analysis.scholar_comparison import ScholarComparisonEntity
from config import DATASET_DIR, OUTPUT_DIR


@dataclass
class ScholarDifferenceAnalysisEntity(ScholarComparisonEntity):
    """
    学者差异分析实体：包含获奖人与对照组在两个时间窗口的得分对比
    """

    # 时间窗口 0（如获奖前）
    academic_prod_0: float = field(metadata=config(field_name="学术生产力0"))
    academic_impact_0: float = field(metadata=config(field_name="学术影响力0"))
    overall_score_0: float = field(metadata=config(field_name="综合分数0"))

    academic_prod_compare_0: float = field(metadata=config(field_name="对照学者均值-学术生产力0"))
    academic_impact_compare_0: float = field(metadata=config(field_name="对照学者均值-学术影响力0"))
    overall_score_compare_0: float = field(metadata=config(field_name="对照学者均值-综合分数0"))

    academic_prod_diff_0: float = field(metadata=config(field_name="差值-学术生产力0"))
    academic_impact_diff_0: float = field(metadata=config(field_name="差值-学术影响力0"))
    overall_score_diff_0: float = field(metadata=config(field_name="差值-综合分数0"))

    # 时间窗口 1（如获奖后）
    academic_prod_1: float = field(metadata=config(field_name="学术生产力1"))
    academic_impact_1: float = field(metadata=config(field_name="学术影响力1"))
    overall_score_1: float = field(metadata=config(field_name="综合分数1"))

    academic_prod_compare_1: float = field(metadata=config(field_name="对照学者均值-学术生产力1"))
    academic_impact_compare_1: float = field(metadata=config(field_name="对照学者均值-学术影响力1"))
    overall_score_compare_1: float = field(metadata=config(field_name="对照学者均值-综合分数1"))

    academic_prod_diff_1: float = field(metadata=config(field_name="差值-学术生产力1"))
    academic_impact_diff_1: float = field(metadata=config(field_name="差值-学术影响力1"))
    overall_score_diff_1: float = field(metadata=config(field_name="差值-综合分数1"))

    # 成长模式
    growth_pattern: str = field(metadata=config(field_name="成长模式"))


class ScholarDifferenceAnalysis(AbstractBase):
    __tbl_name__ = "A3-差值分析数据集"

    def __init__(self, comparison_path: Path, data_path: Path):
        super().__init__()
        self.comparison_path = comparison_path
        self.data_path = data_path

    @staticmethod
    def calc_growth_pattern(overall_score_diff_0: float, overall_score_diff_1: float) -> str:
        """
        成长模式	    内涵	                                    数据表现
        始终领先型	获奖人获奖前后表现均优于对照学者	            获奖前后差值均大于0
        始终落后型	获奖人获奖前后表现均不如对照学者	            获奖前后差值均小于0
        快速成长型	获奖人获奖前不如对照学者、获奖后优于对照学者	获奖前差值小于0、获奖后大于0
        成长放缓型	获奖人获奖前优于对照学者、获奖后不如对照学者	获奖前差值大于0、获奖后小于0
        """
        if overall_score_diff_0 > 0 and overall_score_diff_1 > 0:
            return GrowthPattern.szlxx
        elif overall_score_diff_0 < 0 and overall_score_diff_1 < 0:
            return GrowthPattern.szlhx
        elif overall_score_diff_0 < 0 and overall_score_diff_1 > 0:
            return GrowthPattern.ksczx
        elif overall_score_diff_0 > 0 and overall_score_diff_1 < 0:
            return GrowthPattern.czfhx
        else:
            raise ValueError("计算错误：找不到对应的成长模式。")

    def calc(self) -> pd.DataFrame:
        # 融合基础信息和计算结果
        df_comparison = pd.read_excel(self.comparison_path)
        df = pd.read_excel(self.data_path)
        print(df)

        # 分组计算差值
        df_winner = df_comparison[df_comparison["学者类型（获奖人=1，0=对照学者）"] == 1]
        results = []
        for i, row in enumerate(df_winner.to_dict(orient="records"), start=1):
            scholar_name = row.get("姓名")
            group_id = row.get("分组ID")

            # 时间窗口
            for tw in [0, 1]:
                # 获奖人
                mask = (df["时间窗口（0=获奖前5年，1=获奖后5年）"] == tw) & \
                       (df["分组ID"] == group_id) & \
                       (df["学者类型（获奖人=1，0=对照学者）"] == 1)
                df_scholar_result_tw = df[mask][["姓名", "学术生产力", "学术影响力", "综合分数"]].to_dict(orient="records")
                assert len(df_scholar_result_tw) == 1
                academic_prod = df_scholar_result_tw[0].get("学术生产力")
                academic_impact = df_scholar_result_tw[0].get("学术影响力")
                overall_score = df_scholar_result_tw[0].get("综合分数")
                print(f"{i:02}/{df_winner.shape[0]}: 时间窗口={tw}, 分组ID={group_id}, 获奖人={scholar_name}, "
                      f"学术生产力={academic_prod}, 学术影响力={academic_impact}, 综合分数{overall_score}")

                # 对照组
                mask_compare = (df["时间窗口（0=获奖前5年，1=获奖后5年）"] == tw) & \
                               (df["分组ID"] == group_id) & \
                               (df["学者类型（获奖人=1，0=对照学者）"] == 0)
                df_compare_tw = df[mask_compare][["姓名", "学术生产力", "学术影响力", "综合分数"]]
                assert df_compare_tw.shape[0] == 4
                print("对照组:\n")
                print(df_compare_tw)

                academic_prod_compare = df_compare_tw["学术生产力"].mean()
                academic_impact_compare = df_compare_tw["学术影响力"].mean()
                overall_score_compare = df_compare_tw["综合分数"].mean()

                # 计算差值
                academic_prod_diff = academic_prod - academic_prod_compare
                academic_impact_diff = academic_impact - academic_impact_compare
                overall_score_diff = overall_score - overall_score_compare
                print("差值: "f"学术生产力={academic_prod_diff}, 学术影响力={academic_impact_diff}, 综合分数={overall_score_diff}")
                print()

                row[f"academic_prod_{tw}"] = academic_prod
                row[f"academic_impact_{tw}"] = academic_impact
                row[f"overall_score_{tw}"] = overall_score
                row[f"academic_prod_compare_{tw}"] = academic_prod_compare
                row[f"academic_impact_compare_{tw}"] = academic_impact_compare
                row[f"overall_score_compare_{tw}"] = overall_score_compare
                row[f"academic_prod_diff_{tw}"] = academic_prod_diff
                row[f"academic_impact_diff_{tw}"] = academic_impact_diff
                row[f"overall_score_diff_{tw}"] = overall_score_diff

            # 计算成长模式
            row["growth_pattern"] = self.calc_growth_pattern(overall_score_diff_0=row["overall_score_diff_0"],
                                                             overall_score_diff_1=row["overall_score_diff_1"])
            results.append(row)

        self.export_to_excel(results, clazz=ScholarDifferenceAnalysisEntity)


if __name__ == "__main__":
    _input_file0 = DATASET_DIR.joinpath("S2.2-学者关联信息表-对照分组.xlsx")
    _input_file1 = OUTPUT_DIR.joinpath(ScholarBasicMetricIndex.__tbl_name__ + ".xlsx")
    _metric = ScholarDifferenceAnalysis(_input_file0, data_path=_input_file1)
    _metric.calc()
