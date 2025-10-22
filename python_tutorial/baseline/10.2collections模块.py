# /usr/bin/env python3
# -*- coding:utf-8 -*-
from collections import namedtuple, deque, defaultdict, OrderedDict,Counter

def test_named_tuple():
    '''
    namedtuple是一个函数，它用来创建一个自定义的tuple对象，
    并且规定了tuple元素的个数，并可以用属性而不是索引来引用tuple的某个元素。
    :return:
    '''
    Point = namedtuple('Point', ['x', 'y'])

    point = Point(1, 2)
    print(point)
    print(isinstance(point, tuple))
    print(isinstance(point, Point))
    print(point.x)
    print(point.y)

def test_deque():
    '''
    高效实现插入和删除操作的双向列表
    :return:
    '''
    q = deque(['a','b','c','d'])
    q.append('e')
    q.popleft()
    print(q)
    q.appendleft('a')
    print(q)

def test_default_dict():
    '''
    使用dict时，如果引用的Key不存在，就会抛出KeyError。
    如果希望key不存在时，返回一个默认值，就可以用defaultdict
    :return:
    '''
    dd = defaultdict(lambda : 'N/A')
    dd ['key'] = 'value'
    print(dd['key'])
    print(dd['ada'])

def test_ordered_dict():
    '''
    使用dict时，Key是无序的。在对dict做迭代时，我们无法确定Key的顺序。
    如果要保持Key的顺序，可以用OrderedDict
    :return:
    '''
    d = dict([('a',1),('b',2),('c',3)])
    print(d)

    # OrderedDict的Key会按照插入的顺序排列，不是Key本身排序
    dd = OrderedDict(d)
    print(dd)

    od = OrderedDict()
    od['z'] = 1
    od['y'] = 2
    od['x'] = 3
    print(od)

def test_counter():
    '''
    Counter是一个简单的计数器
    '''
    c = Counter()
    for ch in 'programming':
        c[ch] = c[ch]+1
    print(c)


if __name__ == '__main__':
    # test_named_tuple()
    # test_deque()
    # test_deque()
    # test_default_dict()
    # test_rdered_dict()
    test_counter()






