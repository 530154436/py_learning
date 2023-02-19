#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
小A正在开展面向领域的自然语言处理研究，这项工作的第一步就是建立语料字典，即从给定的语料库中，
分割并提取相应的词汇，并将词汇按某种顺序排列，从而发现该领域中的标识性词汇，为进一步研究奠定基础。

这项工作费时费力且比较枯燥，需要删除语句中的标点符号、连字符等（单词跨行的视为两个独立的单词），
还要去掉所有格，并按空白进行单词分割，实在是太麻烦了，他希望你能够编写一个计算机程序帮他解决这个问题。

输入
输入数据不超过500行，每行最多包括200个ASCII码大小写子母和标点符号，单词之间以空格分隔。

输出
输出小写形式的所有单词。单词不区分大小写，由26个英文字母构成。
请按单词出现次数从高到低及字典序依次输出所有的单词，要求每个单词在单独的行中输出。

示例输入
Peter's Adventures in Disneyland
Two blondes were going to Disneyland when they came to a fork in the road. The sign read: "Disneyland Left."
So they went home.

示例输出
disneyland
in
the
they
to
a
adventures
blondes
came
fork
going
home
left
peter
read
road
sign
so
two
went
were
when
"""
import re
import sys
from collections import Counter

COMPILER = re.compile('\'s|[\s\-\[\]\'\-!"#$%&()*+,./:;<=>?@^_`{|}~‘’“”〝〞（）'
                      '〈〉‹›﹛﹜『』〖〗［］《》〔〕「」【】。，、＇：∶；ˆˇ﹕︰﹔﹖﹑·¨…¸！'
                      '´？～—ˉ｜‖＂〃｀@﹫¡¿﹏﹋﹌︴々﹟﹩﹠﹪﹡﹢﹦﹤‐￣¯―﹨˜﹍﹎＿﹉﹊︷'
                      '︿︹︽﹁﹃︻︶︸﹀︺︾﹂﹄︼!"#$%&\'()*+,./:;<=>?@^_`{|}~]+')

dic = Counter()

for line in sys.stdin:
    line = line.strip()
    line = line.replace('-', '')
    if not line:
        break
    words = COMPILER.split(line)
    dic.update(Counter(word.lower() for word in words if word))

sorted_dic = sorted(dic.items(), key=lambda x: x[0], reverse=False)  # 字典序
sorted_dic = sorted(sorted_dic, key=lambda x: x[1], reverse=True)    # 频数序

for k, v in sorted_dic:
    print(k)