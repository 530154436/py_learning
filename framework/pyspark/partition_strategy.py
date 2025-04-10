#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2025/2/25 16:37
# @function: 自定义分区策略
import random
from typing import Any
from pyspark import RDD


class DualSaltPartitioner(object):
    """
    双重盐值键分区策略
    1、二级混合哈希打破局部聚集
    2、副盐随机数动态调节热点分布
    """
    def __init__(self, num_partitions):
        self.num_partitions = num_partitions
        self.sub_salt = random.randint(0, num_partitions)

    def __call__(self, key: Any) -> int:
        # 二级哈希混合
        return (hash(key) + self.sub_salt) % self.num_partitions


def partition_by_dual_salt(rdd: RDD, num_partitions: int):
    """
    双重盐值键分区策略
    """
    rdd_partitioned = rdd\
        .map(lambda x: (hash(x) % num_partitions, x)) \
        .partitionBy(num_partitions, DualSaltPartitioner(num_partitions=num_partitions)) \
        .values()
    return rdd_partitioned


def partition_by_index(rdd: RDD, num_partitions: int) -> RDD:
    """
    基于全局索引的动态分区策略
    :param rdd: 输入RDD
    :param num_partitions: 目标分区数
    :return: 重分区后的RDD

    使用zipWithIndex为每个元素生成唯一索引，然后通过map将索引作为键，再利用partitionBy根据键的模数来分区。
    但需要注意，zipWithIndex生成的索引是全局的，但分区后的数据可能需要调整，因为重新分区会导致数据移动。
    步骤：
    1. 使用zipWithIndex为每个元素生成索引。
    2. 将索引作为键，元素作为值。
    3. 使用partitionBy并指定分区函数为索引模分区数。
    4. 去除键，保留原始数据。
    """
    # 生成全局唯一索引
    indexed_rdd = rdd\
        .zipWithIndex()\
        .map(lambda x: (x[1], x[0]))  # (data, index) => (index, data)

    # 执行重分区（保留分区键）
    rdd_partitioned = indexed_rdd\
        .partitionBy(numPartitions=num_partitions,
                     partitionFunc=lambda key: key % num_partitions)\
        .values()

    return rdd_partitioned
