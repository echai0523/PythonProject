# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/11/14 21:08
input   : 
output  :   
Short Description: 
Change History:
"""
import pandas as pd


def parse_multi(row):
    return row['a'] + 'a', row['b'] + 'b', row['c'] + 'c', row['d'] + 'd'
    # or
    # return [row['a'] + 'a', row['b'] + 'b', row['c'] + 'c', row['d'] + 'd']


df = pd.DataFrame()
# apply返回一个值
df['A'] = df['A'].apply(lambda x: x + 'A')
# apply返回多个值
# axis=1：按行传递，result_type="expand"：控制返回多行
df[['a', 'b', 'c', 'd']] = df.apply(parse_multi, axis=1, result_type="expand")
