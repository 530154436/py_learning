# -*- coding: utf-8 -*-
# @Author: Michael Lean
# @E-mail: 1013851072@qq.com
# @Create Time: UTC +8:00 2023/6/7 16:25:07
import sys
import time
import traceback
from typing import List

from pyspark import StorageLevel, RDD
import pyspark.sql.functions as F
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StringType, StructField
from create_spark_session import CreateSparkSession
from run_batch_param import SparkRunBachParam
from alarms import DingDingAlarm
from group_strategy import DataGroupDefaultStrategy
import hive_ddl_util
from time_util import DateUtil


class SparkTaskTemplate:
    def __init__(self, param: SparkRunBachParam, task_name: str, phone: str = None):
        self.param = param
        self.task_name = task_name
        self.phone = phone

    def deal_partition_with_index(self, index, iterator, group_id):
        """
        对每个partition进行处理
        """
        raise NotImplementedError("not implemented")

    def fetch_data(self, spark_session: SparkSession, group_id: int = 0) -> RDD:
        # 取分组数据
        sql = self.generate_fetch_data_sql(group_id)
        print(f"第{group_id}分组获取数据集合SQL: {sql}")
        # 执行SQL并进行重分区
        rdd = spark_session \
            .sql(sql) \
            .repartition(self.param.num_partitions, self.param.primary_col) \
            .rdd \
            .persist(StorageLevel.MEMORY_AND_DISK)

        # 触发计算，确保数据准备好
        print(f"第{group_id}分组分区信息：分区数量={rdd.getNumPartitions()} 总数量={rdd.count()}")

        # 计算每个分区的元素数量
        partition_counts = rdd \
            .mapPartitionsWithIndex(self.count_partition) \
            .collect()
        for partition_count in partition_counts:
            print("        Partition {} Count: {}"
                  .format(partition_count[0], partition_count[1]))
        return rdd

    def pipeline(self, rdd: RDD, group_id: int = 0) -> List[dict]:
        """
        主要业务逻辑
        """
        # 业务逻辑
        df: DataFrame = rdd \
            .mapPartitionsWithIndex(lambda index, iterator: self.deal_partition_with_index(index, iterator, group_id)) \
            .toDF(schema=self.param.log_tlb_cols) \
            .persist(StorageLevel.MEMORY_AND_DISK)
        # df.show()
        # df.printSchema

        # 统计每个状态码的数量：触发 mapPartitionsWithIndex 的计算，并将结果缓存。
        df_agg: DataFrame = df \
            .withColumn("code", F.when(F.col("code") != 0, 1).otherwise(0)) \
            .groupBy("code") \
            .agg(F.count("*").alias("count")) \
            .orderBy(F.asc("code")) \
            .collect()

        # 存到结果表(记录表)：coalesce(10) 将分区数减少到 10 个，减少写入时的小文件问题。
        num_partitions = min(max(int(df.count() / 1e5), 10), 100)  # 动态调整写入分区数
        df.coalesce(num_partitions)\
            .write \
            .format("hive") \
            .mode("append") \
            .insertInto(self.param.log_tbl_name, overwrite=False)

        # 释放 df 的缓存
        if rdd.is_cached:
            rdd.unpersist()
        if df.is_cached:
            df.unpersist()
        return df_agg

    @staticmethod
    def count_partition(split_index, iterator) -> tuple:
        """
        计算每个分区的数量
        """
        count = len(list(iterator))
        yield split_index, count

    def generate_fetch_data_sql(self, group_id: int) -> str:
        """
        根据分组id,从源表中加载待处理的数据集合
        """
        sql = f"""
        select {self.param.primary_col}, {','.join(self.param.other_cols)}
        from {self.param.from_tbl_name} 
        where {self.param.primary_col} in (
            select {self.param.primary_col} 
            from {self.param.group_tbl_name}
            where group_id={group_id}
        )
        """
        return sql

    def init_dst_tbl(self, spark_session: SparkSession):
        # TODO: llm结果表可能会很大，可能要定时清理?
        partition_field = StructField("dt", StringType(), metadata={"COMMENT": "保存日期"})
        sql = hive_ddl_util.generate_create_tbl_sql(self.param.log_tlb_cols,
                                                    table_name=self.param.log_tbl_name,
                                                    table_comment="LLM结果记录表",
                                                    partition_by=partition_field)
        print(f"初始化LOG记录表:\n{sql}")
        spark_session.sql(sql)

    def run(self, spark_session: SparkSession = None):
        """
        运行spark任务：
        将数据分组，然后每个分组进行分区，每个分区利用deal_partition函数进行处理
        """
        # 一、初始化
        if spark_session is None:
            spark_session = CreateSparkSession(self.task_name).get_spark_session()
        group_strategy = DataGroupDefaultStrategy(spark_session=spark_session, param=self.param)
        ding_alarm = DingDingAlarm()
        spark_session.sql(f"use {self.param.db_name}")

        # LLM结果记录表
        self.init_dst_tbl(spark_session=spark_session)

        # 二、跑数流程
        # 1、判断分组是否存在
        # 若不存在则重新拉取源数据表，并创建临时分组表
        # 若存在则在原有分组基础上继续开始任务
        group_ids = group_strategy.get_group_ids(reverse=False)
        if len(group_ids) == 0:
            print(f"分组数据为空,获取新数据并分组: {self.param.from_tbl_name} => {self.param.group_tbl_name}.")
            group_strategy.group_by_key()
            # spark_session.sql(f"DROP TABLE if exists {self.parma.from_tbl_name}")
            group_ids = group_strategy.get_group_ids(reverse=False)
        if len(group_ids) == 0:
            msg = "分组数据为空, 退出跑批任务."
            print(msg)
            if self.phone:
                ding_alarm.post_msg(msg, self.phone)
            spark_session.stop()
            sys.exit(0)
        else:
            msg = f"任务【{self.task_name}】开始\n当前分组信息: "\
                  f"共{len(group_ids)}组，范围=[{min(group_ids)},{max(group_ids)}]，数量/组={self.param.nums_per_group}"
            print(msg)
            if self.phone:
                ding_alarm.post_msg(msg, self.phone)

        # 2、遍历每个分组进行跑批
        total = 0
        success = 0
        start_time_in_all = time.time()
        for group_id in group_ids:
            start_time = time.time()
            for try_count in range(1, self.param.max_retry + 1):
                try:
                    # 读取数据
                    rdd = self.fetch_data(spark_session, group_id=group_id)

                    # 业务逻辑+写表 => 最终返回统计信息
                    df_agg: List[dict] = self.pipeline(rdd, group_id=group_id)

                    # 删除该分组
                    group_strategy.delete_by_key(group_id)

                    # 推送信息
                    msg = f"{DateUtil.get_now_str()}: 第{group_id}组完成, 耗时{time.time() - start_time} 秒, "
                    if df_agg is not None:
                        for row in df_agg:
                            code = row['code']
                            count = row['count']
                            total += count
                            if code == 0:
                                msg += f"成功数量={count}, "
                                success += count
                            else:
                                msg += f"失败数量={count}. "
                    print(msg)
                    if self.phone:
                        ding_alarm.post_msg(msg, self.phone)
                    break
                except Exception as e:
                    msg = f"第{try_count}次报错，报错原因：{e}\n"\
                          f"{traceback.format_exc(limit=5)}"
                    print(msg)
                # 达到最大重试次数仍然报错，则抛出异常
                if try_count == self.param.max_retry:
                    raise RuntimeError("达到最大重试次数，请排查代码bug！")

        msg = f"spark任务完成！\n总共耗时：{time.time() - start_time_in_all} 秒, 成功: {success}, 失败: {total-success}."
        print(msg)
        if self.phone:
            ding_alarm.post_msg(msg, self.phone)
