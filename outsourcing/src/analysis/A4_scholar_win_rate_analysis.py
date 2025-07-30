# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path
from dataclasses import dataclass, field
from dataclasses_json import config
from pandas import DataFrame
from analysis.abstract_base import AbstractBase
from analysis.scholar_comparison import ScholarComparisonEntity
from analysis.A2_scholar_basic_metric_index import ScholarBasicMetricIndex
from config import DATASET_DIR, OUTPUT_DIR


@dataclass
class ScholarDifferenceAnalysisEntity(ScholarComparisonEntity):
    """
    学者差异分析实体，包含多个指标及其排名、胜率
    所有字段使用 dataclass + metadata 风格，与父类保持一致
    """
    academic_prod_0: float = field(metadata=config(field_name="学术生产力0"))
    academic_impact_0: float = field(metadata=config(field_name="学术影响力0"))
    overall_score_0: float = field(metadata=config(field_name="综合分数0"))
    academic_prod_0_rank: int = field(metadata=config(field_name="排名-学术生产力0"))
    academic_impact_0_rank: int = field(metadata=config(field_name="排名-学术影响力0"))
    overall_score_0_rank: int = field(metadata=config(field_name="排名-综合分数0"))
    academic_prod_0_win_rate: str = field(metadata=config(field_name="胜率-学术生产力0"))
    academic_impact_0_win_rate: str = field(metadata=config(field_name="胜率-学术影响力0"))
    overall_score_0_win_rate: str = field(metadata=config(field_name="胜率-综合分数0"))

    academic_prod_1: float = field(metadata=config(field_name="学术生产力1"))
    academic_impact_1: float = field(metadata=config(field_name="学术影响力1"))
    overall_score_1: float = field(metadata=config(field_name="综合分数1"))
    academic_prod_1_rank: int = field(metadata=config(field_name="排名-学术生产力1"))
    academic_impact_1_rank: int = field(metadata=config(field_name="排名-学术影响力1"))
    overall_score_1_rank: int = field(metadata=config(field_name="排名-综合分数1"))
    academic_prod_1_win_rate: str = field(metadata=config(field_name="胜率-学术生产力1"))
    academic_impact_1_win_rate: str = field(metadata=config(field_name="胜率-学术影响力1"))
    overall_score_1_win_rate: str = field(metadata=config(field_name="胜率-综合分数1"))


class ScholarWinRateAnalysis(AbstractBase):
    __tbl_name__ = "A4-胜率分析数据集"

    def __init__(self, comparison_path: Path, data_path: Path):
        super().__init__()
        self.comparison_path = comparison_path
        self.data_path = data_path

    @staticmethod
    def calc_win_rate(rank: int) -> str:
        return f"{(5 - rank) * 25}%"

    def calc(self):

        # 融合基础信息和计算结果
        df_comparison = pd.read_excel(self.comparison_path)
        df = pd.read_excel(self.data_path)  # 已经包含分组+指标信息，不需要融合
        print(df)

        # 分组计算差值
        df_winner = df_comparison[df_comparison["学者类型（获奖人=1，0=对照学者）"] == 1]
        results = []
        for i, row in enumerate(df_winner.to_dict(orient="records"), start=1):
            scholar_id = row.get("学者唯一ID")
            scholar_name = row.get("姓名")
            group_id = row.get("分组ID")

            # 时间窗口
            for tw in [0, 1]:
                print(f"{i:02}/{df_winner.shape[0]}: 时间窗口={tw}, 分组ID={group_id}, 获奖人={scholar_name}")

                columns = ["姓名", "学者类型（获奖人=1，0=对照学者）", "学术生产力", "学术影响力", "综合分数"]

                # 获奖人 + 对照组
                mask = (df["时间窗口（0=获奖前5年，1=获奖后5年）"] == tw) & \
                       (df["分组ID"] == group_id)
                df_scholar_result_tw: DataFrame = df[mask][columns]
                df_scholar_result_tw = df_scholar_result_tw.copy().reset_index(drop=True)
                assert df_scholar_result_tw.shape[0] == 5

                # 原始数据：学术生产力、学术影响力、综合分数
                df_scholar_result_tw[f"academic_prod_{tw}"] = df_scholar_result_tw["学术生产力"]
                df_scholar_result_tw[f"academic_impact_{tw}"] = df_scholar_result_tw["学术影响力"]
                df_scholar_result_tw[f"overall_score_{tw}"] = df_scholar_result_tw["综合分数"]

                # 分别排序：学术生产力、学术影响力、综合分数
                df_scholar_result_tw[f"academic_prod_{tw}_rank"] = df_scholar_result_tw["学术生产力"].rank(method='max', ascending=False).astype(int)
                df_scholar_result_tw[f"academic_impact_{tw}_rank"] = df_scholar_result_tw["学术影响力"].rank(method='max', ascending=False).astype(int)
                df_scholar_result_tw[f"overall_score_{tw}_rank"] = df_scholar_result_tw["综合分数"].rank(method='max', ascending=False).astype(int)

                # 计算胜率
                df_scholar_result_tw[f"academic_prod_{tw}_win_rate"] = df_scholar_result_tw[f"academic_prod_{tw}_rank"].apply(lambda x: self.calc_win_rate(x))
                df_scholar_result_tw[f"academic_impact_{tw}_win_rate"] = df_scholar_result_tw[f"academic_impact_{tw}_rank"].apply(lambda x: self.calc_win_rate(x))
                df_scholar_result_tw[f"overall_score_{tw}_win_rate"] = df_scholar_result_tw[f"overall_score_{tw}_rank"].apply(lambda x: self.calc_win_rate(x))

                # 取获奖人信息
                winners = df_scholar_result_tw[df_scholar_result_tw["学者类型（获奖人=1，0=对照学者）"] == 1]
                winners = winners.drop(columns=columns).to_dict(orient="records")
                assert len(winners) == 1
                row.update(winners[0])
            results.append(row)
        self.export_to_excel(results, clazz=ScholarDifferenceAnalysisEntity)


if __name__ == "__main__":
    _input_file0 = DATASET_DIR.joinpath("S2.2-学者关联信息表-对照分组.xlsx")
    _input_file1 = OUTPUT_DIR.joinpath(ScholarBasicMetricIndex.__tbl_name__ + ".xlsx")
    _metric = ScholarWinRateAnalysis(_input_file0, data_path=_input_file1)
    _metric.calc()
