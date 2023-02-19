# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import time
import threading
import numpy as np
import pandas as pd
import functools
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

# Define a function to be applied to the dataframe
def add_func(a, b):
    return a+b

# Apply to dataframe
def apply_to_df(df_chunk):
    '''
    操作 DF
    :param df_chunk:
    :return:
    '''
    result = df_chunk.apply(lambda x: add_func(x['a'], x['b']), axis=1)
    print(f'Pro-id({os.getpid()}), Thread-Name({threading.current_thread().name}): '
          f'finished chunk {df_chunk.index.min()}-{df_chunk.index.max()}')
    return result

def apply_to_df_index(chunk_indices, data):
    '''
    操作 DF
    :param indices_chunk:
    :return:
    '''
    chunk_result = data.loc[chunk_indices].apply(lambda x: add_func(x['a'], x['b']), axis=1)
    print(f'Pro-id({os.getpid()}), Thread-Name({threading.current_thread().name}): '
          f'finished chunk {chunk_indices.min()}-{chunk_indices.max()}')
    return chunk_result

def parallel(data, threads_num=16, chunk_size=1000):
    '''
    并发执行 Pandas 的 apply 方法
    :param data:        数据帧
    :param threads_num: 进程数
    :param chunk_size:  分块大小
    :return:
    '''
    start = time.time()
    # 根据索引进行分块
    chunks = [data.loc[data.index[i:i + chunk_size]] for i in range(0, data.shape[0], chunk_size)]
    # chunks_indices = [data.index[i:i + chunk_size] for i in range(0, data.shape[0], chunk_size)]

    # 线程池
    # with ThreadPool(threads_num) as p: result = p.map(apply_to_df, chunks)

    # 进程池
    with Pool(threads_num) as p: results = p.map(func=functools.partial(apply_to_df),
                                                 iterable=chunks)
    # with Pool(threads_num) as p: results = p.map(func=functools.partial(apply_to_df_index, data=data),
    #                                              iterable=chunks_indices)

    # Concat all chunks
    chunk_results = pd.concat(results) # 纵向拼接
    chunk_results.name = 'sum'
    print(f'All Finshed({round(time.time()-start, 3)}s). New DataFrame:',chunk_results.shape)
    return chunk_results

if __name__ == '__main__':
    data = pd.DataFrame(np.random.random((100000, 2)), columns=['a', 'b'])
    sim = parallel(data, threads_num=4, chunk_size=1000)
    data = pd.concat([data, sim], axis=1)  # 横向拼接
    print(data.head())

    start = time.time()
    data['sum'] = data.apply(lambda x: add_func(x['a'], x['b']), axis=1)
    print(f'Finshed({round(time.time()-start, 3)}s).')