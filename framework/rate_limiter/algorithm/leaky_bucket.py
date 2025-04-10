#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2025/4/9 15:56
# @function:
import time
from threading import Lock


class LeakyBucket(object):
    """
    漏桶算法
    """
    def __init__(self, capacity: int, leak_rate: int):
        """
        :param capacity:  桶的容量
        :param leak_rate: 漏桶出水速率
        """
        self._capacity = int(capacity)
        self._leak_rate = int(leak_rate)
        self._water = 0  # 当前桶中的水量
        self._last_time = time.time()  # 上次漏水时间戳
        self._lock = Lock()

    def _leak(self) -> int:
        """
        漏水
        """
        now = time.time()
        elapsed = int(now - self._last_time)
        if elapsed >= 1:
            self._water = max(0, self._water - int(self._leak_rate * elapsed))  # 水随着时间流逝，不断流走，最多就流干到0.
            self._last_time = now
        return self._water

    def consume(self, water: int = 1) -> bool:
        """
        获取水滴
        :param water: 需要的水滴数量
        :return: 是否获取成功
        """
        self._lock.acquire()   # 加锁
        try:
            self._leak()
            if self._water + water <= self._capacity:
                self._water += water
                return True
            return False
        finally:
            self._lock.release()   # 确保锁释放
