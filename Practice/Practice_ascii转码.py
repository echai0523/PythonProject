# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/25 17:05

input: 
output: 

Short Description:
    - 知识点：
        - ASCII码: 先ord转十进制 再chr转回来
            - 0~9 48~57
            - A~Z 65~90
            - a~z 97~122

Change History:

"""


def use_ascii():
    shi = ord("a")
    shi = ord("9")
    print(shi)
    asc = chr(shi)
    print(asc)


def main():
    use_ascii()
    pass


if __name__ == '__main__':
    main()
