# !/usr/bin/env python3
# -*- coding : utf-8 -*-
import numpy as np
import math
import matplotlib.pyplot as plt
from Math.AdvancedMath.util import common
from mpl_toolkits.mplot3d import Axes3D

def cot(x):
    '''余切'''
    return np.cos(x)/np.sin(x)

def sec(x):
    '''正割'''
    return 1/np.cos(x)

def csc(x):
    '''余割'''
    return 1/np.sin(x)

def lnxy(x,y):
    '''换底公式，任意底数求对数'''
    return np.log(y)/np.log(x)

def tmp():
    fig = plt.figure()
    ax = Axes3D(fig)
    X = np.arange(-3, 3, 0.15)
    Y = np.arange(-3, 3, 0.15)
    X, Y = np.meshgrid(X, Y)
    R = X ** 2 - Y
    Z = np.sin(R)

    # 具体函数方法可用 help(function) 查看，如：help(ax.plot_surface)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')

    plt.show()

#####################################################################
## 1. 三角函数
#####################################################################
def triFunction(function='sin', xmin=np.array([-2*np.pi]), xmax=np.array([2*np.pi]), ymin=-6, ymax=6):
    # 生成一个窗口
    plt.figure(1,dpi=120)
    # 定义域: [-pi, pi] ，共 100 个点, linspace=linear space 线性空间
    x = np.linspace(xmin, xmax, 100)
    if function=='sin':
        y = np.sin(x)
        common.plotVertex2XAxisYAxis(np.pi / 2, 1)
        common.plotVertex2XAxisYAxis(-np.pi / 2, -1)
        common.annotate(r"$(\frac{\pi}{2},1)$", np.pi / 2, 1, xoffset=0.15)
        common.annotate(r"$(-\frac{\pi}{2},-1)$", -np.pi / 2, -1, xoffset=0.15)
        plt.plot(x, y, label='正弦函数')
    elif function=='cos':
        y = np.cos(x)
        common.plotVertex2XAxisYAxis(np.pi, -1)
        common.plotVertex2XAxisYAxis(-np.pi, -1)
        common.annotate(r"$(\frac{\pi}{2},0)$", np.pi / 2, 0, xoffset=0.1)
        common.annotate(r"$(-\frac{\pi}{2},0)$", -np.pi / 2, 0, xoffset=1)
        common.annotate(r"$(\pi,-1)$", np.pi, -1, xoffset=0.15)
        common.annotate(r"$(-\pi,-1)$", -np.pi, -1, xoffset=0.15)
        plt.plot(x, y, label='余弦函数')
    elif function=='tan':
        x = np.linspace(xmin, xmax, 100)
        y = np.tan(x)
        plt.plot(x, y, label='正切函数')
        common.annotate(r"$x=\frac{\pi}{2}$", np.pi / 2 - 0.1, 3, xoffset=0.15, yoffset=0, hasArrow=False)
        common.annotate(r"$x=-\frac{\pi}{2}$", -np.pi / 2 + 0.1, 3, xoffset=-0.15, yoffset=0, hasArrow=False)
        # 限制坐标显示的范围
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
    elif function=='cot':
        x = np.linspace(xmin, xmax, 100)
        y = cot(x)
        plt.plot(x, y, label='余切函数')
        common.annotate(r"$(\frac{\pi}{2},0)$", np.pi / 2, 0, xoffset=0.25, yoffset=0.7)
        common.annotate(r"$(-\frac{\pi}{2},0)$", -np.pi / 2, 0, xoffset=0.25, yoffset=0.8)
        common.annotate(r"$x=\pi$", 2, 3, xoffset=0.15, yoffset=0, hasArrow=False)
        common.annotate(r"$x=-\pi$", -4.5, 3, xoffset=0.15, yoffset=0, hasArrow=False)
        # 限制坐标显示的范围
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
    elif function=='sec':
        x = np.linspace(xmin, xmax, 100)
        y = sec(x)
        plt.plot(x, y, label='正割函数')
        common.annotate(r"$(\frac{\pi}{2},%s)$" % sec(0), 0, sec(0), xoffset=0.25, yoffset=-0.7)
        common.annotate(r"$x=-\frac{\pi}{2}$", -2.5, 3, xoffset=0.15, hasArrow=False)
        common.annotate(r"$x=-\frac{\pi}{2}$", np.pi / 2, 3, xoffset=0.15, hasArrow=False)
        # 限制坐标显示的范围
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
    elif function=='csc':
        x = np.linspace(xmin, xmax, 100)
        y = csc(x)
        plt.plot(x, y, label='余割函数')
        common.annotate(r"$(\frac{\pi}{2},%s)$" % csc(np.pi / 2), np.pi / 2, csc(np.pi / 2), xoffset=0.25, yoffset=-0.7)
        common.annotate(r"$x=\pi$", np.pi, 3, xoffset=0.15, hasArrow=False)
        # 限制坐标显示的范围
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)

    # 画图
    plt.legend(loc='upper right')
    common.setAxis()
    plt.show()

