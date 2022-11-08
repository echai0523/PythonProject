# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/11/8 17:40
input   : 
output  :   
Short Description:
    - 计数器（Counter）: dict的子类，计算可hash的对象
        - 主要功能: 可以支持方便、快速的计数，将元素数量统计，然后计数并返回一个字典，键为元素，值为元素个数。
        - 参考: https://blog.csdn.net/chl183/article/details/106956807
    - 双向队列（deque）: 类似于list的容器，可以快速的在队列头部和尾部添加、删除元素
    - 默认字典（defaultdict）: dict的子类，可以调用提供默认值的函数
    - 有序字典（OrderedDict）: dict的子类，可以记住元素的添加顺序
    - 可命名元组（namedtuple）: 可以创建包含名称的tuple
Change History:
"""
from collections import Counter, defaultdict


def collections_Counter():
    list1 = ["a", "a", "a", "b", "c", "c", "f", "g", "g", "g", "f"]
    dic = Counter(list1)
    print(dic)
    # 结果:次数是从高到低的
    # Counter({'a': 3, 'g': 3, 'c': 2, 'f': 2, 'b': 1})

    print(dict(dic))
    # 结果:按字母顺序排序的
    # {'a': 3, 'b': 1, 'c': 2, 'f': 2, 'g': 3}

    print(dic.items())  # dic.items()获取字典的key和value
    # 结果:按字母顺序排序的
    # dict_items([('a', 3), ('b', 1), ('c', 2), ('f', 2), ('g', 3)])

    print(dic.keys())
    # 结果:
    # dict_keys(['a', 'b', 'c', 'f', 'g'])

    print(dic.values())
    # 结果：
    # dict_values([3, 1, 2, 2, 3])

    print(sorted(dic.items(), key=lambda s: (-s[1])))
    # 结果:按统计次数降序排序
    # [('a', 3), ('g', 3), ('c', 2), ('f', 2), ('b', 1)]

    for i, v in dic.items():
        if v == 1:
            print(i)
    # 结果:
    # b

    str1 = "aabbfkrigbgsejaae"
    print(Counter(str1))
    print(dict(Counter(str1)))
    # 结果:
    # Counter({'a': 4, 'b': 3, 'g': 2, 'e': 2, 'f': 1, 'k': 1, 'r': 1, 'i': 1, 's': 1, 'j': 1})
    # {'a': 4, 'b': 3, 'f': 1, 'k': 1, 'r': 1, 'i': 1, 'g': 2, 's': 1, 'e': 2, 'j': 1}

    dic1 = {'a': 3, 'b': 4, 'c': 0, 'd': -2}
    print(Counter(dic1))


if __name__ == '__main__':
    collections_Counter()
    pass
