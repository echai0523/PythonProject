# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/11/8 09:30
input   : 
output  :   
Short Description:
    - itertools.groupby(): 把可迭代对象中相邻的重复元素挑出来放一起
        for key, group in groupby("AABBCCAA"):
            - key: 重复元素
            - group: itertools._grouper类型的变量，也是个迭代对象
            - list(group): 将迭代对象转化为列表。
    - itertools.chain(): 用于拼接多个嵌套列表, 将元素串联后创建一个新的迭代器
    - itertools.chain.from_iterable(): 拼接单个嵌套列表, 将元素串联后创建一个新的迭代器
Change History:
"""
from itertools import groupby, chain


def itertools_groupby():
    for key, group in groupby("AABBCCAA"):
        # A <itertools._grouper object at 0x7fde1b3546d8> ['A', 'A']
        # B <itertools._grouper object at 0x7fde1b38e2b0> ['B', 'B']
        # C <itertools._grouper object at 0x7fde1b38ee80> ['C', 'C']
        # A <itertools._grouper object at 0x7fde1b3546d8> ['A', 'A']
        print(key, group, list(group))

    #
    for key, group in groupby('AaaBBbcCAAa', lambda c: c.upper()):
        # A <itertools._grouper object at 0x7ff576734cc0> ['A', 'a', 'a']
        # B <itertools._grouper object at 0x7ff576454240> ['B', 'B', 'b']
        # C <itertools._grouper object at 0x7ff57648ee80> ['c', 'C']
        # A <itertools._grouper object at 0x7ff5764546d8> ['A', 'A', 'a']
        print(key, group, list(group))

    """项目实例：按照每帧的instance进行归类"""
    frame = "obj"
    frame.frame_items.sort(key=lambda x: x.instance.id)  # 先排序在使用
    for group, items in groupby(frame.frame_items, key=lambda x: x.instance):
        print(group, items)


def itertools_chain():
    # merge = chain('abc', 'def')
    result = list(chain('abc', 'def'))  # ['a', 'b', 'c', 'd', 'e', 'f']
    print('itertools.chain result:', result)

    """把嵌套的列表合并成一个列表: chain_from.iterable"""
    a = [[1, 11], [2, 22], [3, 33], [4, 44], [5, 55]]
    # 方法1: sum()
    print('sum result:', sum(a, []))  # [1, 11, 2, 22, 3, 33, 4, 44, 5, 55]
    # 方法2: chain/chain.from_iterable拼接可迭代对象中的所有元素
    result = list(chain([1, 11], [2, 22], [3, 33], [4, 44], [5, 55]))  # [1, 11, 2, 22, 3, 33, 4, 44, 5, 55]
    print('itertools.chain result:', result)
    result = list(chain.from_iterable(a))  # [1, 11, 2, 22, 3, 33, 4, 44, 5, 55]
    print('itertools.chain.from_iterable result:', result)
    # 方法3: 迭代判断条件
    def flat(l):
        for k in l:
            if not isinstance(k, (list, tuple)):
                yield k
            else:
                yield from flat(k)

    a = [[1], [2], [3], [4], [5]]
    print('flat result:', list(flat(a)))


if __name__ == '__main__':
    # itertools_groupby()
    itertools_chain()

