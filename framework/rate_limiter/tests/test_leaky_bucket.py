#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2025/4/1 16:03
# @function:
import time
import unittest
import threading
from queue import Queue
from framework.rate_limiter.algorithm.leaky_bucket import LeakyBucket


class TestLeakyBucket(unittest.TestCase):

    def test_concurrent_access(self):
        num_worker = 10
        bucket = LeakyBucket(capacity=4, leak_rate=2)
        result_queue = Queue()  # 线程安全的FIFO队列

        def stress_test():
            while not bucket.consume(1):
                print(f"{threading.current_thread().name}: 限流[漏桶已满]")
                time.sleep(1)
            result_queue.put(True)  # 原子操作，无需锁
            print(f"{threading.current_thread().name}: 漏了1滴水, 漏桶已有水滴: {bucket._water}/{bucket._capacity}")

        threads = [threading.Thread(target=stress_test) for _ in range(num_worker)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 从队列提取结果
        results = []
        while not result_queue.empty():
            results.append(result_queue.get())
        self.assertEqual(sum(results), num_worker)


if __name__ == "__main__":
    unittest.main()
