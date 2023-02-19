#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import threading
import time

from config import logger
from elasticsearch import Elasticsearch,VERSION

class ESWriter:
    def __init__(self, hosts, ports, index,
                       type=None, timeout=3600, max_retries=5, retry_on_timeout=True, maxsize=80):
        self._host = hosts
        self._port = ports
        self._index = index
        self._type = type
        self._timeout = timeout
        self._max_retries = max_retries
        self._retry_on_timeout = retry_on_timeout
        self._max_size = maxsize
        self._db = self._init()
        self.total_count = 0

    def _init(self):
        hosts = []
        if type(self._host) is list:
            hosts = [{'host': self._host[i], 'port': self._port[i]} for i in range(len(self._host))]
        else:
            hosts = [{'host': self._host, 'port': self._port}]

        ES = Elasticsearch(hosts=hosts,
                           timeout=self._timeout,
                           max_retries=self._max_retries,
                           retry_on_timeout=self._retry_on_timeout,
                           maxsize=self._max_size)
        return ES

    def es_crate_index(self):
        pass

    def es_delete(self, id):
        return self._db.delete(self._index, self._type,id)

    def index(self, body, id=None, params=None):
        '''
        根据ID创建/覆盖doc, 注意会覆盖原数据
        :param body:   The document
        :param id:     Document ID
        :param params:
        :return:
        '''
        if not self._db: self._db = self._init()
        return self._db.index(index=self._index, doc_type=self._type, body=body, id=id)

    def update(self, body, id=None, params=None):
        '''
        根据ID更新doc部分字段
        :param body:   The document
        :param id:     Document ID
        :param params:
        :return:
        '''
        if not self._db: self._db = self._init()

        body = {'doc':body} # 或script
        return self._db.update(index=self._index, doc_type=self._type, body=body, id=id)

    def bulk(self, dataes, action, bulkSize=300):
        '''
        :param dataes:
            数据列表(dict):
                eg: [
                        { "doc":{ "field1":value1, "field2":value2} "_id":_id1},
                        { "doc":{ "field1":value1, "field2":value2} "_id":_id2}
                    ]

        :param action: index、update
        :return:
        '''
        if not self._db: self._db = self._init()
        bulk_threshold = 0
        if dataes:
            bulk_str = ''
            for data in dataes:
                actionJson = {}
                contentJson = {}
                if action=='index':
                    if data.get( '_id'):
                        _id = data['_id']
                        actionJson = {action: {"_type": self._type, "_index": self._index, "_id":_id}}
                        contentJson = data['doc']
                    else:
                        actionJson = {action: {"_type": self._type, "_index": self._index}}
                        contentJson = data['doc']
                elif action == 'update' and data.get('doc') and data.get('_id'):
                    actionJson = {"update": {"_type": self._type, "_index": self._index, "_id": data['_id']}}
                    contentJson = {"doc": data['doc']}
                else:
                    return 'Unsuppored action.'

                bulk_str += json.dumps(actionJson, ensure_ascii=False) + "\n" \
                          + json.dumps(contentJson,ensure_ascii=False) + "\n"
                self.total_count += 1
                bulk_threshold += 1

                if bulk_threshold >= bulkSize:
                    try:
                        start = time.time()
                        resp = self._db.bulk(body=bulk_str) #,params={'timeout':3600,'refresh':-1}
                        logger.info('==============================================')
                        logger.info("{} bulk -> {} time: {}".format(
                            threading.current_thread().name,self.total_count, str(time.time()-start)))
                        logger.info("errors {}".format(resp['errors']))
                        if resp['errors']:
                            logger.info(resp)
                            logger.info('==============================================\n')
                        bulk_str = ''
                        bulk_threshold = 0
                    except Exception as e:
                        logger.error('bulk error, sleeping 2 seconds.{}'.format(str(e)))
                        time.sleep(2)

            if bulk_threshold > 0:
                try:
                    start = time.time()
                    resp = self._db.bulk(body=bulk_str)
                    logger.info('==============================================')
                    logger.info("{} bulk -> {} time: {}".format(
                        threading.current_thread().name, self.total_count, str(time.time() - start)))
                    logger.info("errors {}".format(resp['errors']))
                    if resp['errors']:
                        logger.info(resp)
                    logger.info('==============================================\n')
                except Exception as e:
                    logger.error('bulk error, sleeping 2 seconds.{}'.format(str(e)))
                    time.sleep(2)

if __name__ == '__main__':
    from config import es_ip,es_port
    es_client = ESWriter(hosts=es_ip, ports=es_port, index='')

