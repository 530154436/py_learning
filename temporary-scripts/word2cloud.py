# !/usr/bin/env python3
# -*- coding : utf-8 -*-
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# import cv2

def loadWords(path, seperator=' ', debug=False):
    with open(path, mode='r', encoding='utf8') as f:
        word_freq = {}
        for line in f:
            if len(word_freq) == 100:
                break
            line = line.strip().split(seperator)
            if len(line) == 2:
                key = line[0]
                if '/' in key:
                    key = key.split('/')[-1]
                word_freq[key] = float(line[1])
            else:
                print('未被加载词汇：',line)
        # 排序
        if debug:
            k_v = sorted(word_freq.items(), key= lambda item:item[1], reverse=True)
            for k, v in enumerate(k_v):
                print(k, v)
        return word_freq

# 调整图片大小
# img = cv2.imread('main.jpeg')
# height, width = img.shape[:2]
# res = cv2.resize(img,(3*width, 3*height), interpolation = cv2.INTER_CUBIC)
# cv2.imwrite('main_resize.jpeg', res)

backgroud_Image = plt.imread('main.jpeg')
word_freq = loadWords('words.txt', debug=True)
word_cloud = WordCloud( background_color= "white",
                        mask = backgroud_Image,
                        font_path='SIMHEI.TTF',   # 指定中文字体，默认不支持中文
                        max_font_size=100,# 设置字体最大值
                        random_state=30   # 设置有多少种随机生成状态，即有多少种配色方案
                      ).generate_from_frequencies(word_freq)

plt.imshow(word_cloud)
plt.axis("off")
plt.show()