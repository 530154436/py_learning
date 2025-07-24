# -*- coding: utf-8 -*-
import pandas as pd
from matplotlib import pyplot as plt
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from typing import Optional, List


def plot_line_chart(
    x_data: List[str],
    y_data: List[List[float]],
    labels: Optional[List[str]] = None,
    title: Optional[str] = None,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    output_path: str = "line_chart.png"
):
    """
    绘制折线图并保存为图片
    :param x_data: X轴数据（字符串列表）
    :param y_data: Y轴数据（二维浮点数列表）
    :param labels: 图例标签（可选）
    :param title: 图表标题（可选）
    :param x_label: X轴标签（可选）
    :param y_label: Y轴标签（可选）
    :param output_path: 输出图片路径
    """
    # 设置中文字体支持
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 创建图表
    fig, ax = plt.subplots(figsize=(8, 5))

    # 绘制折线
    for i, y in enumerate(y_data):
        label = None if labels is None else labels[i]
        ax.plot(x_data, y, label=label, marker='o', linewidth=2)

    # 设置图表属性
    if title:
        ax.set_title(title, fontsize=14)
    if y_label:
        ax.set_ylabel(y_label)
    if x_label:
        ax.set_xlabel(x_label)
    # 自动调整X轴刻度
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # 保持X轴为整数
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    plt.tight_layout()  # 自动调整边距

    # 保存图片
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def dataframe_to_chart(
    df: DataFrame,
    x_col: str,
    y_cols: List[str],
    title: str = None,
    image_path: str = "line_chart.png"
):
    """
    从 DataFrame 生成折线图并保存
    :param df: 输入数据（DataFrame）
    :param x_col: X轴列名
    :param y_cols: Y轴列名列表
    :param title: 标题
    :param image_path: 输出图片路径
    """
    # 检查列是否存在
    if x_col not in df.columns or any(col not in df.columns for col in y_cols):
        raise ValueError("指定的列不存在于 DataFrame 中")

    # 提取数据
    x_data = df[x_col].astype(str).tolist()
    y_data = [df[col].tolist() for col in y_cols]

    # 调用绘图函数
    plot_line_chart(
        x_data=x_data,
        y_data=y_data,
        labels=y_cols,
        title=title,
        x_label=x_col,
        y_label=y_cols[0],
        output_path=image_path
    )
