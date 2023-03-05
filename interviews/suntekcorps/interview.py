
import numpy as np
import matplotlib.pyplot as mp
import sklearn.linear_model as lm
import sklearn.model_selection as ms
from sklearn import metrics

data_training = np.loadtxt('case2_training.csv', delimiter=',',skiprows=1)
x = data_training[:, 1:-1]
y = data_training[:, -1]

train_x, test_x, train_y, test_y = \
    ms.train_test_split(x, y, test_size=0.25, random_state=7)

data_testing = np.loadtxt('case2_testing.csv', delimiter=',',skiprows=1)
pred_x = data_testing[:, 1:]

# 根据当前样本，训练逻辑回归模型  C: 惩罚系数  为了防止过拟合

model = lm.LogisticRegression(C=2)
model.fit(train_x, train_y)

pred_test_y = model.predict(test_x)

print('精确度：',(pred_test_y == test_y).sum() / test_y.size)  # 精准度
pred_y_prob = model.predict_proba(pred_x)

fpr, tpr, thresholds = metrics.roc_curve(test_y, pred_test_y)
print(f'auc：{metrics.auc(fpr, tpr)}')# 精准度
