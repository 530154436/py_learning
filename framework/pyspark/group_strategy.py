#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2024/12/31 11:10
# @function:
import math
import traceback
from typing import List
from pyspark.sql import SparkSession, DataFrame
from run_batch_param import SparkRunBachParam


class DataGroupDefaultStrategy(object):

    def __init__(self, spark_session: SparkSession, param: SparkRunBachParam):
        self.param = param
        self.spark_session = spark_session

        assert self.param.primary_col is not None \
               and self.param.group_tbl_name is not None \
               and self.param.nums_per_group is not None

    def get_group_ids(self, reverse: bool = False) -> List[int]:
        """
        获取分组表的所有分区
        """
        group_ids = []
        try:
            sql_1 = f"""SHOW PARTITIONS {self.param.group_tbl_name}"""
            partitions = list(self.spark_session.sql(sql_1).toPandas().get("partition").values)
            group_ids = list(map(lambda x: int(x.split("=")[1]), partitions))
            group_ids.sort(key=lambda x: x, reverse=reverse)
        except Exception as e:
            print(f"分组表不存在: {self.param.group_tbl_name}")
            print(traceback.format_exc(limit=5))
        return group_ids

    def get_dataframe_by_key(self, group_id: int) -> DataFrame:
        sql_1 = f"""SELECT {self.param.primary_col} FROM {self.param.group_tbl_name} WHERE group_id = {group_id}"""
        return self.spark_session.sql(sql_1)

    def group_by_key(self) -> int:
        """
        对待处理的数据进行分组，并创建临时表
        :return 分组数量
        """
        # 1、统计本次任务待处理的数据数量
        sql_1 = f"""
        SELECT count(distinct {self.param.primary_col}) FROM {self.param.from_tbl_name}
        """
        nums = self.spark_session.sql(sql_1).toPandas().iloc[0, 0]
        groups = int(math.ceil(nums / self.param.nums_per_group))

        # 2、清除已生成的数据
        self.spark_session.sql(f"DROP TABLE IF EXISTS {self.param.group_tbl_name}")

        create_sql = f"""
        CREATE EXTERNAL TABLE if not exists {self.param.group_tbl_name} (
            {self.param.primary_col} string
        ) PARTITIONED BY (group_id bigint)
        STORED AS ORC
        LOCATION 'hdfs://nameservice1/warehouse/tablespace/external/hive/{self.param.db_name}.db/{self.param.group_tbl_name}'
        TBLPROPERTIES('external.table.purge'='TRUE', 'transactional'='false')
        """
        self.spark_session.sql(create_sql)

        # 3、对数据进行分组
        sql_2 = f"""
        INSERT INTO TABLE {self.param.group_tbl_name}
        SELECT t.{self.param.primary_col}, t.rn % {groups} as group_id
        FROM (
            SELECT {self.param.primary_col}, row_number() over(order by {self.param.primary_col}) as rn
            FROM {self.param.from_tbl_name}
        ) t
        """
        self.spark_session.sql(sql_2)
        print(f"本次分组：分组表={self.param.group_tbl_name}, 数据量={nums}, 共分组数={groups}")
        return groups

    def delete_by_key(self, group_id: int) -> bool:
        """
        删除某个分区
        """
        try:
            sql = f"ALTER TABLE {self.param.group_tbl_name} DROP IF EXISTS PARTITION (group_id='{group_id}')"
            self.spark_session.sql(sql)
            return True
        except Exception as e:
            print(traceback.format_exc(limit=5))
            return False


if __name__ == "__main__":
    from pyspark.sql import SparkSession
    from kerberos_authorization import kerberos_authorization
    from create_spark_session import CreateSparkSession

    kerberos_authorization()
    conf = {
        'hive.exec.dynamic.partition.mode': 'nonstrict',
        # 'hive.exec.dynamic.partition.mode': '5g',
        # 'spark.executor.memory': '5g',
        # 'spark.executor.cores': '4'
    }
    _spark_session = CreateSparkSession("TestDataGroupDefaultStrategy", **conf) \
        .get_spark_session()
    _param = SparkRunBachParam(db_name="algo_recommend_dev",
                               from_tlb_name="tmp_t_ods_patent_us_1000",
                               primary_col="out_num",
                               nums_per_group=100)
    _spark_session.sql(f"use {_param.db_name}")
    _group_strategy = DataGroupDefaultStrategy(_spark_session, _param)
    _group_strategy.group_by_key()

    print(_group_strategy.get_group_ids())
    # print(_group_strategy.delete_by_key(2))
    print(_group_strategy.get_group_ids())

    # _group = _group_strategy.get_dataframe_by_key(3)
    # _group.show()
