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


def plot_grouped_bar(
    x_data: List[str],
    y_data: List[List[float]],
    labels: Optional[List[str]] = None,
    title: Optional[str] = None,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    fig_size: tuple = (8, 6),
    bar_width_factor: float = 0.5,  # 控制条形总宽度占每组宽度的比例
    group_padding: float = 0.16,  # 组与组之间的间距比例
    output_path: str = "bar_chart.png",
):
    """
    绘制分组条形图并保存为图片
    :param x_data: X轴数据 [m,]
    :param y_data: Y轴数据 [m, n]
    :param labels: 图例(分组标签) [n,]
    """
    fig, ax = plt.subplots(figsize=fig_size)

    n_groups = len(x_data)
    n_datasets = len(y_data)

    if labels is None:
        labels = [f"Dataset {i + 1}" for i in range(n_datasets)]

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

    y_ticks = ax.get_yticks()
    y_step = y_ticks[1] - y_ticks[0] if len(y_ticks) > 1 else 1.0
    y_max = max(max(data) for data in y_data) + y_step
    ax.set_ylim(0, y_max)

    ax.legend(bbox_to_anchor=(0.5, -0.08), loc='upper center', ncol=len(labels))
    ax.grid(axis='y', linestyle='--', alpha=0.7, linewidth=0.5)
    plt.tight_layout(rect=[0, 0.1, 1, 1])

    plt.savefig(output_path, dpi=350, bbox_inches='tight')
    plt.close()
    print(f"条形图已保存至: {output_path}")


def plot_multiple_grouped_bars(
    x_data: List[str],
    y_data_before: List[List[float]],
    y_data_after: List[List[float]],
    labels: Optional[List[str]] = None,
    title: Optional[str] = None,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    output_path: str = "bar_chart_subplots.png",
    fig_size: tuple = (16, 6),
    bar_width_factor: float = 0.5,
    group_padding: float = 0.16,
    y_step: int = 10
):
    fig, axs = plt.subplots(1, 2, figsize=fig_size)

    n_groups = len(x_data)
    n_datasets = len(y_data_before)

    if labels is None:
        labels = [f"Dataset {i + 1}" for i in range(n_datasets)]

    total_width = bar_width_factor - (n_datasets - 1) * group_padding / n_datasets
    bar_width = min(total_width / n_datasets, 0.2)
    indices = range(n_groups)

    # ✅ 计算全局最大值，用于统一 Y 轴范围
    all_data = y_data_before + y_data_after
    global_max = max(max(data) for data in all_data)
    y_step = 5  # 可根据数据特点调整，比如 5, 10, 20...
    y_max = ((global_max // y_step) + 2) * y_step  # 向上取整到最近的 y_step 的倍数，留点空隙
    y_min = 0

    # 存储第一个子图的条形，用于图例
    all_bars = []

    def plot_subplot(ax, y_data, subtitle):
        bars = []
        for i, (data, label) in enumerate(zip(y_data, labels)):
            offset = i * (bar_width + group_padding / n_datasets) - (total_width / 2)
            bar = ax.bar([0.055 + x + offset for x in indices], data, width=bar_width, label=label)
            bars.append(bar)

            for rect in bar:
                height = rect.get_height()
                ax.annotate(f'{height:.2f}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom')

        ax.set_title(subtitle, fontsize=14)
        if y_label:
            ax.set_ylabel(y_label)
        if x_label:
            ax.set_xlabel(x_label)
        ax.set_xticks(indices)
        ax.set_xticklabels(x_data)

        # 统一设置 Y 轴范围
        ax.set_ylim(y_min, y_max)

        # （可选）统一设置 Y 轴刻度
        import numpy as np
        ax.set_yticks(np.arange(0, y_max + 1, y_step))

        ax.grid(axis='y', linestyle='--', alpha=0.7, linewidth=0.5)

        # 仅记录第一个子图的 bars 用于图例
        if not all_bars:
            all_bars.extend(bars)

    plot_subplot(axs[0], y_data_before, "获奖前5年")
    plot_subplot(axs[1], y_data_after, "获奖后5年")

    if title:
        fig.suptitle(title, fontsize=16)

    # 共享图例，放在最下方
    fig.legend(
        handles=[bar[0] for bar in all_bars],  # 每个数据集取第一个 bar
        labels=labels,
        loc='lower center',
        ncol=len(labels),
        bbox_to_anchor=(0.5, 0.01)  # 调整位置，避免与 x 轴标签重叠
    )

    # 调整布局，为底部图例留出空间
    plt.tight_layout(rect=[0, 0.1, 1, 0.95])  # [left, bottom, right, top]

    plt.savefig(output_path, dpi=350, bbox_inches='tight')
    plt.close()
    print(f"分组条形图（子图）已保存至: {output_path}")


if __name__ == '__main__':
    plot_grouped_bar(["A", "B", "C"],
                     [[10, 20, 30], [15, 25, 35]],
                     labels=["获奖前5年", "获奖后5年"],
                     title="示例分组条形图")

    x_data = ["A1", "A2", "A3"]
    y_data_before = [[30, 5, 5], [30, 5, 5]]
    y_data_after = [[30, 5, 5], [30, 5, 5]]
    labels = ["何旭华", "刘钢"]
    plot_multiple_grouped_bars(
        x_data=x_data,
        y_data_before=y_data_before,
        y_data_after=y_data_after,
        labels=labels,
        title=None,
        y_label=None,
        output_path="shared_y_legend_bottom.png"
    )
