#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/02/03
@function:
"""
from typing import Iterable, Dict

def gen_insert_sql(tb_name, docs:Iterable[Dict], upsert=True):
    '''
    生成插入 Mysql 语句，注意每个dic中的键数量必须保持一致
    :param tb_name:     表明
    :param docs:        插入的数据

    :Examples:
        INSERT INTO city_row(_id, url, 下辖地区, 中文名称, f_id)
        VALUES ("北京_东城区", "https://bj.zhaoshang.net/dongcheng/zhaoshang", "17个街道", "东城区", "110101"),
        ("北京_西城区", "https://bj.zhaoshang.net/xicheng/zhaoshang", "15个街道", "西城区", "110102"),
        ("北京_朝阳区", "https://bj.zhaoshang.net/chaoyang/zhaoshang", "24个街道、19个地区", "朝阳区", "110105")
        ON DUPLICATE KEY UPDATE
        _id=VALUES(_id), url=VALUES(url), 下辖地区=VALUES(下辖地区), 中文名称=VALUES(中文名称), f_id=VALUES(f_id);
    '''

    def gen_insert_pattern(cnt):
        return '('+', '.join('%s' for i in range(cnt))+')' # (%s, %s, %s)

    def gen_update_pattern(cnt):
        return tuple('%s=VALUES(%s)' for i in range(cnt))  # %%s=VALUES(%s), %s=VALUES(%s)

    if not docs:
        return
    columns = docs[0].keys()
    col_cnt = len(columns)

    # 构造插入语句
    i_pattern = gen_insert_pattern(col_cnt)
    sql = f'INSERT INTO {tb_name}'+i_pattern+'\nVALUES '
    sql = sql % tuple(columns) # INSERT INTO TABLE (1, 2, 3)
    values = []
    for cnt,doc in enumerate(docs):
        v_list = []
        for v in doc.values():
            if isinstance(v, str):
                v = '"%s"' % v
            else:
                v = str(v)
            v_list.append(v)
        values.append(i_pattern%tuple(v_list)) # (1, 2, "3")
    sql += ',\n'.join(values)

    # 构造更新语句(重复键)
    if upsert:
        sql += '\nON DUPLICATE KEY UPDATE\n'
        u_patter = gen_update_pattern(col_cnt)
        columns_dup = tuple((k,k) for k in columns)
        sql += ', '.join( u%c for u,c in zip(u_patter, columns_dup))

    return sql+';'

if __name__ == '__main__':
    docs = [{
                "_id": "北京_东城区",
                "url": "https://bj.zhaoshang.net/dongcheng/zhaoshang",
                "下辖地区": "17个街道",
                "中文名称": "东城区",
                "f_id": "110101"
            }
            ,
            {
                "_id": "北京_西城区",
                "url": "https://bj.zhaoshang.net/xicheng/zhaoshang",
                "下辖地区": "15个街道",
                "中文名称": "西城区",
                "f_id": "110102"
            }
            ,
            {
                "_id": "北京_朝阳区",
                "url": "https://bj.zhaoshang.net/chaoyang/zhaoshang",
                "下辖地区": "24个街道、19个地区",
                "中文名称": "朝阳区",
                "f_id": "110105"
            }]
    sql = gen_insert_sql('city_row', docs, upsert=True)
    print(sql)