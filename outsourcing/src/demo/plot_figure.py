# -*- coding: utf-8 -*-
import pandas as pd

from config import OUTPUT_DIR
from utils.plot_util import plot_line_chart, plot_grouped_bar

# 图3-7. 获奖人获奖前后5年学术能力变化
plot_line_chart(["获奖前5年", "获奖后5年"],
                y_data=[[27.16, 27.07],
                        [10.25, 9.00],
                        [16.91, 18.07]],
                labels=["综合分数", "学术生产力", "学术影响力"],
                output_path="image_3_7.png",
                show_point_text=True,
                fig_size=(6, 5))

# 图3-9. 获奖人在学术生产力和影响力上的相对成长速度
plot_grouped_bar(
    ["学术生产力", "学术影响力"],
    [[-1.25, 1.15],
             [1.25, -0.48]],
    fig_size=(7, 6),
    labels=["获奖人", "对照学者"],
    titles=None,
    x_label=None,
    y_label=None,
    output_path="image_3_8.png")


df = pd.read_excel(OUTPUT_DIR.joinpath("A2-评价指标数据集.xlsx"))
df = df[["学者类型（获奖人=1，0=对照学者）", "时间窗口（0=获奖前5年，1=获奖后5年）", "综合分数", "学术生产力", "学术影响力"]]
df_grouped_means = df \
    .groupby(by=["学者类型（获奖人=1，0=对照学者）", "时间窗口（0=获奖前5年，1=获奖后5年）"])[["学术生产力", "学术影响力", "综合分数"]] \
    .mean()\
    .round(2)\
    .reset_index()
print(df_grouped_means)

# 图4-3. 获奖人与对照学者获奖前后5年各指标变化情况
print(df_grouped_means)
df_scholar = df_grouped_means[df_grouped_means["学者类型（获奖人=1，0=对照学者）"]==1]
print(df_scholar)
plot_line_chart(["获奖前5年", "获奖后5年"],
                y_data=[[27.16, 27.07],
                        [10.25, 9.00],
                        [16.91, 18.07]],
                labels=["综合分数", "学术生产力", "学术影响力"],
                output_path="image_3_7.png",
                show_point_text=True,
                fig_size=(6, 5))

# 图4-3. 获奖人与对照学者获奖前后5年各指标变化情况
# 定义列名常量，方便代码阅读
COL_TYPE = "学者类型（获奖人=1，0=对照学者）"
COL_TIME = "时间窗口（0=获奖前5年，1=获奖后5年）"

# 遍历三个指标
for col in ["综合分数", "学术生产力", "学术影响力"]:
    print(f"正在处理指标: {col}...")

    # 1. 提取【处理组】（获奖人 Type=1）的数据，并按时间排序
    # 结果类似于: [27.16, 27.07]
    y_treatment = df_grouped_means[df_grouped_means[COL_TYPE] == 1] \
        .sort_values(by=COL_TIME)[col].tolist()

    # 2. 提取【对照组】（对照学者 Type=0）的数据，并按时间排序
    # 结果类似于: [23.35, 24.12]
    y_control = df_grouped_means[df_grouped_means[COL_TYPE] == 0] \
        .sort_values(by=COL_TIME)[col].tolist()

    # 3. 打印检查数据是否正确
    print(f"  处理组数据: {y_treatment}")
    print(f"  对照组数据: {y_control}")

    file_name = f"4-3-{col}.png"
    plot_line_chart(
        x_data=["获奖前5年", "获奖后5年"],
        y_data=[y_treatment, y_control],  # 填入提取出来的两组数据
        labels=["处理组", "对照组"],  # 图例
        y_label=col,  # Y轴标签
        output_path=file_name,  # 动态文件名
        show_point_text=True,
        fig_size=(3, 5),
        legend_loc='lower right',
    )
    print(f"  已保存图片: {file_name}\n")
