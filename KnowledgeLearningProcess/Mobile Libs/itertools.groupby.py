# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/11/8 09:30
input   : 
output  :   
Short Description:
    - groupby()的作用就是把可迭代对象中相邻的重复元素挑出来放一起
        for key, group in groupby("AABBCCAA"):
            - key: 重复元素
            - group: itertools._grouper类型的变量，也是个迭代对象
            - list(group): 将迭代对象转化为列表。
Change History:
"""
from itertools import groupby


def practice():
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


def project_instance():
    # 按照每帧的instance进行归类
    frame.frame_items.sort(key=lambda x: x.instance.id)  # 先排序在使用
    for group, items in groupby(frame.frame_items, key=lambda x: x.instance):
        print(group, items)


if __name__ == '__main__':
    practice()
    project_instance()