def testTri():
    # triFunction('sin')
    # triFunction('cos')
    # triFunction('tan')
    # triFunction('cot')
    # triFunction('sec')
    triFunction('csc')

#####################################################################
## 2. 反三角函数
#####################################################################
def atriFunction(function='sin', xmin=np.array([-1]), xmax=np.array([1]), ymin=-np.pi/2, ymax=np.pi/2):
    # 生成一个窗口
    plt.figure(1,dpi=120)
    # 定义域: [-pi, pi] ，共 100 个点, linspace=linear space 线性空间
    x = np.linspace(xmin, xmax, 100)
    if function=='asin_acos':
        y = np.arcsin(x)
        plt.plot(x, y, label='反正弦函数 arcsin')

        y = np.arccos(x)
        plt.plot(x, y, label='反余弦函数 arccos')

        common.plotVertex2XAxisYAxis(-1, -np.pi / 2)
        common.plotVertex2XAxisYAxis(1, np.pi / 2)
        common.plotVertex2XAxisYAxis(-1, np.pi)
        common.annotate(r"$(-1,-\frac{\pi}{2})$", -1, -np.pi / 2, xoffset=0.3)
        common.annotate(r"$(1,\frac{\pi}{2})$", 1, np.pi / 2, xoffset=0.08)
        common.annotate(r"$(-1,\pi)$", -1, np.pi, xoffset=0.2)
    elif function=='atan_acot':
        xmin = -10
        xmax = 10
        x = np.linspace(xmin, xmax, 100)
        y = np.arctan(x)
        plt.plot(x, y, label='反正切函数')

        x1 = np.linspace(0.1, np.pi, 100)
        y1 = cot(x1)
        plt.plot(y1, x1, label='反余切函数')

        common.plotLine(y=np.pi)
        common.plotLine(y=-np.pi / 2)
        common.annotate(r"$(0,-\frac{\pi}{2})$", 0, -np.pi / 2, xoffset=0.5, yoffset=0.4)
        common.annotate(r"$(0,\pi)$", 0, np.pi, xoffset=0.5, yoffset=0.3)
        # 限制坐标显示的范围
        plt.xlim(xmin, xmax)
        plt.ylim(ymin-1, np.pi+1)
    elif function=='asec_acsc':
        x11 = np.linspace([0.1], [np.pi/2-0.01], 100)
        x12 = np.linspace([np.pi/2+0.01], np.pi, 100)
        plt.plot(sec(x11), x11, label='反正割函数', color='orange')
        plt.plot(sec(x12), x12, color='orange')

        x11 = np.linspace([-np.pi / 2],  [0-0.01], 100)
        x12 = np.linspace([0 + 0.01], [np.pi/2], 100)
        plt.plot(csc(x11), x11, label='反余割函数', color='green')
        plt.plot(csc(x12), x12, color='green')

        common.annotate(r"$x=\pi$", 0, np.pi, xoffset=0.15, hasArrow=False)
        common.annotate(r"$x=-\frac{\pi}{2}$", 0, -np.pi / 2, xoffset=0.15, yoffset=0.3, hasArrow=False)
        common.plotLine(y=np.pi)
        common.plotLine(y=-np.pi / 2)

        # 限制坐标显示的范围
        plt.xlim(-10, 10)
        plt.ylim(ymin - 1, np.pi + 1)
    # 画图
    plt.legend(loc='upper right')
    common.setAxis()
    plt.show()

