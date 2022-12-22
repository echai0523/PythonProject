# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/12/22 09:50
input   : 
output  :   
Short Description:
    sys.exit()
        程序执行完后退出
    sys.stdin
        参考：https://blog.csdn.net/duiduihh123/article/details/123940124
        是一个标准化输入的方法。
        1. sys.stdin.readline()等价于input()
    sys.stdout
        用于print和状态表达式的结果输出，及input()的瞬时输出
        1. sys.stdout.write()等价于print()
        2. sys.stdout 重定向
    sys.stderr
        stderr与stdout一样，用于重定向错误信息至某个文件。
        1. sys.stderr 重定向
Change History:
"""
import sys
import os
import traceback


def stdin():
    """sys.stdin.readline()等价于input()"""
    nickname = input("enter your name: ")
    print("Hello", nickname)

    print("Enter your name: ")
    name = sys.stdin.readline()
    print("Hello ", name)


def stdout():
    """sys.stdout.write()等价于print()"""
    sys.stdout.write("hello world\n")
    print("hello world")

    """sys.stdout 重定向"""
    temp = sys.stdout
    print("hello temp!")  # 打印到终端
    
    # 之后使用print函数，都将内容打印到test.txt 文件中
    file = open("test.txt", "a")
    sys.stdout = file
    print("hello test.txt!")  # 打印到文件中
    
    # 恢复print函数打印到终端上
    sys.stdout = temp
    print("恢复 hello temp!")  # 打印到终端
    
    file.close()


def stderr():
    """sys.stderr 重定向"""
    file = open("test.txt", "a")
    sys.stderr = file
    # 使用traceback 函数定位错误信息
    try:
        1 / 0
    except:
        traceback.print_exc()

    print("print不需要sys.stderr直接写入到文件", file=file)

    file.close()

