# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/23 10:56

input: 
output: 
Short Description:
    - 知识点：
        - dropna() dropna存在缺失值则丢弃该行/列。
            - axis={'0':丢掉整列, '1':丢掉整行}
            - how={'any':存在缺失值, 'all':整行/列都是缺失值}
        - fillna() 填写缺失的值
        - isnull() 缺失值用True代替，其他值用False代替
            - np.any() 找到缺失值
Change History:

"""
import pandas as pd
import numpy as np


def parse_nan():
    """处理丢失数据"""
    datas = pd.date_range('20210101', periods=6)
    df = pd.DataFarme(np.arange(24).reshape((6, 4)), index=datas, columns=['A', 'B', 'C', 'D'])

    # 缺失值位置填充NaN
    df.iloc[0, 1] = np.nan
    df.iloc[1, 2] = np.nan

    # dropna
    print(df.dropna(axis=0, how='any'))

    # fillna
    print(df.fillna(value=0))

    # isnull
    print(df.isnull())  # True
    # np.any() 找到缺失值
    print(np.any(df.isnull()) == True)


def main():
    # 学习
    parse_nan()


if __name__ == '__main__':
    main()
