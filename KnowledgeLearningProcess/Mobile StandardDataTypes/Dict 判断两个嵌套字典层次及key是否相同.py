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


def read_json():
    import json
    from peutils.fileutil import list_current_file
    # path1 = list_current_file(path='', type='file', suffix='.json')
    # path2 = list_current_file(path='', type='file', suffix='.json')
    for i in range(84, 95):
        p1 = f""
        p2 = f""

        with open(p1, 'r', encoding='utf-8') as f1:
            json1 = json.load(f1)
        with open(p2, 'r', encoding='utf-8') as f2:
            json2 = json.load(f2)

        result = [i for i in diff(json1, json2)]
        print(i, result)


if __name__ == '__main__':
    # main()
    read_json()