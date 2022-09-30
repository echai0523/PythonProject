# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/22 14:17

input: 
output: 
Short Description: 

Change History:

"""
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
import warnings  # 警告, 参考：https://blog.konghy.cn/2017/12/16/python-warnings/

warnings.filterwarnings('ignore')  # filterwarnings()将规则添加到过滤器  "ignore" 忽略匹配的警告

# 读入数据集
data = pd.read_csv(r'../EthanFileData/txt/iris.txt', header=None, names=['x1', 'x2', 'x3', 'x4', 'y'])
x = data.iloc[:, :-1]
y = data.iloc[:, -1:]
# print(y)
x = StandardScaler().fit_transform(x)  # 数据标准化 [[-9.00681170e-01  1.03205722e+00 -1.34127240e+00 -1.31297673e+00]]
# print(x)

# 使用LabelEncoder对数据集进行编码
lable = LabelEncoder()
y = lable.fit_transform(y)  # 训练LabelEncoder并对原数据进行编码
# print(y)
# y = lable.inverse_transform(y)  # 根据编码后的类别，反向推导出编码前对应的原始标签
# print(y)

# 留出法对数据进行分类操作
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=666, test_size=0.3)  # 分割训练集和测试集
lr = LogisticRegression()  # 多分类处理效果
# 网格搜索交叉验证，对数据进行处理操作  # 参考：https://www.cnblogs.com/dalege/p/14175192.html
model = GridSearchCV(lr, param_grid={'C': [1, 10, 20, 50]})
model.fit(x_train, y_train)
# print(model.score(x_test, y_test))  # 模型得分，准确率
# print(model.best_params_)  # 最优参数

y_ = model.predict(x_test)
print(accuracy_score(y_test, y_))  # 准确率

# help(LogisticRegression)

