# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/9/17 17:29

input: 

output: 

Short Description: 
    - 知识点：
        - 任意一个条件符合
            - any
                - or
        - 所有条件都符合时
            - all
                - and
Change History:
    
"""


def any_use():
    # 任意一个条件符合，就会进入if语句中
    if 'a' in data or 'x' in data:
        print("or 成功进入if语句")
    if any(x in data for x in ("a", "b", "c", "e")):
        print("any 成功进入if语句")


def all_use():
    # 所有条件都符合时，才能进入if语句
    if 'a' in data and 'x' in data:
        print("and 成功进入if语句")
    if all(x in data for x in ("a", "b", "c", "e")):
        print("all 成功进入if语句")


def main():
    any_use()
    any_use()
    pass


if __name__ == '__main__':
    data = ["a", "b", "c", "d"]
    main()
