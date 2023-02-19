#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
"""
import jieba
import jieba.posseg
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer

import data_loader
from config import DATA_DIR

jieba.load_userdict(DATA_DIR.joinpath('userdict.txt').__str__())


def train():
    model = MultinomialNB()
    vectorizer = TfidfVectorizer(analyzer='word')
    dataset = data_loader.load_questions_template()

    # 对文本进行预处理
    dataset['text'] = dataset['text'].apply(
        lambda x: ' '.join(word.word for word in jieba.posseg.cut(x)))
    x = dataset['text'].values

    vectorizer.fit(x)
    x = vectorizer.transform(x)

    y = dataset['label'].apply(lambda x: int(x)).values

    model.fit(x, y)
    nb_predict = model.predict(x)
    print(nb_predict)

    print('----------------------- 朴素贝叶斯 -----------------------')
    print(classification_report(y, nb_predict))
    print("平均准确率\n", metrics.accuracy_score(y, nb_predict))

    return model, vectorizer

if __name__ == '__main__':
    train()