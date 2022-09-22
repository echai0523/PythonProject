# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/9/15 20:30

input: 

output: 

Short Description: 
    - 逻辑：
        - 1. 计算机随机选择一个密码词库中的单词。
        - 2. 现在将每个单词用下划线“_”表示，给用户提供猜单词的机会，如果用户猜对了单词，则将“_”用单词替换。
        - 3. 关卡分为"简单"、"中等"、"困难"三种模式，分别对应猜词机会"9次"、"6次"、"3次"。
Change History:
    
"""
import random

# 输入玩家姓名
name = input("What is your name?")
print("Hello, " + name, "Time to play hangman!")
# 玩家选择模式
mode = input("Please select a mode, easy, medium or hard:").islower()
print("Start guessing...\n")
# 密码词库
words = ['python', 'programming', 'treasure', 'creative', 'medium', 'horror', 'hard', 'project', 'easy', 'man', 'women']
# CPU出词
word = random.choice(words)

# 猜对的初始值及剩余猜测次数
guesses = ''
if mode == 'easy':
    turns = 9
elif mode == 'medium':
    turns = 6
else:
    turns = 3
# 游戏开始
while turns > 0:
    # 首次进入，生成长度为单词长度的'_'，当玩家输入猜测的单词后，与CPU所出词进行一一匹对，符合的用字母代替_
    failed = 0
    for char in word:
        if char in guesses:
            print(char, end="")
        else:
            print("_", end=""),
            failed += 1
    # 首次进入，经过上面逻辑后，failed==len(word)，当玩家输入猜测的单词后，failed==failed-猜中的字母，当全部猜中或次数用完后退出死循环
    if failed == 0:
        print("\nYou won")
        break
    # 玩家输入猜测的单词
    guess = input("\nguess a character:")
    guesses += guess
    # 判断玩家猜测的单词是否与CPU所出词一致
    if guess not in word:
        # 机会次数-1， 并提示剩余次数， 若次数 == 0，玩家猜测失败，退出游戏
        turns -= 1
        print("\nWrong")
        print("\nYou have", + turns, 'more guesses')
        if turns == 0:
            print("\nYou Lose")
