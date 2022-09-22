# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/23 10:23

input:

output:

Short Description: 
    - 知识点：
        - pandas数据结构
            - Series 一维数组
            - Time-Series 时间为索引的Series
            - DataFrame 二维的表格型数据结构
            - Panel 三维的数组，可以理解为DataFrame的容器

Change History:

"""
import pandas as pd
import numpy as np


def series_use():
    """Series的使用"""
    # Series 就如同列表一样，一系列数据，每个数据对应一个索引值。Series 就是“竖起来”的 list。
    s = pd.Series([1, 4, 'ww', 'tt'])
    print(s)
    # 显示 Series 对象的索引和数据值
    print(s.index)
    print(s.values)

    # 自定义索引
    s2 = pd.Series(['wangxing', 'man', 24], index=['name', 'sex', 'age'])
    print(s2)
    # 查看值与修改值
    print(s2["name"])
    s2["name"] = 'wudadiao'
    print(s2)

    # 字典式定义Series对象
    sd = {'python': 9000, 'c++': 9001, 'c#': 9000}
    s3 = pd.Series(sd)
    print(s3)
    s4 = pd.Series(sd, index=['java', 'c++', 'c#'])
    print(s4)  # 如果没有值，都对其赋给 NaN。
    print(pd.isnull(s4))  # 判断值是否为空
    print(s4.isnull())
    # 索引重新定义
    s4.index = ['语文', '数学', 'English']
    print(s4)
    # series运算
    print(s4 * 2)


def dataframe_use():
    # DataFrame对象的常用方法——使用 dict 定义
    data = {"name": ['google', 'baidu', 'yahoo'], "marks": [100, 200, 300], "price": [1, 2, 3]}
    df = pd.DataFrame(data)
    print(df)
    # 设置columns顺序
    df = pd.DataFrame(data, columns=['name', 'price', 'marks'])
    print(df)
    # 自定义数据索引，单行数据需要index=[0]
    df = pd.DataFrame(data, columns=['name', 'marks', 'price'], index=['a', 'b', 'c'])
    print(df)

    # DataFrame对象——使用 字典套字典 定义
    newdata = {'lang': {'first': 'python', 'second': 'java'}, 'price': {'first': 5000, 'second': 2000}}
    df1 = pd.DataFrame(newdata)
    print(df1)
    # 在字典中规定好了每个数据格子中的数据，没有规定的都是空。
    newdata = {"lang": {"firstline": "python", "secondline": "java"}, "price": {"firstline": 8000}}
    df1 = pd.DataFrame(newdata)
    print(df1)
    df1 = pd.DataFrame(newdata, index=["firstline", "secondline", "thirdline"])
    print(df1)


def main():
    # 学习
    series_use()
    dataframe_use()
    pass


if __name__ == '__main__':
    main()
