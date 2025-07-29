# -*- coding: utf-8 -*-
import json
import pandas as pd
from pathlib import Path
from pydantic import BaseModel, Field
from typing import OrderedDict
from config import DATASET_DIR, OUTPUT_DIR
from entity.abstract_base import AbstractBase
from entity.s2_2_scholar_basic_metric import ScholarBasicMetric


class ScholarDifferenceAnalysisEntity(BaseModel):
    id: str = Field(serialization_alias="学者唯一ID")
    name: str = Field(serialization_alias="姓名")
    group_id: int = Field(serialization_alias="分组ID")
    scholar_type: int = Field(serialization_alias="学者类型（获奖人=1，0=对照学者）")
    academic_prod_0: float = Field(serialization_alias="学术生产力0")
    academic_impact_0: float = Field(serialization_alias="学术影响力0")
    overall_score_0: float = Field(serialization_alias="综合分数0")
    academic_prod_compare_0: float = Field(serialization_alias="对照学者均值-学术生产力0")
    academic_impact_compare_0: float = Field(serialization_alias="对照学者均值-学术影响力0")
    overall_score_compare_0: float = Field(serialization_alias="对照学者均值-综合分数0")
    academic_prod_diff_0: float = Field(serialization_alias="差值-学术生产力0")
    academic_impact_diff_0: float = Field(serialization_alias="差值-学术影响力0")
    overall_score_diff_0: float = Field(serialization_alias="差值-综合分数0")
    academic_prod_1: float = Field(serialization_alias="学术生产力1")
    academic_impact_1: float = Field(serialization_alias="学术影响力1")
    overall_score_1: float = Field(serialization_alias="综合分数1")
    academic_prod_compare_1: float = Field(serialization_alias="对照学者均值-学术生产力1")
    academic_impact_compare_1: float = Field(serialization_alias="对照学者均值-学术影响力1")
    overall_score_compare_1: float = Field(serialization_alias="对照学者均值-综合分数1")
    academic_prod_diff_1: float = Field(serialization_alias="差值-学术生产力1")
    academic_impact_diff_1: float = Field(serialization_alias="差值-学术影响力1")
    overall_score_diff_1: float = Field(serialization_alias="差值-综合分数1")
    growth_pattern: str = Field(serialization_alias="成长模式")


class GrowthPattern(object):
    szlxx: str = "始终领先型"
    szlhx: str = "始终落后型"
    ksczx: str = "快速成长型"
    czfhx: str = "成长放缓型"


class ScholarDifferenceAnalysis(AbstractBase):
    __tbl_name__ = "差值分析"

    def __init__(self, basic_info_path: Path, data_path: Path):
        super().__init__()
        self.basic_info_path = basic_info_path
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

        # 融合基础信息和计算结果
        df = pd.merge(df_basic_info, df_data, on=["学者唯一ID", "姓名"], how="left")

        # 分组计算差值
        df_winner = df_basic_info[df_basic_info["学者类型（获奖人=1，0=对照学者）"] == 1]
        results = []
        for i, row in enumerate(df_winner.to_dict(orient="records"), start=1):
            scholar_id = row.get("学者唯一ID")
            scholar_name = row.get("姓名")
            group_id = row.get("分组ID")
            scholar_type = row.get("学者类型（获奖人=1，0=对照学者）")
            result = OrderedDict({
                "id": scholar_id,
                "name": scholar_name,
                "group_id": group_id,
                "scholar_type": scholar_type,
            })

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

                result[f"academic_prod_{tw}"] = academic_prod
                result[f"academic_impact_{tw}"] = academic_impact
                result[f"overall_score_{tw}"] = overall_score
                result[f"academic_prod_compare_{tw}"] = academic_prod_compare
                result[f"academic_impact_compare_{tw}"] = academic_impact_compare
                result[f"overall_score_compare_{tw}"] = overall_score_compare
                result[f"academic_prod_diff_{tw}"] = academic_prod_diff
                result[f"academic_impact_diff_{tw}"] = academic_impact_diff
                result[f"overall_score_diff_{tw}"] = overall_score_diff

            # 计算成长模式
            result["growth_pattern"] = self.calc_growth_pattern(overall_score_diff_0=result["overall_score_diff_0"],
                                                                overall_score_diff_1=result["overall_score_diff_1"])

            results.append(result)

        data = []
        for result in results:
            entity = ScholarDifferenceAnalysisEntity(**result)
            data.append(entity.model_dump(mode="json", by_alias=True))
        self.save_to_excel(pd.DataFrame(data))


if __name__ == "__main__":
    # 设置 Pandas 打印选项
    pd.set_option('display.max_rows', 100)  # 显示所有行
    pd.set_option('display.max_columns', None)  # 显示所有列
    pd.set_option('display.width', 2000)  # 不折叠单元格
    pd.set_option('display.max_colwidth', None)  # 显示完整的单元格内容

    _input_file0 = DATASET_DIR.joinpath("S0.0-获奖人基础信息表.xlsx")
    _input_file1 = OUTPUT_DIR.joinpath(ScholarBasicMetric.__tbl_name__ + ".xlsx")
    _metric = ScholarDifferenceAnalysis(_input_file0, data_path=_input_file1)
    _metric.calc()
