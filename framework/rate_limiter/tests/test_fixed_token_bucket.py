#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2025/4/1 16:03
# @function:
import unittest
from queue import Queue
from threading import Thread
from unittest.mock import patch
from framework.rate_limiter.token_bucket import IntervalRefillTokenBucket


class TestFixedTokenBucket(unittest.TestCase):

    @patch('time.time')
    def test_single_thread_refill(self, mock_time):
        """测试单线程下的令牌补充逻辑"""
        # 初始时间戳
        mock_time.return_value = 1000.0
        bucket = IntervalRefillTokenBucket(capacity=1000, fill_rate=10)

        # 第0分钟（初始状态）
        print(f"第1分钟内: tokens数量={bucket._tokens}")
        self.assertTrue(bucket.consume(5))
        self.assertEqual(bucket._tokens, 5)  # 访问protected成员仅用于测试

        # 模拟时间流逝到第2分钟
        mock_time.return_value = 1060.0  # +60秒
        bucket._refill()
        print(f"第2分钟内: tokens数量={bucket._tokens}")
        self.assertTrue(bucket.consume(15))  # 10初始 + 10新增 = 20可用
        self.assertEqual(bucket._tokens, 5)

        self.assertTrue(bucket.consume(5))
        self.assertEqual(bucket._tokens, 0)
        self.assertTrue(not bucket.consume(1))

        # 模拟时间流逝到第3分钟
        mock_time.return_value = 1120.0  # +120秒
        bucket._refill()
        print(f"第3分钟内: tokens数量={bucket._tokens}")
        self.assertTrue(bucket.consume(30))  # 20可用 + 10新增 = 30可用
        self.assertEqual(bucket._tokens, 0)

    @patch('time.time')
    def test_multi_thread(self, mock_time):
        """验证多线程 token消费"""
        mock_time.return_value = 1000.0
        fill_rate = 10
        bucket = IntervalRefillTokenBucket(capacity=1000, fill_rate=fill_rate)
        result_queue = Queue()  # 线程安全的FIFO队列

        def stress_test():
            result_queue.put(bucket.consume(1))  # 原子操作，无需锁

        # 第1分钟内只能消费 10 个token
        threads = [Thread(target=stress_test) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # 从队列提取结果
        results = []
        while not result_queue.empty():
            results.append(result_queue.get())
        self.assertEqual(sum(results), fill_rate)

        # 第2分钟内只能消费 20 个token
        mock_time.return_value = 1080.0
        threads = [Thread(target=stress_test) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # 从队列提取结果
        results = []
        while not result_queue.empty():
            results.append(result_queue.get())
        self.assertEqual(sum(results), fill_rate * 2)


if __name__ == '__main__':
    unittest.main()
