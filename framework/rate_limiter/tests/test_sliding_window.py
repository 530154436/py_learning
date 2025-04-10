#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2025/4/1 16:03
# @function:
import random
import time
import unittest
import threading
from queue import Queue
from unittest.mock import patch
from framework.rate_limiter.sliding_window import SlidingWindow


class TestSlidingWindow(unittest.TestCase):

    @patch('time.time')
    def test_single_thread(self, mock_time):
        # 初始时间戳
        mock_time.return_value = 1000.0
        window_size = 6
        cycle_size = 3
        limiter = SlidingWindow(capacity=4, window_size=window_size, cycle_size=cycle_size)
        result_queue = Queue()  # 线程安全的FIFO队列

        def stress_test():
            while not limiter.consume(1):
                print(f"{threading.current_thread().name}: 限流[计算器为0]")
                time.sleep(1)
            result_queue.put(True)  # 原子操作，无需锁

            print(limiter._counter)
            print(f"{threading.current_thread().name}: 剩余请求数: {sum(limiter._counter.values())}/{limiter._capacity}")
            print()

        # 子窗口1=[999, 1002), 请求数=1
        stress_test()
        limiter.print_counter()

        # 子窗口1 = [999, 1002), 请求数 = 1
        # 子窗口2 = [1002, 1005), 请求数 = 2
        mock_time.return_value = 1003.0
        stress_test()
        stress_test()
        limiter.print_counter()

        # 子窗口1=[1002, 1005), 请求数=2
        # 子窗口2=[1005, 1008), 请求数=1
        mock_time.return_value = 1006.0  # 子窗口[999, 1002)过期被删除
        stress_test()
        stress_test()
        limiter.print_counter()

        results = []
        while not result_queue.empty():
            results.append(result_queue.get())
        self.assertEqual(sum(results), 5)


if __name__ == "__main__":
    unittest.main()
