#!/usr/bin/env python3
# -*- coding:utf-8 -*--
import json
import logging
from celery import Celery
from kombu.serialization import register
from celery_framework import celeryconfig
from celery_framework.callbacks import CallbackTask
from celery_framework.task import add, update_state


# 字体有问题
logging.getLogger('matplotlib.font_manager').disabled = True

CELERY_APP = Celery('tasks')
CELERY_APP.config_from_object(celeryconfig)

# 注册JSON序列化器
register('json', lambda v: json.dumps(v), lambda v: json.loads(v),
         content_type='application/json', content_encoding='utf-8')

# 加载异步任务
add_async = CELERY_APP.task(add, name=add.__name__, base=CallbackTask)
update_state_async = CELERY_APP.task(update_state, name=update_state.__name__, base=CallbackTask, bind=True)
# report_controller_creat_async = CELERY_APP.task(ReportController.create,
#                                                 name=ReportController.create.__name__)


if __name__ == "__main__":
    CELERY_APP.worker_main(argv=['worker', '--loglevel=DEBUG', '--pool=threads'])
