# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/23 11:22

input: 
output: 
Short Description: 
    - 知识点：
        - concat()
            - axis={'0':列向合并, '1':行向合并}
            - ignore_index={'True':id重新排序，'False':默认直接合并}
            - join={'inner':相同部分合并,'outer':默认不存在的使用NaN填充}
        - merge()
Change History:

"""
import pandas as pd
import numpy as np


def pandas_concat():
    # ignore_index
    df1 = pd.DataFrame(np.ones((3, 4)) * 0, columns=['a', 'b', 'c', 'd'])
    df2 = pd.DataFrame(np.ones((3, 4)) * 1, columns=['a', 'b', 'c', 'd'])
    df3 = pd.DataFrame(np.ones((3, 4)) * 2, columns=['a', 'b', 'c', 'd'])
    res = pd.concat([df1, df2, df3], axis=0, ignore_index=True)

    # join, ('inner', 'outer')
    df1 = pd.DataFrame(np.ones((3, 4)) * 0, columns=['a', 'b', 'c', 'd'], index=[1, 2, 3])
    df2 = pd.DataFrame(np.ones((3, 4)) * 1, columns=['b', 'c', 'd', 'e'], index=[2, 3, 4])
    res = pd.concat([df1, df2], axis=1, join='outer')
    res = pd.concat([df1, df2], axis=1, join='inner')

    # join_axes
    res = pd.concat([df1, df2], axis=1, join_axes=[df1.index])

    # append
    df1 = pd.DataFrame(np.ones((3, 4)) * 0, columns=['a', 'b', 'c', 'd'])
    df2 = pd.DataFrame(np.ones((3, 4)) * 1, columns=['a', 'b', 'c', 'd'])
    df2 = pd.DataFrame(np.ones((3, 4)) * 1, columns=['b', 'c', 'd', 'e'], index=[2, 3, 4])
    res = df1.append(df2, ignore_index=True)
    res = df1.append([df2, df3])

    s1 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
    res = df1.append(s1, ignore_index=True)

    print(res)


def pandas_merge():
    # merging two df by key/keys. (may be used in database)
    # simple example
    left = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                         'A': ['A0', 'A1', 'A2', 'A3'],
                         'B': ['B0', 'B1', 'B2', 'B3']})
    right = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                          'C': ['C0', 'C1', 'C2', 'C3'],
                          'D': ['D0', 'D1', 'D2', 'D3']})
    print(left)
    print(right)
    res = pd.merge(left, right, on='key')
    print(res)

    # consider two keys
    left = pd.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'],
                         'key2': ['K0', 'K1', 'K0', 'K1'],
                         'A': ['A0', 'A1', 'A2', 'A3'],
                         'B': ['B0', 'B1', 'B2', 'B3']})
    right = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                          'key2': ['K0', 'K0', 'K0', 'K0'],
                          'C': ['C0', 'C1', 'C2', 'C3'],
                          'D': ['D0', 'D1', 'D2', 'D3']})
    print(left)
    print(right)
    res = pd.merge(left, right, on=['key1', 'key2'], how='inner')  # default for how='inner'
    # how = ['left', 'right', 'outer', 'inner']
    res = pd.merge(left, right, on=['key1', 'key2'], how='left')
    print(res)

    # indicator
    df1 = pd.DataFrame({'col1': [0, 1], 'col_left': ['a', 'b']})
    df2 = pd.DataFrame({'col1': [1, 2, 2], 'col_right': [2, 2, 2]})
    print(df1)
    print(df2)
    res = pd.merge(df1, df2, on='col1', how='outer', indicator=True)
    # give the indicator a custom name
    res = pd.merge(df1, df2, on='col1', how='outer', indicator='indicator_column')

    # merged by index
    left = pd.DataFrame({'A': ['A0', 'A1', 'A2'],
                         'B': ['B0', 'B1', 'B2']},
                        index=['K0', 'K1', 'K2'])
    right = pd.DataFrame({'C': ['C0', 'C2', 'C3'],
                          'D': ['D0', 'D2', 'D3']},
                         index=['K0', 'K2', 'K3'])
    print(left)
    print(right)
    # left_index and right_index
    res = pd.merge(left, right, left_index=True, right_index=True, how='outer')
    res = pd.merge(left, right, left_index=True, right_index=True, how='inner')

    # handle overlapping
    boys = pd.DataFrame({'k': ['K0', 'K1', 'K2'], 'age': [1, 2, 3]})
    girls = pd.DataFrame({'k': ['K0', 'K0', 'K3'], 'age': [4, 5, 6]})
    res = pd.merge(boys, girls, on='k', suffixes=['_boy', '_girl'], how='inner')
    print(res)

    # join function in pandas is similar with merge. If know merge, you will understand join


def main():
    # 学习
    pandas_concat()
    pandas_merge()
    pass


if __name__ == '__main__':
    main()
