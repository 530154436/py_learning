#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import psutil

def demo():
    cpu_count = psutil.cpu_count()
    cpu_nological_count = psutil.cpu_count(logical=False)
    print(cpu_count)
    print(cpu_nological_count)
    # 2说明是双核超线程, 4则是4核非超线程

    # 统计CPU的用户／系统／空闲时间：
    cpu_times = psutil.cpu_times()
    print(cpu_times)

    # top命令的CPU使用率，每秒刷新一次，累计10次
    for x in range(10):
        print(psutil.cpu_percent(interval=0.1, percpu=True))

    # 使用psutil获取物理内存和交换内存信息
    print(psutil.virtual_memory())
    print(psutil.swap_memory())

    # 获取磁盘分区、磁盘使用率和磁盘IO信息
    print(psutil.disk_partitions())
    print(psutil.disk_usage('/'))
    print(psutil.disk_io_counters())

    # 获取网络接口和网络连接信息
    # print(psutil.net_connections())
    # print(psutil.net_if_addrs())
    # print(psutil.net_if_stats())

    print()
    # 获取到所有进程的详细信息
    pids = psutil.pids()
    print(pids)
    p = psutil.Process(pids[0])
    print(p.name())
    print(p.exe()) # 进程exe路径
    print(p.cwd()) # 进程工作目录
    print(p.cmdline())  # 进程启动的命令行
    print(p.status())
    print(p.username())
    print(p.memory_info())  # 进程使用的内存
    print(p.open_files())   # 进程打开的文件
    print(p.connections())  # 进程相关网络连接
    print(p.num_threads())  # 进程的线程数量
    print(p.threads())      # 所有线程信息
    print(p.environ())      # 进程环境变量

if __name__ == '__main__':
    # demoGet()
    demo()