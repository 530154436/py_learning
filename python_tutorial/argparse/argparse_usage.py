# !/usr/bin/env python3
# -*- coding : utf-8 -*-
import sys
import argparse

def test():
    print(sys.argv)
    print(sys.argv[1])

# 简单示例
def test01():
    parser = argparse.ArgumentParser(description='APP Cluster')
    parser.add_argument('integer', type=int, help='display an integer')
    args = parser.parse_args()

    print(args.integer)

    # 定位参数
    print(args.integer**2)

# 可选参数
def test02():
    parser = argparse.ArgumentParser()

    parser.add_argument("--square", help="display a square of a given number", type=int)
    parser.add_argument("--cubic", help="display a cubic of a given number", type=int)

    args = parser.parse_args()

    if args.square:
        print(args.square ** 2)

    if args.cubic:
        print(args.cubic ** 3)

def test03():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--square", dest="lala", required=False, default=-1, help="display a square of a given number", type=int)
    parser.add_argument("-c", "--cubic", dest="haha", required=False, default=-1, help="display a cubic of a given number", type=int)

    args = parser.parse_args()
    if args.lala:
        print(args.lala)

    if args.haha:
        print(args.haha)

if __name__ == '__main__':
    test02()

