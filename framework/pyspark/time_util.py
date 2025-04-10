#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2021/9/7 14:37
# @function:    日期工具包
import pytz
from typing import Union
from datetime import datetime, timedelta


# 时区
TIME_ZONE = pytz.timezone('Asia/Shanghai')


class DateUtil(object):

    @classmethod
    def get_now_str(cls, _format='%Y-%m-%d %H:%M:%S') -> str:
        """
        获取当前日期
        """
        return datetime.now().strftime(_format)

    @classmethod
    def get_now_str_isoformat(cls) -> str:
        """
        获取当前日期(ISO格式): 2021-11-26T14:44:52.058+08:00
        """
        return datetime.now(tz=TIME_ZONE).isoformat(timespec='milliseconds')

    @classmethod
    def get_days_ago_str(cls, days, _format='%Y-%m-%d %H:%M:%S') -> str:
        """
        获取此刻 N天前 的日期
        """
        return (datetime.now() - timedelta(days=days)).strftime(_format)

    @classmethod
    def get_days_ago_str_isoformat(cls, days) -> str:
        """
        获取此刻 N天前 的日期
        """
        return (datetime.now(tz=TIME_ZONE) - timedelta(days=days)).isoformat(timespec='milliseconds')

    @classmethod
    def isoformat2format(cls, date_string: str, to_format='%Y-%m-%d %H:%M:%S') -> Union[str, None]:
        """
        获取此刻 N天前 的日期
        """
        if not isinstance(date_string, str):
            return None
        _obj = datetime.fromisoformat(date_string)
        return _obj.strftime(to_format)

    @classmethod
    def timestamp2format(cls, seconds: float, to_format='%Y-%m-%d %H:%M:%S.%f'):
        # 转换为datetime对象
        dt = datetime.fromtimestamp(seconds)
        # 格式化为字符串，包括毫秒
        formatted = dt.strftime(to_format)
        return formatted

    @classmethod
    def get_days_later_str(cls, days, _format='%Y-%m-%d %H:%M:%S'):
        """
        获取此刻 N天后 的日期
        """
        return (datetime.now() + timedelta(days=days)).strftime(_format)

    @classmethod
    def get_hours_before_str(cls, hours, _format='%Y-%m-%d %H:%M:%S'):
        """
        获取此刻 N天后 的日期
        """
        return (datetime.now() - timedelta(hours=hours)).strftime(_format)

    @classmethod
    def get_special_date_str(cls, special_date, days, _format='%Y-%m-%d'):
        """
        获取指定日期间隔 N天 的日期
        """
        return (datetime.strptime(special_date, _format) + timedelta(days=days)).strftime(_format)

    @classmethod
    def get_special_date_before_hours_str(cls, special_date, hours, _format='%Y-%m-%d'):
        """
        获取指定日期间隔 N天 的日期
        """
        return (datetime.strptime(special_date, _format) - timedelta(hours=hours)).strftime(_format)


if __name__ == '__main__':
    print(DateUtil.get_now_str())
    print(DateUtil.get_days_ago_str(30))
    print(DateUtil.get_days_later_str(30))

    print(DateUtil.get_now_str_isoformat())
    print(DateUtil.isoformat2format(DateUtil.get_now_str_isoformat()))
    print(DateUtil.get_special_date_before_hours_str("2022-09-19 00:00:00", 1, _format='%Y-%m-%d %H:%M:%S'))
    print(DateUtil.get_hours_before_str(1, _format='%Y-%m-%d %H:%M:%S'))

    print(datetime.strptime("2022-09-21", '%Y-%m-%d'))
    print(DateUtil.timestamp2format(1695297986.901691))
