import numpy as np

'''
    Numpy 的属性
'''
array = np.array([[1,2,3],
                  [2,3,4]])
print(array)

# ndim：维度
print('numbers of dim:', array.ndim)

# shape：行数和列数
print('shape:',array.shape)

# size：元素个数
print('size:',array.size)