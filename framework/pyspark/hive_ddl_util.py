#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2025/1/17 16:20
# @function:
from typing import Optional

from pyspark.sql.types import StructType, StructField, StringType, IntegerType


def generate_create_tbl_sql(schema: StructType,
                            table_name: str,
                            table_comment: str = "",
                            partition_by: Optional[StructField] = None,
                            storage_format: str = "ORC",
                            tbl_properties: dict = None) -> str:
    """
    根据schema元数据创建hive表
    """
    if tbl_properties is None:
        tbl_properties = {'external.table.purge': 'TRUE', 'transactional': 'false'}

    partition_by_str = ""
    if partition_by:
        partition_type = "INT" if isinstance(partition_by.dataType, IntegerType) else "STRING"
        partition_by_str = f"PARTITIONED BY ({partition_by.name} {partition_type})"

    field_lines = []
    for i, field in enumerate(schema.fields):
        field_name = field.name
        if partition_by is not None and field_name == partition_by.name:
            continue
        field_type = "INT" if isinstance(field.dataType, IntegerType) else "STRING"
        comment = field.metadata.get("COMMENT", "")
        field_lines.append(
            min(i, 1) * "        "
            + f"`{field_name}`".ljust(15)
            + f"{field_type.ljust(10)} COMMENT \"{comment}\""
        )

    fields_str = ",\n".join(field_lines)
    properties_str = ", ".join([f"'{k}' = '{v}'" for k, v in tbl_properties.items()])

    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {fields_str}
    )
    COMMENT '{table_comment}'
    {partition_by_str}
    STORED AS {storage_format}
    TBLPROPERTIES ({properties_str})
    """
    return create_table_sql


if __name__ == '__main__':
    _schema = StructType([
        StructField("custom_id", StringType(), False, metadata={"COMMENT": "自定义id, 唯一标识"}),
        StructField("prompt", StringType(), metadata={"COMMENT": "提示词"}),
        StructField("llm_result", StringType(), metadata={"COMMENT": "大模型原始结果"}),
        StructField("content", StringType(), metadata={"COMMENT": "大模型解析结果"}),
        StructField("usage", StringType(), metadata={"COMMENT": "调用大模型Token花费情况"}),
        StructField("finish_reason", StringType(), metadata={"COMMENT": "调用大模型结束原因"}),
        StructField("code", IntegerType(), metadata={"COMMENT": "自定义代码, 0/ok、其他/异常"}),
        StructField("message", StringType(), metadata={"COMMENT": "异常信息"}),
    ])
    print(generate_create_tbl_sql(_schema,
                                  "tmp_table_name",
                                  table_comment="LLM结果记录表",
                                  partition_by=StructField("dt", StringType())))

