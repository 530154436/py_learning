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
from typing import Optional, List, Iterable, Union

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
    fig_size: tuple=(8, 5),
    y_min: Optional[Union[float, int]] = None,
    y_max: Optional[Union[float, int]] = None,
    auto_y_limit: bool = True,
):
    """
    绘制折线图并保存为图片
    :param x_data: X轴数据（字符串列表） [m,]
    :param y_data: Y轴数据（二维浮点数列表） [n, m]
    :param labels: 图例标签（可选） [n, ]
    :param title: 图表标题（可选）
    :param x_label: X轴标签（可选）
    :param y_label: Y轴标签（可选）
    :param output_path: 输出图片路径
    :param fig_size: 图片大小
    :param y_min: Y轴最小值
    :param y_max: Y轴最大值
    :param auto_y_limit: 自动计算 Y轴最大最小值
    """
    # 创建图表
    fig, ax = plt.subplots(figsize=fig_size)

    # 绘制折线
    for i, y in enumerate(y_data):
        label = None if labels is None else labels[i]
        ax.plot(x_data, y, label=label, marker='o', linewidth=2)

    # 计算全局最大值，用于统一X轴、Y轴范围
    if auto_y_limit:
        y_min = min(min(data) for data in y_data)
        y_max = max(max(data) for data in y_data)
        y_min = min(y_min, 0) if y_min > 0 else y_min + y_min * 0.4
        y_max = max(y_max, 0) if y_max < 0 else y_max + y_max * 0.4
    ax.set_ylim(y_min, y_max)

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
    ax.legend(labels=labels, loc='upper center', ncol=len(labels), bbox_to_anchor=(0.5, 1.0), fontsize=14)
    plt.tight_layout(rect=(0, 0, 1, 0.95))  # 预留顶部空间以适应图例

    # 保存图片
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


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
    fontsize: int = 14,
):
    """
    绘制分组条形图并保存为图片
    :param ax: 坐标轴
    :param x_data: X轴数据 [m,]
    :param y_data: Y轴数据 [n, m]
    :param labels: 分组标签（图例） [n,]
    """
    num_groups = len(y_data)
    num_items = len(x_data)
    labels = [f"Group {i + 1}" for i in range(len(y_data))] if labels is None else labels

    # 动态计算 bar_width, group_gap, 和 bar_gap
    bar_width = min(0.8 / num_groups, 0.2)  # 最大宽度为0.2，以避免单个分组时条形过宽
    bar_gap = bar_width * 0.3  # 单位间隔，可以根据需求调整
    group_gap = 0.3  # 计算组间空隙大小

    # 初始化每一组 x 的起始位置
    x_pos = list(map(float, range(len(x_data))))
    for i, x in enumerate(x_pos):
        if i > 0:
            x = max(x, x_pos[i-1] + num_groups * (bar_width + bar_gap) + group_gap)
        x_pos[i] = x
    x_pos = np.array(x_pos)
    # print(x_pos)

    for i, (data, label) in enumerate(zip(y_data, labels)):
        pos = x_pos + (i * (bar_width + bar_gap))  # 根据组索引、组内间隔和组间间隔计算位置
        # print(i, label, pos)
        bar = ax.bar(pos, data, width=bar_width, label=label)
        for rect in bar:
            height = rect.get_height()
            if height >= 0:
                va = 'bottom'
                offset = 3
            else:
                va = 'top'
                offset = -3
            ax.annotate(f'{height:.2f}' if isinstance(height, float) else f'{height}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, offset),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va=va,
                        fontsize=12)
    ax.set_xticks(x_pos + ((len(y_data) - 1) / 2) * bar_width)
    ax.set_xticklabels(x_data, fontsize=12)

    if title:
        ax.set_title(title, fontsize=fontsize)
    if y_label:
        ax.set_ylabel(y_label, fontsize=fontsize)
    if x_label:
        ax.set_xlabel(x_label, fontsize=fontsize)
    if y_min or y_max:
        ax.set_ylim(y_min, y_max)
        # ax.set_yticks(np.arange(0, y_max + 1, y_step))
    ax.tick_params(axis='y', labelsize=fontsize)

    # ax.legend(bbox_to_anchor=(0.5, -0.08), loc='upper center', ncol=len(labels))
    ax.grid(axis='y', linestyle='--', alpha=0.7, linewidth=0.5)

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

    # 计算全局最大值，用于统一X轴、Y轴范围
    all_data = list(reduce(lambda x, y: x + y, y_datas))
    y_max = max(max(data) for data in all_data)
    y_min = min(min(data) for data in all_data)
    y_min = min(y_min, 0) if y_min > 0 else y_min + y_min * 0.4
    y_max = max(y_max, 0) if y_max < 0 else y_max + y_max * 0.4

    # 多个子图
    for i, (axes, y_data) in enumerate(zip(axes_list, y_datas)):
        title = titles[i] if titles else None
        _plot_bar(axes, x_data, y_data=y_data, title=title,
                  labels=labels, x_label=x_label, y_label=y_label,
                  y_min=y_min, y_max=y_max)

    # 共享图例，放在最下方
    fig.legend(labels=labels, loc='lower center', ncol=len(labels), bbox_to_anchor=(0.5, 0.03), fontsize=14)

    # 调整布局，为底部图例留出空间
    plt.tight_layout(rect=(0.0, 0.1, 1.0, 0.95))  # [left, bottom, right, top]
    plt.savefig(output_path, dpi=350, bbox_inches='tight')
    plt.close()
    print(f"分组条形图已保存至: {output_path}")


if __name__ == '__main__':
    plot_line_chart(["A", "B", "C"],
                    y_data=[[10, 20, 30],
                            [5, 25, 35]],
                    labels=["获奖前5年", "获奖后5年"],
                    output_path="line_chart.png")
    plot_grouped_bar(["A", "B", "C"],
                     [[10, 20, 30]],
                     labels=["获奖前5年"],
                     titles=["示例分组条形图"],
                     output_path="bar_1.png")
    plot_grouped_bar(["A", "B", "C"],
                     [[10, 20, 30],
                              [15, 25, 35]],
                     labels=["获奖前5年", "获奖后5年"],
                     titles=["示例分组条形图"],
                     output_path="bar_2.png")
    plot_grouped_bar(
        ["A1", "A2", "A3"],
        [[30, 5, 5], [30, 5, 5]],
        [[10, 5, 5], [30, 5, 5]],
        labels=["何旭华", "刘钢"],
        titles=["获奖前5年", "获奖后5年"],
        fig_size=(12, 6),
        output_path="bar_3.png"
    )
