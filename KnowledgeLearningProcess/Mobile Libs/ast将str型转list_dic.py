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
        - 字符串类型的字典(eg: "{'a': {'b': 1}}")转为字典(eg: {'a': {'b': 1}})

Change History:

"""
from ast import literal_eval
from pprint import pprint


def str_to_list():
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


def str_to_dict():
    default = "{'行走或站立的人': {'height': 2.5, 'length': 2, 'width': 2.0},'坐或弯腰或蹲下的人': {'height': 1.8, 'length': 1.5, 'width': 1.5},'躺着的人': {'height': 1.0, 'length': 2, 'width': 1.5},'摩托车和人': {'height': 2.0, 'length': 3, 'width': 2.0},'自行车和人': {'height': 2.0, 'length': 3, 'width': 2.0},'非箱式三轮车和人': {'height': 4.0, 'length': 4, 'width': 3.0},'手推车和人': {'height': 4.0, 'length': 3, 'width': 3.0},'摩托车': {'height': 2.0, 'length': 2.5, 'width': 1.5},'自行车': {'height': 2.0, 'length': 2.5, 'width': 1.5},'非箱式三轮车': {'height': 2.0, 'length': 4, 'width': 3.0},'手推车': {'height': 2.0, 'length': 3, 'width': 3.0},'微型车': {'height': 3.0, 'length': 4.5, 'width': 3.0},'轿车': {'height': 3.0, 'length': 6.5, 'width': 3.0},'越野车': {'height': 3.0, 'length': 6.5, 'width': 3.0},'面包车': {'height': 3.0, 'length': 7, 'width': 3.0},'巴士': {'height': 5.0, 'length': 15, 'width': 6.0},'软连接巴士': {'height': 5.0, 'length': 15, 'width': 6.0},'小货车': {'height': 4.0, 'length': 10, 'width': 5.0},'卡车': {'height': 7.0, 'length': 20, 'width': 6.0},'卡车头': {'height': 7.0, 'length': 10, 'width': 6.0},'拖挂': {'height': 8.0, 'length': 20, 'width': 6.0},'专业作业车': {'height': 7.0, 'length': 20, 'width': 6.0},'锥筒': {'height': 2.0, 'length': 1.5, 'width': 1.5},'警示立牌': {'height': 3.0, 'length': 3, 'width': 3.0},'防撞柱': {'height': 2.0, 'length': 2, 'width': 2.0},'水马': {'height': 3.0, 'length': 5, 'width': 3.0},'杂物': {'height': 10.0, 'length': 10, 'width': 10.0}}"
    dic = literal_eval(default)
    print(type(dic), type(dic['行走或站立的人']['height']))
    pprint(dic)
