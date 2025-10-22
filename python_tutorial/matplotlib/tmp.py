# !/usr/bin/env python3
# -*- coding : utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
x = [1,2,3,4]
y1 = np.sin(x)
y2 = np.cos(x)
plt.plot(x, y1, color='orange')
plt.plot(x, y2, color='red')
# plt.show()

y0 = [np.array([1])]
y_0 = [ int(i) for i in y0]
print(y0, type(y0))
print(y_0, type(y_0))