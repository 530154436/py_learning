#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2025/4/9 16:45
# @function:
import time
from collections import OrderedDict
from threading import Lock


class SlidingWindow(object):
    """
    滑动窗口时间算法
    """

    def __init__(self, capacity: int, window_size: int = 30, cycle_size: int = 3):
        """
        :param capacity:  请求数阈值
        :param window_size: 时间窗口30秒
        :param cycle_size:  小周期时间（将时间窗口划分为N个小周期） eg.时间窗口30秒，3秒一个周期，一共10个周期
        """
        self._capacity = capacity
        self._window_size = window_size
        self._cycle_count = int(window_size / cycle_size)
        self._cycle_size = cycle_size  # 3秒一个周期

        self._counter = OrderedDict()
        self._req_count = 0
        self._lock = Lock()

    def print_counter(self):
        """
        打印窗口内的所有周期和请求数
        """
        for i, (k, v) in enumerate(self._counter.items(), start=1):
            print(f"周期{i}=[{k}, {k + self._cycle_size}), 请求数={v}")

    def _count_req_in_window(self, cur_cycle_start_time: int):
        """
        统计当前窗口的请求数（遍历所有小周期）
        """
        # 计算窗口开始时间
        cur_window_start_time = cur_cycle_start_time - self._cycle_size * (self._cycle_count - 1)
        count = 0
        for key, value in list(self._counter.items()):
            # 删除无效过期的子窗口计数器
            if key < cur_window_start_time:
                self._counter.pop(key)
            else:
                count += value
        return count

    def consume(self, req: int = 1) -> bool:
        """
        :return 是否请求成功
        """
        self._lock.acquire()   # 加锁
        try:
            # 计算当前小周期开始时间：当前(1744200124), 开始时间=1744200123=int(1744200124/3)*3，即第10个周期是 [1744200123, 1744200126]
            cur_cycle_start_time = int(time.time() / self._cycle_size) * self._cycle_size
            req_count = self._count_req_in_window(cur_cycle_start_time)

            if req_count + req <= self._capacity:
                # 更新计数器
                self._counter[cur_cycle_start_time] = self._counter.get(cur_cycle_start_time, 0) + req
                return True
            return False
        finally:
            self._lock.release()   # 确保锁释放
