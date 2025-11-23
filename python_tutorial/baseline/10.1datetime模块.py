# /usr/bin/env python3
# -*- coding:utf-8 -*-
from datetime import datetime, timedelta, timezone
import re

def test_date():
    """
    日期操作
    :return:
    """
    now = datetime.now()

    # 2017-09-19 09:35:19.050186
    print(now)

    # <class 'datetime.datetime'>
    print(type(now))

    # 用指定日期时间创建datetime
    dt = datetime(2015, 4, 19, 12, 20)

    # 2015-04-19 12:20:00
    print(dt)

    # datetime转换为timestamp-小数位表示毫秒数
    print(dt.timestamp())

    t = 1429417200.0

    # timestamp转换为datetime-本地时间
    print(datetime.fromtimestamp(t))

    # timestamp直接转换到UTC标准时区的时间
    print(datetime.utcfromtimestamp(t))

    # str转换为datetime
    cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
    print(cday)

    # datetime转换为str
    print(cday.strftime('%a, %b %d %H:%M'))

    # datetime 加减法
    now = now - timedelta(hours=1)
    print(now)
    now = now + timedelta(days=2, hours=10)
    print(now)

    # 拿到UTC时间，并强制设置时区为UTC+0:00:
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    print(utc_dt)
    # astimezone()将转换时区为北京时间:
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    print(bj_dt)
    # astimezone()将转换时区为东京时间:
    tokyo_dt1 = utc_dt.astimezone(timezone(timedelta(hours=9)))
    print(tokyo_dt1)
    # astimezone()将bj_dt转换时区为东京时间:
    tokyo_dt = bj_dt.astimezone(timezone(timedelta(hours=9)))
    print(tokyo_dt)

tz_rex = r'^UTC(\-|\+)(\d{1,2}):(\d{2})$'
def to_timestamp(dt_str, tz_str):
    '''
    字符串转为 timestamp
    :param dt_str:
    :param tz_str:
    :return:
    '''
    str2date = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    tz_com = re.compile(tz_rex)
    tz_match = tz_com.match(tz_str)

    tz_symbol = tz_match.group(1)
    tz_hour = tz_match.group(2)
    tz_min = tz_match.group(3)
    tz = None
    if tz_symbol == '+':
        tz = timezone(timedelta(hours=int(tz_hour), minutes=int(tz_min)))
    elif tz_symbol == '-':
        tz = timezone(timedelta(hours=-int(tz_hour), minutes=int(tz_min)))
    return str2date.replace(tzinfo=tz).timestamp()

def exercise():
    '''
    假设你获取了用户输入的日期和时间如2015-1-21 9:01:30，以及一个时区信息如UTC+5:00，
    均是str，请编写一个函数将其转换为timestamp：
    :return:
    '''
    t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
    assert t1 == 1433121030.0, t1

    t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
    assert t2 == 1433121030.0, t2

if __name__ == '__main__':
    # test_date()
    exercise()











