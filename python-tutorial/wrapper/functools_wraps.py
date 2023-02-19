# !/usr/bin/env python3
# -*- coding : utf-8 -*-
import time
import traceback
import functools

# -------------------------------------------------------------------------------------------------
# ### 2. update_wrapper
# ```python
# functools.update_wrapper(wrapper, wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)
# ```
# -------------------------------------------------------------------------------------------------
def myfunc(a, b=2):
    "Docstring for myfunc()"
    print('     called myfunc with:', (a, b))

def show_details(name, f):
    info = f'{name}:\n    object:{f}\n'
    try:
        info += f'     __name__: {f.__name__}\n'
    except AttributeError:
        info += f'     no __name__\n'
    info += f'     __doc__: {f.__doc__}\n'
    print(info)

# myfunc
show_details('myfunc', myfunc)

# raw_wrapper
f1 = functools.partial(myfunc, b=4)
show_details('raw wrapper', f1)

# update_wrapper
functools.update_wrapper(f1, myfunc)
show_details('updated wrapper', f1)
print()

# -------------------------------------------------------------------------------------------------
# #### 2.3 wraps
# ```python
# functools.wraps(wrapped, assigned = WRAPPER_ASSIGNMENTS, updated = WRAPPER_UPDATES)
# ```
# -------------------------------------------------------------------------------------------------

# ##### 2.3.1 无参装饰器之计时器(Timer)
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print('load wrapper')
        print(f'执行函数 {func.__name__}，共耗时 {time.time()-start} 秒')

    print('load timer')
    return wrapper

@timer
def decorated_func1():
    time.sleep(2)

# 等价于
# wrapper = functools.wraps(decorated_func1)(wrapper)
# decorated_func1 = timer(decorated_func1)

# ##### 2.3.2 有参装饰器之重试机制(Retry)
def retry(max_retry=2):
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs): # 接收任意参数的修饰器

            attempt = 0
            while attempt <= max_retry:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    if attempt>0:
                        print(f'重试 {attempt}/{max_retry}: {func.__name__}()')
                    attempt += 1
            print('load wrapper')
        print('load decorator')
        return wrapper

    print('load retry')
    return decorator

@retry(max_retry=2)
def decorated_func2(*args):
    print(args)
    a = 1/0
    # a = 1 + 1

# 等价于
# wrapper = functools.wraps(decorated_func2)(wrapper)
# decorated_func2 = retry(max_retry)(decorated_func2)

if __name__ == '__main__':
    print('run main')
    decorated_func1()
    decorated_func2(1,2,3)