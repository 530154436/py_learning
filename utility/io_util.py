# !/usr/bin/env python3
# -*- coding : utf-8 -*-

import os

Debug = False

'''  操作io流   '''


def get_read_file_obj(file):

    """
    读取文本文件，默认编码为utf-8
    :param file: 文件路径
    :return: file
    """

    try:
        f = open(file, 'r', encoding='utf-8')
    except FileNotFoundError as e:
        print('文件不存在:',file)
        raise
    except TypeError as e :
        print('类型错误:', file)
        f.close()
        raise

    return f


def get_write_file_obj(file):

    """
    读取文本文件，默认编码为utf-8
    :param file: 文件路径
    :return:
    """

    try:
        f = open(file, 'w', encoding='utf-8')
    except FileNotFoundError as e:
        print('文件不存在: ', file)
        raise
    except TypeError as e:
        print('类型错误: ', file)
        f.close()
        raise
    return f


def load_dic(*dices, split=None):

    """
    读取多份字典
    :param dices: 每个字典的路径
    :param split: 词条分隔符
    :return: dict

    >>> file = '/test/corpus_1/dish/dic/filter/filter.txt'
    >>> load_dic(file)
    /test/corpus_1/dish/dic/filter/filter.txt 加载了 170 词条
    共加载了 170 词条

    """

    dictionary = {}
    old_size = 0
    for dic in dices:
        if '.DS_Store' in dic:
            continue

        f = get_read_file_obj(dic)
        old_size = len(dictionary)

        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                continue

            # 源码:若分隔符为空，则默认使用空格
            k_v = line.split(split)

            # key - value
            if len(k_v[1:]) == 1:
                dictionary[k_v[0]] =k_v[1]
            else:
                dictionary[k_v[0]] = k_v[1:]

            if Debug:
                print('key:', k_v[0], 'value:', dictionary[k_v[0]])

        print(dic, '加载了', len(dictionary) - old_size, '词条')
        f.close()
    print('共加载了', len(dictionary), '词条')

    return dictionary


def load_dices_from_folder(folder, split=None):

    """
    从指定目录读取多份字典
    :param folder:
    :return:

    >>> folder = '/test/corpus_1/dish/dic/filter'
    >>> load_dices_from_folder(folder)
    /test/corpus_1/dish/dic/filter/CustomDictionary.txt 加载了 57606 词条
    /test/corpus_1/dish/dic/filter/filter.txt 加载了 57769 词条
    /test/corpus_1/dish/dic/filter/restaurant_title.txt 加载了 235420 词条
    共加载了 235420 词条
    """

    # 获取目录下的所有文件
    path_list = os.listdir(folder);
    for i in range(len(path_list)):
        path_list[i] = os.path.join(folder, path_list[i])
    dictionary = load_dic(*path_list, split=split)
    return dictionary


def save_dic(dic, output, is_contain_value=False):
    """
    保存字典
    :param dic:
    :param output:
    :return:
    """
    if not isinstance(dic, dict):
        print('参数不是字典类型!')
        return False
    f = get_write_file_obj(output)
    for key in dic.keys():
        if is_contain_value:
            f.write(key+' '+ dic[key]+ '\n')
        else:
            f.write(key + '\n')
    print(output)
    print('共保存了', len(dic), '个词条')
    f.close()
    return True


def test():
    folder = '/test/corpus_1/dish/dic/filter'
    load_dices_from_folder(folder)
    file = '/test/corpus_1/dish/dic/filter/filter.txt'
    load_dic(file)


if __name__ == '__main__':
    test()
