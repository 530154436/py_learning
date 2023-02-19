# /usr/bin/env python3
# -*- coding:utf-8 -*-
import pandas as pd
from log_util import logger

def readCsv2PdByChunkSize(origin, fields, chunk_size=1000):
    '''
    pandas 分块读取
    '''
    documents = pd.read_csv(origin, usecols=fields, chunksize=chunk_size)
    chunk_list = []
    for doc in documents:
        chunk_list.append(doc)
        logger.info("读取 {} : {}".format(origin, len(doc)))
    df_concat = pd.concat(chunk_list)
    return df_concat