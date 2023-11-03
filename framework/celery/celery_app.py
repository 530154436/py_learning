#!/usr/bin/env python3
# -*- coding:utf-8 -*--
# celery==5.2.0
# importlib_metadata==4.13.0
import json
from celery import Celery
from kombu.serialization import register
from framework.celery import celeryconfig
from framework.celery.task import add

CELERY_APP = Celery('tasks')
CELERY_APP.config_from_object(celeryconfig)

# 注册JSON序列化器
register('json', lambda v: json.dumps(v), lambda v: json.loads(v),
         content_type='application/json', content_encoding='utf-8')

# 加载异步任务
add_async = CELERY_APP.task(add, name=add.__name__)


if __name__ == "__main__":
    CELERY_APP.worker_main(argv=['worker', '--loglevel=DEBUG', '--pool=threads'])
