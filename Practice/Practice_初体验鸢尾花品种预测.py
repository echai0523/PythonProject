# -*- coding: UTF-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
# pip3 install scikit-learn(如果不是notebook上就去掉！)
from sklearn import model_selection  # 将数据打乱并分成两部分: 训练、测试
from sklearn.svm import SVC  # 支持向量机模型

# 1，首先学会利用pandas对数据进行读取操作，将iris.csv数据读取，每一行前面四列数据存储在变量X中，最后一列存入变量y中
# 使用pandas.read_csv(路径)方法，读取iris.csv
iris_df = pd.read_csv("../EthanFileData/File xlsx csv/iris.csv")
# print(type(iris_df))  # 类型DataFrame

X = []  # 构建变量X为空列表存前面四列数据
Y = []  # 构建变量Y为空列表存最后一列数据
# 使用DataFrame.iterrows()方法遍历所有行，index为该行的索引值，row为该行的数据
for row_index, row in iris_df.iterrows():
    # 使用list.append()方法 把第row_index行的前4列及名为0 1 2 3的列 存入列表X
    X.append([row['0'], row['1'], row['2'], row['3']])
    # 使用list.append()方法 把第row_index行的最后一列及名为y的列 存入列表Y
    Y.append(row['y'])
# print(X)  # X=[ [x1,x2,x3,x4], [...] , [...],....[..]]-数据X形式
# print(Y)  # Y=[y1,y2,,,,,yn]-数据y

# 2，查看数据分布，利用matplotlib作图。选取X前两列x1,x2和对应的数据y,使用plt.scatter做散点图,注意根据y不同点的颜色不同，例如y的值为0,那么这个点表示品种1,则在图中用红色表示，以此类推
# plt.scatter做散点图，参考：https://zhuanlan.zhihu.com/p/111331057

# X是四列的值，需要修改，使用列表推导式，循环遍历X获取每4列值，利用索引分别取前两列的值。
X1 = [x[0] for x in X]
X2 = [x[1] for x in X]
# 先构建颜色映射，所有y==0的均为red, y==1的均为green, y==2的均为yellow
map_color = {0: 'r', 1: 'g', 2: 'y'}
color = list(map(lambda x: map_color[x], Y))
# 绘制scatter散点图，x轴为X1、X2，y轴均为Y， 颜色根据y的值
plt.scatter(x=X1, y=Y, c=color)
plt.scatter(x=X2, y=Y, c=color)
# plt.show()，展示散点图
plt.show()


# 4，一次的实验可能会存在偶然性，重复10次步骤3,记录结果的平均值（重复操作for循环）
for _ in range(10):
    # 3，将x，y转化成numpy
    # 将数据打乱并分成两部分，一部分用来训练模型，另一部分用作做测试，其中训练和测试数据占比8：2
    # 训练集的特征值x_train 测试集的特征值x_test 训练集的目标值y_train 测试集的目标值y_test
    x_train, x_test, y_train, y_test = model_selection.train_test_split(X, Y, test_size=0.2)
    # print("x_train:", x_train, "\nx_test:", x_test, "\ny_train:", y_train, "\ny_test:", y_test)

    # 向量机模型
    model = SVC()
    model.fit(x_train, y_train)  # 训练模型
    score = model.score(x_test, y_test)  # 预测准确度
    print(score * 100)  # 最终的数值表明我们预测的准确度，例如输出90，表明有90%的数据预测对了，也可以说模型准确率90%


# 4，一次的实验可能会存在偶然性，重复10次步骤3,记录结果的平均值（重复操作for循环）
# 96.66666666666667
# 96.66666666666667
# 96.66666666666667
# 100.0
# 100.0
# 96.66666666666667
# 100.0
# 93.33333333333333
# 83.33333333333334
# 96.66666666666667

