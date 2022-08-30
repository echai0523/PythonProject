# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/22 15:17

input:
    - dict
output:

Short Description: 
    - 知识点：
        - 如何定义dict
Change History:

"""


def operation_dict():
    """以下均可定义结果  {"name": 'Tom', "age": 18}"""
    dic = dict(name='Tom', age=18)
    dic = dict([("name", "Tom"), ("age", 18)])
    dic = dict(zip(["name", "age"], ["Tom", 18]))
    """访问字典"""
    dic_value = dic.get("height", 180)  # 若不存在key，则输出默认值180
    """添加"""
    dic.setdefault("height", 180)  # 插入一个key，设置默认值为180
    dic.update({"home": "China"})  # 插入一个键值对
    """删除"""
    dic.pop("name")  # 删除键值对，指定key，并弹出value
    del dic["home"]  # 删除键值对，指定key
    dic.popitem()  # 随机删除一项
    """拷贝"""
    dic2 = dic.copy()  # 深拷贝，dic的变化不影响dic2
    """操作"""
    dic = {'a': 100, 'b': 2, 'c': 3}
    print(dic)
    print(max(dic))     # c 最大的key，注意是key而不是value，与value无关
    print(min(dic))     # a 最小的key，注意是key而不是value，与value无关
    print(len(dic))     # 3 键值对的个数
    print(str(dic))     # "{'a': 10, 'b': 5, 'c': 20}"
    print(any(dic))     # True(只要一个键为True)，注意是key而不是value，与value无关
    print(all(dic))     # True(所以键都为True)，注意是key而不是value，与value无关
    print(sorted(dic))  # 对键排序


operation_dict()






