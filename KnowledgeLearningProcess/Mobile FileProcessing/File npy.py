# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/10/25 20:43
input   : 
output  :   
Short Description: 
Change History:
"""
import numpy as np

columns_path = "../../EthanFileData/npy/columns.npy"
values_path = "../../EthanFileData/npy/values.npy"

# 注意编码方式
pre_train_columns = np.load(columns_path, allow_pickle=True, encoding="latin1")
pre_train_values = np.load(values_path, allow_pickle=True, encoding="latin1")

print(pre_train_columns)
print(pre_train_values)
