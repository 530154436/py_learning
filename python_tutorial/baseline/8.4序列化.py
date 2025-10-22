#!/usr/bin/env python3
# -*- utf-8 -*-
'''
序列化
'''
import pickle

d = dict(name='bob', age=10, score=100)

# dumps()方法把任意对象序列化成一个bytes
dumps_s = pickle.dumps(d)
print(type(dumps_s), dumps_s)

# bytes写入文件
f = open('dump.txt', 'wb')
pickle.dump(d, f)
f.close()

# 读取bytes文件
f = open('dump.txt', 'rb')
d = pickle.load(f)
print(type(d), d)

'''
Json

JSON类型      Python类型
{}	            dict
[]	            list
"string"        str
1234.56	        int或float
true/false	    True/False
null	        None
'''
import json

# Python对象转换为JSON对象(字符串) --Serialize ``obj`` to a JSON formatted ``str``
json_str = json.dumps(d)
print(type(json_str), json_str)

# JSON对象(字符串)转换为Python对象 -Deserialize
# ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance containing a JSON document) to a Python object.
json_str = '{"age": 20, "score": 88, "name": "Bob"}'
j = json.loads(json_str)
print(type(j), j)

# python json.dumps() json.dump()的区别
# dump需要一个类似于文件指针的参数（并不是真的指针，可称之为类文件对象），可以与文件操作结合，也就是说可以将dict转成str然后存入文件中；
# dumps直接给的是str，也就是将字典转成str。

class Student(object):

    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

s = Student('Bob', 11, 90)

def std2Json(student):
    return {
        'name':student.name,
        'age':student.age,
        'score':student.score
    }

# Student实例首先被std2Json()函数转换成dict，然后再被顺利序列化为JSON
print(json.dumps(std2Json(s)))

# 把任意class的实例变为dict
d = json.dumps(s, default=lambda obj : s.__dict__)
print(type(d), d)


# 把JSON反序列化为一个Student对象实例，loads()方法首先转换出一个dict对象，
# 然后，我们传入的object_hook函数负责把dict转换为Student实例

def dict2Student(student_dict):
    return Student(student_dict['name'], student_dict['age'], student_dict['score'])

json_str = '{"age": 20, "score": 88, "name": "Bob"}'

s = json.loads(json_str, object_hook=dict2Student)
print(type(s))








