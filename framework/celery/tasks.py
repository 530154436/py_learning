#!/usr/bin/env python3
# -*- coding:utf-8 -*--
import time


def add(x, y, double=2):
    return (x + y) * double


def update_state(self):
    """ 实时更新任务状态 """
    for i in range(100):
        self.update_state(state=f'{i}/100',
                          meta={'current': i + 1, 'total': 100,
                                'status': "分析中"})
        time.sleep(0.1)
        print(f"{i}/100")
    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': 42}
