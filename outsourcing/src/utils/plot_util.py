# -*- coding: utf-8 -*-
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from typing import Optional, List

# 设置中文字体（防止中文乱码）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号


def plot_line_chart(
    x_data: List[str],
    y_data: List[List[float]],
    labels: Optional[List[str]] = None,
    title: Optional[str] = None,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    output_path: str = "line_chart.png",
    fig_size: tuple=(8, 5)
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
    :param fig_size: 图片大小
    """
    # 创建图表
    fig, ax = plt.subplots(figsize=fig_size)

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


def plot_line_char_by_df(
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


def plot_group_bar_chart(
        x_data: List[str],
        y_data: List[List[float]],
        labels: Optional[List[str]] = None,
        title: Optional[str] = None,
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        output_path: str = "bar_chart.png",
        fig_size: tuple = (8, 6),
        y_min: float = 0,
        y_max: Optional[float] = None,
        bar_width_factor: float = 0.5,  # 控制条形总宽度占每组宽度的比例
        group_padding: float = 0.2  # 组与组之间的间距比例
):
    """
    绘制分组条形图并保存为图片
    """
    fig, ax = plt.subplots(figsize=fig_size)

    n_groups = len(x_data)
    n_datasets = len(y_data)

    if labels is None:
        labels = [f"Dataset {i + 1}" for i in range(n_datasets)]

    # 计算条形宽度和组间间距
    total_width = bar_width_factor - (n_datasets - 1) * group_padding / n_datasets
    bar_width = min(total_width / n_datasets, 0.25)
    indices = range(n_groups)

    bars = []
    for i, (data, label) in enumerate(zip(y_data, labels)):
        offset = i * (bar_width + group_padding / n_datasets) - (total_width / 2)
        bar = ax.bar([0.055 + x + offset for x in indices], data, width=bar_width, label=label)
        bars.append(bar)

        for rect in bar:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    if title:
        ax.set_title(title, fontsize=14)
    if y_label:
        ax.set_ylabel(y_label)
    if x_label:
        ax.set_xlabel(x_label)
    ax.set_xticks(indices)
    ax.set_xticklabels(x_data)

    y_ticks = ax.get_yticks()
    y_step = y_ticks[1] - y_ticks[0] if len(y_ticks) > 1 else 1.0
    if y_max is None:
        y_max = max(max(data) for data in y_data) + y_step
    ax.set_ylim(y_min, y_max)

    ax.legend(bbox_to_anchor=(0.5, -0.08), loc='upper center', ncol=len(labels))
    ax.grid(axis='y', linestyle='--', alpha=0.7, linewidth=0.5)
    plt.tight_layout(rect=[0, 0.1, 1, 1])

    plt.savefig(output_path, dpi=350, bbox_inches='tight')
    plt.close()
    print(f"条形图已保存至: {output_path}")