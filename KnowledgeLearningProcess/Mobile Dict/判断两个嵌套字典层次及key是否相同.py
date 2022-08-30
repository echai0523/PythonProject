# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/18 21:04

input:
    - 嵌套字典a
    - 嵌套字典b
output:
    - [] 相同
    - change 修改
    - remove a要删除**才和b相同
    - add a要添加**才和b相同
Short Description: 

Change History:

"""
from dictdiffer import diff


def main():
    a = {"a": {"b": 1, "bb": 2}, "aa": 2}
    b = {"a": {"b": 1, "bb": 2}, "aa": 2, 'aaa': 3}

    result = [i for i in diff(a, b)]
    print(result)


if __name__ == '__main__':
    main()
