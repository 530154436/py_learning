#!/usr/bin/env python3
# -*- coding:utf-8 -*--
from abc import ABC
from celery import Task


class CallbackTask(Task, ABC):
    def on_success(self, retval, task_id, args, kwargs):
        """
        retval – The return value of the task.
        task_id – Unique id of the executed task.
        args – Original arguments for the executed task.
        kwargs – Original keyword arguments for the executed task.
        """
        print(retval, task_id, args, kwargs)
        super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        exc – The exception raised by the task.
        task_id – Unique id of the failed task.
        args – Original arguments for the task that failed.
        kwargs – Original keyword arguments for the task that failed.
        """
        print(exc, task_id, args, kwargs, einfo)
        super().on_failure(exc, task_id, args, kwargs, einfo)
