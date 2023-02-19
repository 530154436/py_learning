#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import hashlib
from pymongo import bulk
from pymongo.errors import BulkWriteError

class MongoDBWriter:
    def __init__(self, client, dbName, collectionName, filter=None, userName=None, password=None):
        self.client = client
        self.dbName = dbName
        self.collectionName = collectionName

        self.filter = filter

        self.total_miss_count = 0
        self.nMatched = 0
        self.nModified = 0
        self.nInserted = 0
        self.writeErrors = 0

    def writeBulk(self, documents, size=500, ordered=False):
        '''
        批量写
        :param db:  数据库名 str
        :param collection:  集合名 collection
        :param documents:  dict 列表
        :param size:  每批次写入数据
        :param ordered: False:当发生异常(主键重复)时，还会将其他数据写入
        :return:
        '''
        collection = self.client[self.dbName][self.collectionName]
        _bulk = bulk.BulkOperationBuilder(collection, ordered=ordered)
        count = 0
        for document in documents:

            if self.filter is not None:
                document = self.filter(document)
                if not document:
                    self.total_miss_count += 1
                    continue

            # 去重
            count += 1
            md5 = hashlib.md5()
            md5.update((str(document['id']) + "_" + str(document['appCode'])).encode(encoding='utf-8'))
            _id = md5.hexdigest()
            document['_id'] = _id

            _bulk.insert(document)
            if count%size==0:
                try:
                    resp =  _bulk.execute()
                    self.nInserted += resp['nInserted']
                except BulkWriteError as bwe:
                    if 'nInserted' in bwe.details:
                        self.nInserted += bwe.details['nInserted']
                    if 'writeErrors' in bwe.details:
                        self.writeErrors = len(bwe.details['writeErrors'])
                except Exception as e:
                    logging.info(e)
                # logging.info('{} {} filter: {}, nMatched: {}, nInserted: {}, writeErrors: {}'
                #              .format(self.dbName, self.collectionName, self.total_miss_count, self.nMatched, self.nInserted, self.nModified))
                _bulk = bulk.BulkOperationBuilder(collection, ordered=ordered)
        if count>0:
            try:
                resp = _bulk.execute()
                self.nInserted += resp['nInserted']
            except BulkWriteError as bwe:
                if 'nInserted' in bwe.details:
                    self.nInserted += bwe.details['nInserted']
                if 'writeErrors' in bwe.details:
                    self.writeErrors = len(bwe.details['writeErrors'])
            except Exception as e:
                logging.info(e)
            # logging.info('{} {} filter: {}, nMatched: {}, nInserted: {}, writeErrors: {}'
            #              .format(self.dbName, self.collectionName, self.nMatched, self.nInserted, self.nModified, self.writeErrors))

    def updateBulkBy_id(self, documents, updateField, size=500, ordered=False):
        '''
        批量更新
        :param db:  数据库名 str
        :param collection:  集合名 collection
        :param documents:  dict 列表(文档中需要含有_id字段)
        :param size:  每批次写入数据
        :param ordered: False:当发生异常(主键重复)时，还会将其他数据写入
        :return:
        '''
        collection = self.client[self.dbName][self.collectionName]
        count = 0
        _bulk = bulk.BulkOperationBuilder(collection, ordered=ordered)
        for document in documents:
            if updateField not in document:
                continue
            count += 1
            _bulk.find({'_id': document['_id']}).update_one({'$set': {updateField: document[updateField]}})
            if count % size == 0:
                try:
                    resp = _bulk.execute()
                    self.nMatched += resp['nMatched']
                    self.nInserted += resp['nInserted']
                    self.nModified += resp['nModified']
                except Exception as e:
                    logging.warning(e)
                logging.info('{} {} nMatched: {}, nInserted: {}, nModified: {}, writeErrors: {}'
                             .format(self.dbName, self.collectionName, self.nMatched, self.nInserted, self.nModified, self.writeErrors))
                _bulk = bulk.BulkOperationBuilder(collection, ordered=ordered)
        if count > 0:
            try:
                resp = _bulk.execute()
                self.nMatched += resp['nMatched']
                self.nInserted += resp['nInserted']
                self.nModified += resp['nModified']
            except Exception as e:
                logging.warning(e)
            logging.info('{} {} nMatched: {}, nInserted: {}, nModified: {}, writeErrors: {}'
                         .format(self.dbName, self.collectionName, self.nMatched, self.nInserted, self.nModified, self.writeErrors))

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info('Operation done. {} {}  filter: {}, nMatched: {}, nInserted: {}, nModified: {}, writeErrors: {}'
                     .format(self.dbName, self.collectionName, self.total_miss_count, self.nMatched, self.nInserted, self.nModified, self.writeErrors))

    def __enter__(self):
        return self