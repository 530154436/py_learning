# !/usr/bin/env python3
# -*- coding:utf-8 -*-
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED
import time

def task(name, seconds:int):
    print(f"{name} is doing task.")
    time.sleep(seconds)
    print(f"{name} has done task.")
    return name,seconds


def test01():
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        # future.result()将阻塞调用方所在的线程，直到有结果可返回
        r1 = executor.submit(task, "task01", 5).result()
        r2 = executor.submit(task, "task02", 5).result()
        r3 = executor.submit(task, "task03", 5).result()

    print(f"costTime={time.time()-start}s sum={sum([r1,r2,r3])}")
    return sum([r1,r2,r3])

def test02():
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        tasks = []
        tasks.append(executor.submit(task, "task01", 10))
        tasks.append(executor.submit(task, "task02", 1))
        tasks.append(executor.submit(task, "task03", 1))
        tasks.append(executor.submit(task, "task04", 11))
        tasks.append(executor.submit(task, "task05", 1))
        tasks.append(executor.submit(task, "task06", 1))
        tasks.append(executor.submit(task, "task07", 10))
        tasks.append(executor.submit(task, "task08", 1))

        # 阻塞线程，直到所有任务完成
        wait(tasks, timeout=10, return_when=ALL_COMPLETED)

        print("封装结果")
        for t in tasks:
            name, seconds = t.result()
            print(name, seconds)

        print(f"costTime={time.time()-start}s ")

if __name__ == '__main__':
    # test01()
    test02()