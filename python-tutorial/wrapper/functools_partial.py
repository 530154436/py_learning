# !/usr/bin/env python3
# -*- coding : utf-8 -*-
import functools

# ------------------------------------------------------------------------------------------
# ### 1. Partial Objects
# ```python
# functools.partial(func, /, *args, **keywords)
# ```
# 返回一个新的 部分对象，当被调用时其行为类似于 func 附带位置参数 args 和关键字参数 keywords 被调用。
# 如果为调用提供了更多的参数，它们会被附加到 args。 如果提供了额外的关键字参数，它们会扩展并重载 keywords。
# 大致等价于:
# ```python
# def partial(func, /, *args, **keywords):
#     def newfunc(*fargs, **fkeywords):
#         newkeywords = {**keywords, **fkeywords}
#         return func(*args, *fargs, **newkeywords)
#
#     newfunc.func = func
#     newfunc.args = args
#     newfunc.keywords = keywords
#     return newfunc
# ```
# partial() 会被“冻结了”一部分函数参数和/或关键字的部分函数应用所使用，从而得到一个具有简化签名的新对象。
# ------------------------------------------------------------------------------------------

def show_details(name, f, is_partial=False):
    info = f'{name}:\n    object:{f}\n'
    if is_partial:
        info += f'    func: {f.func}\n    args: {f.args}\n    keywords: {f.keywords}\n'
    else:
        info += f'    __name__: {f.__name__}\n'
    print(info)

# #### 1.1 example01 二进制转换
base_two = functools.partial(int, base=2)

show_details('base_two(): ', base_two, True)
print('    call base_two("1100") =', base_two('1100'))
print()

# #### 1.2 example02
def myfunc(a, b, c=2):
    print('    called myfunc with (a, b, c): (%s, %s, %s)' % (a, b, c))

# + **原始函数**
show_details('myfunc', myfunc)

# + **参数c指定默认值，参数a、b不指定**
f1 = functools.partial(myfunc, c=4)
show_details('f1()：partial with named default', f1, True)
f1('passing a', 'passing b')
f1('passing a', 'passing b', c=5)
print()

# + **参数a、c均指定默认值, 参数b不指定**
f2 = functools.partial(myfunc, 'default a', c=4)
show_details('f2()：partial with defaults', f2, True)
f2('passing b')
f2('passing b', c=5)
print()

# + **嵌套调用**
f3 = functools.partial(functools.partial(myfunc, 'default a'), 'default b')
show_details('f3()：partial with defaults', f3, True)
f3('passing c')


# TypeError: myfunc() got multiple values for argument 'c'
# f2('passing b', 'passing c')