def testATri():
    # atriFunction('asin_acos')
    # atriFunction('atan_acot')
    atriFunction('asec_acsc')

#####################################################################
## 3. 幂函数
#####################################################################
def powerFunction(xmin=-5, xmax=5, ymin=-5, ymax=5):
    x = np.linspace(xmin, xmax, 100)

    #############################
    ## (1) a>0
    #############################
    # 生成一个窗口
    plt.figure(1, dpi=120)
    plt.title('幂函数 a>0')
    y1 = np.power(x, 1)
    plt.plot(x, y1, label='a=1')

    y2 = np.power(x, 2)
    plt.plot(x, y2, label='a=2')

    y3 = np.power(x, 3)
    plt.plot(x, y3, label='a=3')

    common.plotVertex2XAxisYAxis(1, 1)
    common.plotVertex2XAxisYAxis(-1, -1)
    common.annotate(r'$(-1,-1)$', -1, -1, xoffset=1.5, yoffset=-0.1)
    common.plotVertex2XAxisYAxis(1, 1)
    common.annotate(r'$(1,1)$', 1, 1, xoffset=0.3, yoffset=-0.5)

    y2 = np.cbrt(x)
    plt.plot(x, y2, label=r'$a=\frac{1}{3}$')

    x1 = np.linspace(0, xmax, num=100)
    y1 = np.power(x1, 1/2)
    plt.plot(x1, y1, label=r'$a=\frac{1}{2}$')

    # 画图
    plt.legend(loc='lower right')
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    common.setAxis()
    plt.show()

    #############################
    ## (2) a<0
    #############################
    # 生成一个窗口
    plt.figure(1, dpi=120)
    plt.title('幂函数 a<0')
    y1 = np.power(x, -1)
    plt.plot(x, y1, label='a=-1')

    y2 = np.power(x, -2)
    plt.plot(x, y2, label='a=-1')

    common.plotVertex2XAxisYAxis(1, 1)
    common.annotate(r'$(1,1)$', 1, 1, xoffset=0.3, yoffset=0.5)

    # 画图
    plt.legend(loc='upper right')
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    common.setAxis()
    plt.show()

#####################################################################
## 4. 指数函数
#####################################################################
def exp(xmin=-5, xmax=5, ymin=-5, ymax=5):
    x = np.linspace(xmin, xmax, 100)

    #############################
    # 生成一个窗口
    plt.figure(1, dpi=120)
    plt.title('指数函数')

    y2 = np.power(1, x)
    plt.plot(x, y2, label='a=1')

    y1 = np.power(np.e, x)
    plt.plot(x, y1, label='a=e')

    y3 = np.power(3, x)
    plt.plot(x, y3, label='a=3')

    common.plotVertex2XAxisYAxis(0, 1)
    common.annotate(r'$(0,1)$', 0, 1, xoffset=0.3, yoffset=-0.5)

    # 画图
    plt.legend(loc='upper right')
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    common.setAxis()
    plt.show()

