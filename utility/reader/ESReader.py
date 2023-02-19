#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch,VERSION

class ESReader(object):
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

    def _init(self):
        hosts = []
        if type(self._host) is list:
            hosts = [{'host':self._host[i], 'port': self._port[i]} for i in range(len(self._host))]
        else:
            hosts = [{'host': self._host, 'port': self._port}]

        ES = Elasticsearch(hosts=hosts,
                           timeout=self._timeout,
                           max_retries=self._max_retries,
                           retry_on_timeout=self._retry_on_timeout,
                           maxsize=self._max_size)
        return ES

    def getById(self, _id, _source_include=None):
        if not self._db: self._db = self._init()

        data = self._db.get(index=self._index, doc_type=self._type, id=_id, _source_include=_source_include)
        return data

    def es_search(self, query, aggs=False):
        ''' 查询 '''
        if not self._db: self._db = self._init()

        data = {}
        if VERSION[0]>=7:
            data = self._db.search(index=self._index, body=query)
        else:
            data = self._db.search(index=self._index, doc_type=self._type, body=query)
        total = data['hits']['total']
        hits = data['hits']['hits']
        if aggs:
            return data['aggregations']
        return total,hits

    def processing_hit(*args):
        """
        Decorator that pops all accepted parameters from method's kwargs and puts
        them in the params argument.
        """
        def _wrapper(func):
            return func(*args)
        return _wrapper

    def es_scroll_init(self, query, scroll_time, size):
        '''
        初始化scroll
        :param query:           scroll 的查询语句
        :param scroll_time:     失效时间
        :return:
        '''
        if not self._db: self._db = self._init()

        data = {}
        if VERSION[0]>=7:
            data = self._db.search(index=self._index, body=query, scroll=scroll_time, size=size)
        else:
            data = self._db.search(index=self._index, doc_type=self._type, body=query, scroll=scroll_time, size=size)

        sc_id = data['_scroll_id']
        total = data['hits']['total']
        hits = data['hits']['hits']
        return sc_id,total,hits

    def es_scroll(self, query, scroll_time='5m', size=300):
        '''
        滚屏，用法: for hits in ES.es_scroll(sc_id=sc_id):
        :param sc_id:   scroll_id
        :return:
        '''
        if not self._db: self._db = self._init()

        sc_id,total,hits = self.es_scroll_init(query, scroll_time, size)
        yield hits

        while True:
            data = self._db.scroll(scroll_id=sc_id, scroll=scroll_time)
            hits = data['hits']['hits']
            if not hits:
                break
            yield hits