# !/usr/bin/env python3
# -*- coding : utf-8 -*-
import os

# 操作系统类型
print(os.name)

# 详细的系统信息
print(os.uname())

'''
环境变量
'''

# 查看操作系统中定义的环境变量
print(os.environ)

# 查看操作系统中定义的环境变量的值
print(os.environ.get('PATH'))
print(os.environ.get('x', 'default'))

'''
操作目录
'''

# 查看当前目录的绝对路径
print(os.path.abspath('.'))

# 在某个目录下创建一个新目录,首先把新目录的完整路径表示出来
new_path = os.path.join('/Users/zhengchubin/PycharmProjects/learn/python-tutorial','test_dir')
print(new_path)

# 创建一个目录
if not os.path.exists(new_path):
    os.mkdir(new_path)
    print('crate a dir: %s' % new_path)

# 删除一个目录
# os.rmdir(new_path)

# 拆分路径
splits = os.path.split(new_path)
print(splits)

'''
操作文件
'''

# 获得文件扩展名
new_file = os.path.join(new_path,'file.txt')
split_extend = os.path.splitext(new_file)
print(split_extend)

# 文件重命名
os.rename('file.py', 'test.txt')

# 删除文件
os.remove('test.txt')

'''
批量处理目录和文件
'''

# 列出当前目录下的所有目录
print([x for x in os.listdir('.') if os.path.isdir(x)])

# 列出所有的.py文件
print([x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.py'])

'''
练习 编写一个程序，能在当前目录以及当前目录的所有子目录下查找文件名包含指定字符串的文件，并打印出相对路径。
'''

def get_files(parent, files, search):
    paths = os.listdir(parent)
    for path in paths:
        if os.path.isdir(path):
            get_files(path, files, search)
        if os.path.isfile(path) and search in path:
            files.append(path)

files=[]
get_files('.', files, '函数')
for file in files:
    print(file)















