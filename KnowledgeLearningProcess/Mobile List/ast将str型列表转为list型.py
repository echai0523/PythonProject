# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/16 15:39

input:
    - "[]"
output:
    - list
Short Description:
    - 知识点：
        - ast.literal_eval()
    - 需求：
        - 字符串类型的列表(eg: "['a','b']")转为列表(eg: ['a', 'b'])
Change History:

"""
import ast

type_str = "['1, 2', '1, 2']"
list_ = ast.literal_eval(type_str)
# <class 'list'> ['1, 2', '1, 2']
print(type(list_), list_)


type_list = ['1, 2', '1, 2']
result_list = list()
for i in type_list:
    a, b = i.split(', ')
    result_list.append((int(a), int(b)))
# <class 'list'> [(1, 2), (1, 2)]
print(type(result_list), result_list)
