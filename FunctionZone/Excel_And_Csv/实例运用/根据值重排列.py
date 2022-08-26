# -*- coding: UTF-8 -*-

import pandas as pd

# 读取excel 无列名的数据(默认0开始排序)
df = pd.read_excel("../../../EthanFileData/exercise.xlsx", header=None)
print(df)

# 排序规则514230
header_sort_list = []  # 以此来进行排序
for i in list('514230'):
    # 按列遍历，h为头部(要放到header_sort_list中)，row为每一列的数据(类型是series)
    for h, row in df.iteritems():
        # 每列第一行 == 5 1 4 2 3 0 时，将头部写入到header_sort_list
        if row[0] == int(i):
            header_sort_list.append(h)

# 根据header_sort_list中顺序进行列排序
df = df[header_sort_list]
# 写入 无列名 无索引 的excel
df.to_excel("exercise_result.xlsx", header=None, index=False)
print(df)

