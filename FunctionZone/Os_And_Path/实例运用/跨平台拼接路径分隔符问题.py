# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/22 14:36

input: 
output: 
Short Description: 
    - 知识点：
        - os.sep 根据你所处的平台，自动采用相应的分隔符号。
    - 需求：
        - python是跨平台的。在Windows上，文件的路径分隔符是'\'，在mac上是'/'。为了让代码在不同的平台上都能运行，那么路径应该写'\'还是'/'呢？
Change History:

"""
import os


def main():
    sep = os.sep
    # 当前平台采用的分隔符号
    print(sep)
    # path_join = f'{sep}'.join(['a', 'b'])
    path_join = os.sep.join([r"C:\Users\echai\PycharmProjects\PythonProject\FunctionZone", "Os_And_Csv"])
    print(path_join)


if __name__ == '__main__':
    main()
