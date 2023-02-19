# !/usr/bin/env python3
# -*- coding : utf-8 -*-
from fabric.api import *

# python3.5 -m pip install --upgrade pip
# sudo python3.5 -m pip install fabric3

# env.hosts = ['139.199.5.56']
# env.user = 'ubuntu'
# env.password = 'wF6@cL1^jH5|fQ3'
# env.timeout = 60

def hello():
    print("Hello world!")

def hello1(name="world"):
    print("Hello %s!" % name)

def cluster():
    with cd('/home/ubuntu/data/zhengchubin/textmining/textming2017/mongodb'):
        run('nohup python3.5 -u updateCluster2MongoByTfidfNew.py > cluster.log&', pty=False)

env.hosts = ['120.79.123.139']
env.user = 'root'
env.password = 'wF6@cL1^jH5|fQ3'
# env.shell = "/bin/sh -c"
env.timeout = 60
def test():
    with cd('/root/zhengchubin/fabric'):
        run('nohup python3.5 -u demo.py > test.log&', pty=False)

if __name__ == '__main__':
    print('clustering')
    # execute(cluster)
    execute(test)
    print('Task Done.')