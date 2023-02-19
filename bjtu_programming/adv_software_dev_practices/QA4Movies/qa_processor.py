#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@time: 2021/08/28
@function:
"""
import jieba
import jieba.posseg
from classifier import train
from answer import QAProcessor

model, vectorizer = train()

QA_TEMPLATE = {
    1: QAProcessor.template_1,
    2: QAProcessor.template_2,
    3: QAProcessor.template_3,
    4: QAProcessor.template_4,
    5: QAProcessor.template_5,
    6: QAProcessor.template_6,
    7: QAProcessor.template_7,
    8: QAProcessor.template_8
}

def run(_input: str):
    result = ''

    if not _input:
        return result

    # 分词_词性标注
    segments = jieba.posseg.cut(_input)
    print('分词', segments)

    # 构造参数
    actor1, actor2, movie = None, None, None
    word_flag = []
    for token in segments:
        word_flag.append((token.word, token.flag))
        if token.flag == 'person':
            if actor1 is None:
                actor1 = token.word
            else:
                actor2 = token.word
        elif token.flag == 'movie':
            movie = token.word

    # 没有实体直接返回
    if not (actor1 or actor2 or movie):
        return result

    # 构造特征
    feats = vectorizer.transform([' '.join(i[0] for i in word_flag)])

    # 预测分类
    y_pred = model.predict(feats)[0] + 1
    print('问题模板: ', y_pred)

    # 获取相应的问题模板
    answer_func = QA_TEMPLATE.get(y_pred, None)

    if actor1 and actor2:
        func = QA_TEMPLATE.get(7, None)
        return func(actor1, actor2)

    # 只有1个演员的参数
    if y_pred in (1, 5, 8):
        result = answer_func(actor1)

    # 只有1个电影的参数
    elif y_pred in (2, 3, 4, 6):
        result = answer_func(movie)

    # 2个演员的参数
    elif y_pred==7:
        result = answer_func(actor1, actor2)

    return result


if __name__ == '__main__':
    res = run('周润发演过哪些电影？卧虎藏龙')
    print(res)