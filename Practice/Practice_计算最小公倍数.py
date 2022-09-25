# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/9/25 22:02

input: 

output: 

Short Description: 
    - 计算最大公约数、最小公倍数
        - lowest_common_multiple()
Change History:
    
"""


def lowest_common_multiple():
    m = 2
    n = int(input("请输入一个正整数n: "))
    if m > n:
        m, n = n, m
    for i in range(m, 0, -1):
        if m % i == 0 and n % i == 0:
            print(f"{m} 和 {n} 的最大公约数是 {i}。")
            print(f"{m} 和 {n} 的最小公倍数为 {int(m * n / i)}。")
            break


if __name__ == '__main__':
    lowest_common_multiple()
