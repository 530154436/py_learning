#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2025/4/9 16:45
# @function:
import time
from threading import Lock


class FixedWindow(object):

    def __init__(self, capacity: int, window_size: int = 1):
        """
        :param capacity:  请求数阈值
        :param window_size: 固定的时间窗口（例如每秒、每分钟等），在此期间内的所有请求都会被计数，这里单位是秒
        """
        self._capacity = capacity
        self._window_size = window_size
        self._req_count = 0
        self._last_time = time.time()
        self._lock = Lock()

    def _reset(self):
        """
        重置计数器
        """
        now = time.time()
        elapsed = int(now - self._last_time)  # 秒
        if elapsed >= self._window_size:
            self._req_count = 0
            self._last_time = now

    def consume(self, req: int = 1) -> bool:
        """
        :return 是否请求成功
        """
        self._lock.acquire()   # 加锁
        try:
            self._reset()
            if self._req_count + req <= self._capacity:
                self._req_count += req
                return True
            return False
        finally:
            self._lock.release()   # 确保锁释放
