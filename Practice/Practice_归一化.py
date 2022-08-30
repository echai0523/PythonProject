# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/26 10:16

input: 

output: 

Short Description: 

Change History:
    
"""
import pandas as pd
import numpy as np


def main():
    # 将坐标转为DataFrame
    body_df = pd.DataFrame([upleft["x"], upleft["y"], lowright["x"], lowright["y"]])
    # 归一化运算的两种方法:
    # 1
    body_normalization = (body_df - body_df.min()) / (body_df.max() - body_df.min())
    # 2
    body_normalization = body_df.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))

    # 将归一化值(type-DataFrame)转为list
    body_box = np.array(body_normalization.stack()).tolist()


if __name__ == '__main__':
    main()
