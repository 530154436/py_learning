#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2024/12/30 17:50
# @function:
import argparse
from typing import List, Union
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


class SparkRunBachParam(object):

    def __init__(self, **kwargs):
        """
        :param db_name: 存数的db
        :param from_tbl_name: 取数表,待处理的数据集合
          -group_tbl_name: 数据分组表-${from_tbl_name}_group,作用类似缓存队列,每完成一组任务后删除对应分组
          -log_tbl_name: 保存结果表-${from_tbl_name}_log,作为为记录表,记录每次任务的所有信息(结果、异常信息等)
        :param dst_tlb_cols: log结果表列名
        :param dt: 当天日期

        涉及3张表：
        源数据表: ${source_tbl_name}，数据来源
        分组表: ${group_tbl_name}，对 ${from_tbl_name} 按ID进行分组，确保每次处理的数据量不会过大。
        日志表: ${log_tbl_name}，记录调用接口过程中的所有信息，包括业务代码、错误栈信息、原始返回结果等信息。
        """
        # 表信息
        self.db_name: str = kwargs.get('db_name')
        self.from_tbl_name: str = kwargs.get('from_tbl_name')
        assert self.from_tbl_name is not None

        self.primary_col: str = kwargs.get('primary_col')  # id
        self.other_cols: List[str] = list(kwargs.get('other_cols', "").split(","))
        self.dt: str = kwargs.get('dt')
        assert len(self.other_cols) > 0

        # 分组信息_
        self.group_tbl_name: str = self.from_tbl_name + "_group"
        self.nums_per_group: int = kwargs.get('nums_per_group', 10000)

        # 并行度
        # 并发数 = min(num_partitions, num-executors * executor-cores) * num_thread，防止master的io达到瓶颈
        # 先分组=>分区=>多线程请求
        self.num_partitions = int(kwargs.get('num_partitions', 10))
        self.num_thread = int(kwargs.get('num_thread', 10))  # 10

        # 重试次数
        self.max_retry: int = kwargs.get('max_retry', 3)

        # 其他参数
        self.others: dict = self._parse_kwargs(kwargs.get('others', ""), parse_int=True)

        # log结果记录表
        self.log_tbl_name: str = self.from_tbl_name + "_log"
        if kwargs.get('log_tbl_name') is not None:
            self.log_tbl_name = kwargs.get('log_tbl_name')
        self.log_tlb_cols: Union[List[str], StructType] = StructType([
            StructField("custom_id", StringType(), False, metadata={"COMMENT": "自定义id, 唯一标识"}),
            StructField("payload", StringType(), metadata={"COMMENT": "传入参数: json格式，如提示词等"}),
            StructField("result_raw", StringType(), metadata={"COMMENT": "调用接口原始结果"}),
            StructField("result", StringType(), metadata={"COMMENT": "解析后的结果"}),
            StructField("code", IntegerType(), metadata={"COMMENT": "自定义代码, 0/ok、其他/异常"}),
            StructField("message", StringType(), metadata={"COMMENT": "异常信息"}),
            StructField("option1", StringType(), metadata={"COMMENT": "扩展字段1:如调用大模型Token花费情况"}),
            StructField("option2", StringType(), metadata={"COMMENT": "扩展字段2:如调用大模型结束原因finish_reason"}),
            StructField("dt", StringType(), metadata={"COMMENT": "任务时间也是分区字段，格式为 yyyyMMddHHmm。"}),
        ])

    @staticmethod
    def _parse_kwargs(string: str, parse_int: bool = True, parse_bool: bool = True) -> dict:
        others = dict()
        for k_v in string.split(','):
            k_v = k_v.strip()
            if not k_v:
                continue
            k = k_v.split("=")[0]
            v = k_v.split("=")[1]
            if parse_int:
                try:
                    v = int(v)  # 如果可以转为整型则转为整型
                except ValueError:
                    pass
            if parse_bool and str(v).lower() in {"true", "false"}:
                v = str(v).lower() == "true"
            others[k] = v
        return others

    @staticmethod
    def get_args_parser() -> argparse.ArgumentParser:
        """
        构造命令行参数
        """
        parser = argparse.ArgumentParser(description="Spark Run Batch Parameters")

        # 基本参数
        parser.add_argument('--db_name', type=str, required=True, help='存储的数据库名称')
        parser.add_argument('--from_tbl_name', type=str, required=False, help='取数表')
        parser.add_argument('--primary_col', type=str, required=True, help='主键(也是分组的键)')
        parser.add_argument('--other_cols', type=str, required=True, help='其他列名，按逗号分隔')
        parser.add_argument('--dt', type=str, required=True, help='当天日期，也可以作为任务ID，格式为 yyyyMMddHH')

        # 分组信息
        parser.add_argument('--nums_per_group', type=int, default=10000, help='每组的数据条数，默认为10000')

        # 并行度
        parser.add_argument('--num_partitions', type=int, default=10, help='分区数，默认为10')
        parser.add_argument('--num_thread', type=int, default=10, help='每个分区的线程数，默认为10')

        # 重试次数
        parser.add_argument('--max_retry', type=int, default=3, help='重试次数')

        # 其他参数
        parser.add_argument('--others', type=str, default="", help='其他参数')
        return parser

    @classmethod
    def parse_args(cls) -> "SparkRunBachParam":
        parser = cls.get_args_parser()
        # 将解析后的参数转换为字典
        args = parser.parse_args()
        params_dict = {
            'db_name': args.db_name,
            'from_tbl_name': args.from_tbl_name,
            'primary_col': args.primary_col,
            'other_cols': args.other_cols,
            'dt': args.dt,
            'nums_per_group': args.nums_per_group,
            'num_partitions': args.num_partitions,
            'num_thread': args.num_thread,
            'max_retry': args.max_retry,
            'others': args.others,
        }
        return cls(**params_dict)

    def print_args(self):
        """
        打印所有参数，格式化输出。
        """
        print("Parameters:")
        print("=" * 80)
        for key, value in self.__dict__.items():
            if isinstance(value, (str, int, float)):
                print(f"{key}: {value}")
            elif isinstance(value, StructType):
                print(f"{key}: {','.join(value.fieldNames())}")
            elif isinstance(value, (list, set, tuple)):
                print(f"{key}: {','.join(value)}")
            elif isinstance(value, dict):
                print(f"{key}: ")
                for k, v in value.items():
                    print(f"  {k}: {v}")
            else:
                print(f"{key}: {str(value)}")
        print("=" * 80)
