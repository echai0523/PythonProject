# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/24 16:36

input: 
output: 
Short Description: 
    - 知识点：
        - tolist()
            - 只有Series存在，DataFrame没有tolist
        - to_dict()
Change History:

"""
import pandas as pd


def main():
    # tolist:只有Series存在，DataFrame没有tolist
    sr = pd.Series([1, 2, 3])
    sr_lst = sr.tolist()
    print(type(sr), type(sr_lst))
    df2 = pd.DataFrame([
        [1, 2],
        [3, 4]
    ], columns=['a', 'b'])
    # print(df2.tolist())  # df没有tolist

    # to_dict
    df2 = pd.DataFrame([
        [1, 2],
        [3, 4]
    ], columns=['a', 'b'])
    print(df2)
    print(df2.to_dict())  # index 为key,值为series 转还后的 dict
    print(type(df2.to_dict()["a"]))  # dict
    print(df2.to_dict(orient="list"))
    print(df2.to_dict(orient="dict"))  # 默认行为
    print(df2.to_dict(orient="series"))
    print(df2.to_dict(orient="records"))  # 常用
    print(df2.to_dict(orient="index"))  # key是index


if __name__ == '__main__':
    main()