#####################################################################
## 5. 对数函数
#####################################################################
def log(xmin=0.001, xmax=5, ymin=-5, ymax=5):
    x = np.linspace(xmin, xmax, 100)

    #############################
    # 生成一个窗口
    plt.figure(1, dpi=120)
    plt.title('对数函数')

    y4 = lnxy(0.5, x)
    plt.plot(x, y4, label='a=0.5')

    y1 = np.log2(x)
    plt.plot(x, y1, label='a=2')

    y2 = np.log(x)
    plt.plot(x, y2, label='a=e')

    y3 = np.log10(x)
    plt.plot(x, y3, label='a=10')

    common.annotate(r'$(1,0)$', 1, 0, xoffset=0, yoffset=0.5)

    # 画图
    plt.legend(loc='upper right')
    plt.xlim(-1, xmax)
    plt.ylim(ymin, ymax)
    common.setAxis()
    plt.show()

#####################################################################
## 6. 双曲函数、反双曲函数
#####################################################################
def triH(xmin=-4, xmax=4, ymin=-4, ymax=4):
    x = np.linspace(xmin, xmax, 100)

    #############################
    # 生成一个窗口
    plt.figure(1, dpi=120)
    plt.title('双曲函数')

    y1 = np.sinh(x)
    plt.plot(x, y1, label=r'$sinh(x)=\frac{e^x-e^{-x}}{2}$')

    y2 = np.cosh(x)
    plt.plot(x, y2, label=r'$cosh(x)=\frac{e^x+e^{-x}}{2}$')

    y3 = np.tanh(x)
    plt.plot(x, y3, label=r'$tanh(x)=\frac{sinh(x)}{cosh(x)}$')

    common.plotLine(y=-1)
    common.plotLine(y=1)

    # 画图
    plt.legend(loc='lower right')
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    common.setAxis()
    plt.show()

    # 生成一个窗口
    plt.figure(2, dpi=120)
    plt.title('反双曲函数')

    y1 = np.arcsinh(x)
    plt.plot(x, y1, label=r'$arcsinh(x)=\frac{e^x-e^{-x}}{2}$')

    x = np.linspace(1, xmax)
    y2 = np.arccosh(x)
    plt.plot(x, y2, label=r'$arccosh(x)=\frac{e^x+e^{-x}}{2}$')

    x = np.linspace(-0.9999, 0.9999)
    # x = np.linspace(xmin, xmax, 100)
    y3 = np.arctanh(x)
    plt.plot(x, y3, label=r'$arctanh(x)=\frac{sinh(x)}{cosh(x)}$')

    common.plotLine(x=-1)
    common.plotLine(x=1)

    # 画图
    plt.legend(loc='lower right')
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    common.setAxis()
    plt.show()

#####################################################################
## 7. x、sinx、cosx、tans、lnx
#####################################################################
def x_sinx_cosx_tanx_lnx():
    xmin, xmax,  ymin, ymax = 0, np.pi, -np.pi, np.pi
    x = np.linspace([xmin], [xmax])

    # 生成一个窗口
    plt.figure(1, dpi=120)
    plt.title('初等函数')

    plt.plot(x, x, label=r'$y=x$')

    # sinx = np.sin(x)
    # plt.plot(x, sinx, label=r'$y=sin(x)$')
    #
    # cosx = np.cos(x)
    # plt.plot(x, cosx, label=r'$y=cos(x)$')

    # tanx = np.tan(x)
    # plt.plot(x, tanx, label=r'$y=tan(x)$')

    lnx = np.log(x)
    plt.plot(x, lnx, label=r'$y=ln(x)$')

    exp = np.exp(x)
    plt.plot(x, exp, label=r'$y=e^{(x)}$')

    common.plotLine(y=-1)
    common.plotLine(y=1)
    common.plotLine(x=1 / 2 * np.pi)

    # 画图
    plt.legend(loc='lower right')
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    common.setAxis()
    plt.show()

if __name__ == '__main__':
    # testTri()
    # testATri()
    # powerFunction()
    # exp()
    # log()
    # triH()
    x_sinx_cosx_tanx_lnx()