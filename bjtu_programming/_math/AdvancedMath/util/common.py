# !/usr/bin/env python3
# -*- coding : utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

#####################################################################
## 通用方法
#####################################################################
def setAxis():
    '''使坐标原点为 (0,0)'''
    # 获取当前的坐标轴, gca = get current axis(坐标轴)
    ax = plt.gca()
    # 不显示右、上边框, spines(框、脊梁骨)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # 定位在 y=0 的位置, 位置所有属性：outward，axes(轴)，data(数据)
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))

def plotVertex2XAxisYAxis(x, y, num=25, color='black'):
    '''绘点 (x,y) 分别到 x、y 轴的虚线'''
    if x >= 0:
        # 到 y 轴
        x1 = np.linspace(0, x, num)
        y1 = np.linspace(y, y, num)
        # 到 x 轴
        x3 = np.linspace(x, x, num)
        y3 = np.linspace(0, y, num)
        plt.plot(x1, y1, linestyle='--', color=color)
        plt.plot(x3, y3, linestyle='--', color=color)
    else:
        # 到 y 轴
        x2 = np.linspace(x, 0, num)
        y2 = np.linspace(y, y, num)
        # 到 x 轴
        x4 = np.linspace(x, x, num)
        y4 = np.linspace(y, 0, num)
        plt.plot(x2, y2, linestyle='--', color=color)
        plt.plot(x4, y4, linestyle='--', color=color)

def plotLine(x=None, y=None, omin=-50, omax=50, num=25, color='black'):
    if x is not None:
        x1 = np.linspace(x, x, num)
        y1 = np.linspace(omin, omax, num)
        plt.plot(x1, y1, linestyle='--', color=color)
    else:
        x1 = np.linspace(omin, omax, num)
        y1 = np.linspace(y, y, num)
        plt.plot(x1, y1, linestyle='--', color=color)

def annotate(mdText, x, y, xoffset=0.15, yoffset=0.15, hasArrow=True):
    '''
    标注某个点y
    :param mdText: 标注信息，支持MarkDown语法, eg: r"$arcsin(-1)= -\frac{\pi}{2}$"
    :param x:      标注点 x 坐标
    :param y:      标注点 y 坐标
    :param xoffset: 标注信息和标注点之间的偏移量
    :return:
    '''
    # 标注信息的位置
    xtext = x
    ytext = y

    if x>=0:
        xtext += xoffset
    else :
        xtext -= xoffset
    if y>=0:
        ytext += yoffset
    else:
        ytext -= yoffset

    if hasArrow:
        plt.annotate(mdText,
                 xy=(x, y), xycoords='data',
                 xytext=(xtext, ytext), textcoords='data', fontsize=8,
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="arc3"),
                 )
    else:
        plt.annotate(mdText,
                     xy=(x, y), xycoords='data',
                     xytext=(xtext, ytext), textcoords='data', fontsize=8
                     )




