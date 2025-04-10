#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pyspark import SparkConf
from pyspark.sql import SparkSession
from kerberos_authorization import kerberos_authorization


class CreateSparkSession(object):
    def __init__(self, task_name, **config):
        kerberos_authorization()

        # 初始化创建sparksession需要的配置以及对应的任务编号
        spark_conf = SparkConf().setAppName(task_name)
        if not config:
            config = {
                'spark.hadoop.hive.exec.dynamic.partition': 'true',
                'spark.hadoop.hive.exec.dynamic.partition.mode': 'nonstrict',
                'spark.hadoop.hive.exec.max.dynamic.partitions': '20000',
                'spark.sql.sources.partitionOverwriteMode': 'dynamic',
            }
        for k, v in config.items():
            spark_conf.set(k, v)
        self._spark = SparkSession.builder.config(conf=spark_conf).enableHiveSupport().getOrCreate()

    def get_spark_session(self) -> SparkSession:
        return self._spark
