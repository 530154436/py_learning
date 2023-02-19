# !/usr/bin/env python3
# -*- coding : utf-8 -*-

import sys
import os
import re

# 阅读背景
Regex = '^[Uu]nit.+[0-9]+.+$'
EN_CN_Regex = '([a-zA-Z]+.+[a-zA-Z]+).*?([\u4e00-\u9a5f]+)'
Suject_Compiler = re.compile(Regex)
EN_CN_Compiler = re.compile(EN_CN_Regex)

# 真题
englishRegex = '^[a-zA-Z]+$'
chinese_Regex = '^[a-zA-Z]+\..+[\u4e00-\u9a5f]+.+$'
english_Compiler = re.compile(englishRegex)
chinese_Compiler = re.compile(chinese_Regex)

# 真题词汇
year_regex = '[0-9]+ '
title_regex = '[Tt]ext [0-9]+|[Pp]art [Bb]|[Ss]ection I'
en_regex = '[a-zA-Z]+[^\u4e00-\u9a5f\(]*?[a-zA-Z]+'
cn_regex = '[\u4e00-\u9a5f]+.*?[\u4e00-\u9a5f]+'
year_compiler = re.compile(year_regex)
title_compiler = re.compile(title_regex)
en_Compiler = re.compile(en_regex)
cn_Compiler = re.compile(cn_regex)

Main_Dir = '/Users/zhengchubin/Desktop/HIT/英语/阅读理解词汇'
Reading = '阅读.txt'
Examination = '真题.txt'
ExaminationWords = '真题重点词汇.txt'

reading = 'reading'
examination = 'examination'
examination_words = 'reading_words'

__methods_fileName = {reading:Reading, examination:Examination, examination_words:ExaminationWords}

def save2file(method, file, words, onlyWord=True):
    '''
    保存文件
    :param file:
    :param words:
    :param onlyWord:
    :return:
    '''
    direction = os.path.join(Main_Dir, method)
    if not os.path.exists(direction):
        os.mkdir(direction)

    with open(os.path.join(direction, file), mode='w', encoding='utf-8') as f:
        if isinstance(words, tuple):
            for k,v in words:
                if onlyWord:
                    f.write('{}\n'.format(k))
                    f.flush()
                else:
                    f.write('{} {}\n'.format(k,v))
                    f.flush()
        elif isinstance(words, dict):
            for k,v in words.items():
                f.write('{}\n'.format(k))
                for word in v:
                    f.write('{}\n'.format(word))
                    f.flush()
                f.write('\n')
    print('Save to {}, Done.\n'.format(os.path.join(direction, file)))

def process(method):
    '''
    处理
    :param method:
    :return:
    '''
    file = os.path.join(Main_Dir, __methods_fileName[method])
    print('Opening file: {}'.format(file))
    if method == reading:
        with open(file, mode='r', encoding='utf-8') as f:
            units = {}

            subject = None
            words = []
            for line in f:
                # 匹配类别
                if re.match(Suject_Compiler, line):
                    if len(words) != 0:
                        units[subject] = words
                        words = []

                    subject = line
                else:
                    if len(line) == 0:
                        continue
                    en_cn = re.findall(EN_CN_Compiler, line)
                    words.extend(en_cn)

            if len(words) != 0:
                units[subject] = words

            for k,v in units.items():
                print(k)
                words = []
                phrase = []

                # 将短语和单词分组
                for item in v:
                    if ' ' in item[0] or '-' in item[0] or '(' in item[0] :
                        phrase.append(item)
                    else:
                        words.append(item)
                words.extend(phrase)
                save2file(reading, '{}_EN.txt'.format(k.strip()), words, True)
                save2file(reading, '{}_EN_CN.txt'.format(k.strip()), words, False)

    if method == examination:
        with open(file, mode='r', encoding='utf-8') as f:
            words = []
            en = ''
            cn = ''
            for line in f:

                if len(line) == 0:
                    continue
                if re.match(english_Compiler, line):
                    en = line
                elif re.match(chinese_Compiler, line):
                    cn = line
                else:
                    continue

                if en and cn:
                    words.append((en.strip(), cn.strip()))
                    en = ''
                    cn = ''

            save2file(examination, '{}_EN.txt'.format('真题词汇'), words, True)
            save2file(examination, '{}_EN_CN.txt'.format('真题词汇'), words, False)

    if method == examination_words:
        with open(file, mode='r', encoding='utf-8') as f:
            year_title_words = {}
            year = ''
            title =''
            for line in f:
                if re.match(year_compiler, line):
                    year = re.findall(year_compiler, line)[0]
                elif re.match(title_compiler, line):
                    title = re.findall(title_compiler, line)[0]
                else:
                    if re.match(en_Compiler, line):
                        chapter = '# {} {}'.format(year.strip(), title)
                        en = ' '.join(re.findall(en_Compiler, line))

                        if chapter not in year_title_words:
                            year_title_words[chapter] = []
                        year_title_words[chapter].append(en)
            save2file(examination, '{}_EN.txt'.format('真题重点词汇'), year_title_words, True)

def readWords(method):
    '''
    预处理
    :param path:
    :param method:
    :return:
    '''
    if method in __methods_fileName.keys():
        return process(method)
    else:
        raise Exception("Such method doesn't exist.")

def main():
    # readWords(reading)
    # readWords(examination)
    readWords(examination_words)

if __name__ == '__main__':
    main()