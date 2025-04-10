#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2025/2/27 9:58
# @function:
import random


def get_exponential_backoff_interval(
    retries,
    minimum: int = 0,
    maximum: int = 10,
    full_jitter: bool = True
):
    """
    指数退避算法实现网络请求重试（Exponential backoff）
    https://developer.aliyun.com/article/748634
    https://www.oryoy.com/news/python-zhong-shi-xian-zhi-shu-tui-bi-suan-fa-you-hua-wang-luo-qing-qiu-zhong-shi-ce-lve.html
    https://github.com/celery/celery/blob/v4.3.0/celery/utils/time.py?spm=a2c6h.12873639.article-detail.6.71c8f895o5ZLmw#L392

    背景：
    大批量调用API，从而导致限流的报错。在遇到这种报错时，传统的重试策略是每隔一段时间重试一次。
    但由于是固定的时间重试一次，重试时又会有大量的请求在同一时刻涌入，会不断地造成限流。

    指数退避
    根据wiki上对Exponential backoff的说明，指数退避是一种通过反馈，成倍地降低某个过程的速率，以逐渐找到合适速率的算法。
    在以太网中，该算法通常用于冲突后的调度重传。根据时隙和重传尝试次数来决定延迟重传。
    在 c 次碰撞后（比如请求失败），会选择 0 和 $2^c$ 之间的随机值作为时隙的数量。
    对于第 1 次碰撞来说，每个发送者将会等待 0 或 1 个时隙进行发送。
    而在第 2 次碰撞后，发送者将会等待 0 到 3（ 由计算得到）个时隙进行发送。
    而在第 3 次碰撞后，发送者将会等待 0 到 7（ 由计算得到）个时隙进行发送。
    以此类推……
    随着重传次数的增加，延迟的程度也会指数增长。

    指数退避的期望值
    考虑到退避时间的均匀分布，退避时间的数学期望是所有可能性的平均值。
    也就是说，在 c 冲突次数为 `c` 时，可选时隙集合为 `[0, 1, ..., N]`，其中，
    $$
    N = \min(2^c-1, \text{maximum})
    $$
    **数学期望计算**：
    $$
    E = \frac{\sum_{k=0}^{N}k}{N+1} = \frac{N}{2} \quad \text{（时隙单位）}
    $$
    **推导步骤**：
    1. 等差数列求和：总和为 $\frac{(0+N)(N+1)}{2}$
    2. 平均分配：均匀分布下期望值为总和除以样本数 $(N+1)$
    3. 简化结果：$\frac{N(N+1)/2}{N+1} = \frac{N}{2}$

    | **冲突次数 (c)** | **时隙上限 (N)** | **数学期望 (E)** | **物理时间（以太网）** | **网络影响** |
    |-------------------|-------------------|-------------------|-------------------------|---------------|
    | 1                 | 1                 | 0.5 时隙         | 25.6μs                 | 快速重试      |
    | 3                 | 7                 | 3.5 时隙         | 179.2μs                | 冲突累积      |
    | 10                | 1023              | 511.5 时隙       | 26.2ms                 | 接近拥塞      |
    | 15（上限）        | 1023              | 511.5 时隙       | 26.2ms                 | 超时风险      |
。
    :param retries 对应于上文的 c（也就是碰撞次数）。
    :param max_retries 最大重试次数
    :param full_jitter 为了避免多个客户端同时重试，可以在等待时间中加入随机抖动。
    :param minimum: 最小等待时间（秒）。
    :param maximum: 最大等待时间（秒），以避免无限长的等待时间。
    """
    countdown = 2 ** retries
    # Full jitter according to
    # https://www.awsarchitectureblog.com/2015/03/backoff.html
    if full_jitter:
        countdown = random.randrange(countdown)  # 左闭右开 => [0, 2^c-1)
    # Adjust according to maximum wait time and account for negative values.
    return max(minimum, min(maximum, countdown))


if __name__ == "__main__":
    for i in range(50):
        print(i, get_exponential_backoff_interval(i, minimum=0.5, maximum=3))
