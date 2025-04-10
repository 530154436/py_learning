#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2025/3/31 16:57
# @function:
import time
from threading import Lock


class TokenBucket(object):
    """
    令牌桶算法（单机版）
    """
    def __init__(self, capacity: int, fill_rate: int):
        """
        :param capacity:  The total tokens in the bucket.
        :param fill_rate:  The rate in tokens/second that the bucket will be refilled
        """
        self._capacity = int(capacity)
        self._tokens = int(capacity)
        self._fill_rate = int(fill_rate)
        self._last_time = time.time()
        self._lock = Lock()

    @property
    def capacity(self) -> int:
        """获取当前桶容量"""
        return self._capacity

    @property
    def tokens(self) -> int:
        """获取当前令牌数量"""
        return self._tokens

    @property
    def last_time(self) -> int:
        """获取最新时间"""
        return self._last_time

    def _refill(self) -> int:
        """补充令牌"""
        now = time.time()
        elapsed = int(now - self._last_time)
        if elapsed >= 1 and self._tokens < self._capacity:
            delta = int(self._fill_rate * elapsed)
            self._tokens = min(self._capacity, self._tokens + delta)
            self._last_time = now
        return self._tokens

    def consume(self, tokens: int = 1) -> bool:
        """
        获取令牌
        :param tokens: 需要的令牌数量
        :return: 是否获取成功
        """
        self._lock.acquire()   # 加锁
        try:
            self._refill()
            if tokens <= self._tokens:
                self._tokens -= tokens
                return True
            return False
        finally:
            self._lock.release()   # 确保锁释放


class IntervalRefillTokenBucket(TokenBucket):
    """
    令牌桶算法（固定间隔时间后补充令牌）
    """

    def __init__(self, capacity: int, fill_rate: int):
        """
        :param fill_rate: 令牌填充速度
        :param capacity: 令牌桶容量
        """
        super().__init__(capacity, fill_rate)
        self._tokens = fill_rate        # 初始化为填充速率
        self._refill_count = 1

    def _refill(self, interval: int = 60) -> int:
        """
        动态计算每分钟内允许的最大令牌数，即填充速率匀速增长/每分钟
        第1分钟内: init_tokens
        第2分钟内: init_tokens * 2
        第3分钟内: init_tokens * 3
        ...
        """
        elapsed_seconds = (time.time() - self._last_time)
        if elapsed_seconds >= interval:
            now = time.time()
            self._refill_count += 1
            self._tokens = min(self._fill_rate * self._refill_count, self._capacity)
            self._last_time = now
            print(f"令牌补充: 当前时间={now},最新时间={self._last_time},令牌数量={self._tokens}")
