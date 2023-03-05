[TOC]
深圳市三态电子商务股份有限公司
interview.py 精确度(baseline)： 0.74008


| 模型 | 准确率(%) | AUC |
|:-----:|:-----:|:-----:|
| LR | 0.74216 | 0.597894512054918 |
|LR + OneHot | 0.8008 | 0.035 |
| | 0.8203 | 0.158 |
| | 0.8196 | 1.107 |
> 采用交叉验证，cv=5


export CXX=g++-8 CC=gcc-8
python -m pip install lightgbm -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com