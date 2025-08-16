# -*- coding: utf-8 -*-
"""
Axes(坐标轴 / 绘图区域)：这是Figure上实际进行绘图的区域。它通常包含：
    坐标轴(Axes)：X轴和Y轴（有时还有Z轴）。
    数据(Data)：你绘制的线条、散点、柱状图等。
    刻度(Ticks)：坐标轴上的小标记。
    标签(Labels)：X轴和Y轴的名称（xlabel, ylabel）。
    标题(Title)：这个子图的标题。
    图例(Legend)：解释图中不同线条或颜色的含义。
    网格(Grid)：可选的背景网格线。
"""
from functools import reduce

import numpy as np
from matplotlib.axes import Axes
from matplotlib.container import BarContainer
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from typing import Optional, List, Iterable

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


#--------------------------------------------------------------------------
# 条形图(bar): 支持单组、多组
#--------------------------------------------------------------------------
def  _plot_bar(
    ax: Axes,
    x_data: List[str],
    y_data: List[List[float]],
    title: Optional[str] = None,
    labels: Optional[List[str]] = None,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    y_min: Optional[float] = 0,
    y_max: Optional[float] = None,
    bar_width_factor: float = 0.5,  # 控制条形总宽度占每组宽度的比例
    group_padding: float = 0.2,  # 组与组之间的间距比例
) -> List[BarContainer]:
    """
    绘制分组条形图并保存为图片
    :param ax: 坐标轴
    :param x_data: X轴数据 [m,]
    :param y_data: Y轴数据 [m, n]
    :param labels: 图例标签 [n,]
    """
    n_groups = len(x_data)
    n_datasets = len(y_data)
    labels = [f"Dataset {i + 1}" for i in range(n_datasets)] if labels is None else labels

    # 计算条形宽度和组间间距
    total_width = bar_width_factor - (n_datasets - 1) * group_padding / n_datasets
    bar_width = min(total_width / n_datasets, 0.2)
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
    if y_max:
        ax.set_ylim(y_min, y_max)
        # ax.set_yticks(np.arange(0, y_max + 1, y_step))

    # ax.legend(bbox_to_anchor=(0.5, -0.08), loc='upper center', ncol=len(labels))
    ax.grid(axis='y', linestyle='--', alpha=0.7, linewidth=0.5)
    return bars

def plot_grouped_bar(
    x_data: List[str],
    *y_datas: List[List[float]],
    titles: Optional[List[str]] = None,
    labels: Optional[List[str]] = None,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    fig_size: tuple = (8, 6),
    output_path: str = "bar_chart.png",
):
    if titles:
        assert len(y_datas) == len(titles)
    assert len(y_datas[0]) == len(labels)
    assert len(y_datas[0][0]) == len(x_data)

    n_rows, n_cols = 1, len(y_datas)
    fig, axes_list = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=fig_size)
    if not isinstance(axes_list, Iterable):
        axes_list = [axes_list]

    # 计算全局最大值，用于统一Y轴范围
    all_data = list(reduce(lambda x, y: x + y, y_datas))
    y_max = max(max(data) for data in all_data)
    y_step = y_max * 0.2

    # 多个子图
    all_bars = []
    for i, (axes, y_data) in enumerate(zip(axes_list, y_datas)):
        title = titles[i] if titles else None
        bars = _plot_bar(axes, x_data, y_data=y_data, title=title,
                         labels=labels, x_label=x_label, y_label=y_label,
                         y_min=0, y_max=y_max + y_step)
        all_bars.extend(bars)

    # 共享图例，放在最下方
    fig.legend(labels=labels, loc='lower center', ncol=len(labels), bbox_to_anchor=(0.5, 0.03))

    # 调整布局，为底部图例留出空间
    plt.tight_layout(rect=(0.0, 0.1, 1.0, 0.95))  # [left, bottom, right, top]
    plt.savefig(output_path, dpi=350, bbox_inches='tight')
    plt.close()
    print(f"分组条形图已保存至: {output_path}")


if __name__ == '__main__':
    plot_grouped_bar(["A", "B", "C"],
                     [[10, 20, 30], [15, 25, 35]],
                     labels=["获奖前5年", "获奖后5年"],
                     titles=["示例分组条形图"])
    plot_grouped_bar(
        ["A1", "A2", "A3"],
        [[30, 5, 5], [30, 5, 5]],
        [[10, 5, 5], [30, 5, 5]],
        labels=["何旭华", "刘钢"],
        titles=["获奖前5年", "获奖后5年"],
        fig_size=(10, 6),
        output_path="shared_y_legend_bottom.png"
    )
