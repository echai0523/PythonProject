# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/9/5 12:21
input:
output:
Short Description:
    - 需求：
        - 5. 旋转一个字母意味着在字母表中移动它，如果有必要的话环绕到开头，所以旋转3个字母的“a”就是“D”，旋转1个字母的“Z”就是“a”。定义你自己的函数rotate_letter(letter, n)，它接受一个字母和一个整数n，并返回一个旋转n的新字母。你可能想要参考问题2中的ord和chr。在你的回答中，测试如下几个例子。没有特别的要求。
        - 6. 编写一个程序，找出圆周率的前一百万位数中所有连续的六位数(如123456、345678和789012)。从文本文件“pi_million_digits.txt”中读取。你的答案应该如下所示。要求:使用for循环生成所有可能的六位数连续组合，但不以012345678901234为基数开始。
Change History:
"""
# 5


def rotate_letter(letter, n):
    if (letter.isupper() or letter.islower()) and len(letter) == 1 and isinstance(n, int):
        if letter.isupper():
            if ord(letter) + n > ord('Z'):
                return chr(ord(letter) + n - ord('Z') - 1 + ord('A'))
            else:
                return chr(ord(letter) + n)
        else:
            if ord(letter) + n > ord('z'):
                return chr(ord(letter) + n - ord('z') - 1 + ord('a'))
            else:
                return chr(ord(letter) + n)
    else:
        return "WARNING: Your input is not valid."


print(rotate_letter('t', 3))
print(rotate_letter('Y', 5))
print(rotate_letter('abc', 5))
print(rotate_letter('?', 5))


# 6
six_digit = str()
in_million_digits = str()
for i in range(10):
    s = str()
    for j in range(6):
        next_num = i+j
        if next_num > 9:
            next_num = next_num - 10
        s += str(next_num)
    six_digit += s + '\t'

    with open('../EthanFileData/pi_million_digits.txt', 'r', encoding='utf-8') as readfile:
        pi_txt = readfile.read().replace('\n', '').replace('  ', '')
    if s in pi_txt:
        in_million_digits += s + '\t'

print('These are the possible six-digit consecutive combinations:\n', six_digit)
print('The following are in the first million digits of pi:\n', in_million_digits)

