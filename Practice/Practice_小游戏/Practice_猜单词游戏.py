# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/9/15 20:30

input: 

output: 

Short Description:
    - Hangman Game逻辑：
        - 1. 计算机从一个文本中随机抽取一个单词，字符串表示，并显示出字符串长度
        - 2. 用户一个字符一个字符去猜，手动输入猜测结果，总共有6次猜测次数，每次猜测完之后，计算机告知玩家已经猜测的结果和剩余可以猜测的字母范围
        玩家猜测过程是有一定的规则的：
            - 1. 不能猜测已经猜测过的字符，每重复猜测一次，计算机发出警告一次，总共有3次警告机会；不能猜测除了大小写字母之外的字符，如‘#’ 等一些特殊字符，每猜测一次，警告次数减 1；当警告次数没有了，玩家如果继续犯规（猜测重复，或者猜测除大小写字母之外的字符）则猜测次数减去 1；
            - 2. 玩家猜测的字母不在目标串 secret_letters中，如果猜测的字母是元音字母，则猜测次数减 2 作为惩罚，如果是辅音字母，则猜测次数减 1
            - 3. 这样猜对于玩家来说实在太有难度了，是否可以实现一个游戏的改进版本，每当玩家输入星号 * 时，计算机自动输出文本中所有与当前玩家已猜测结果相符合的单词呢？这样就可以大大缩小玩家的猜测范围了，降低游戏难度。

Change History:
    
"""
import random
import string

#
# def load_words():  # 读取文件
#     print("Loading word list from file...")
#     # inFile: file
#     inFile = open("words.txt", 'r')
#     # line: string
#     line = inFile.readline()
#     # wordlist: list of strings
#     wordlist = line.split()  # 空格分开的单词
#     print("  ", len(wordlist), "words loaded.")
#     return wordlist  # 返回的是一个列表
#
#
# wordlist = load_words()
wordlist = ['python', 'programming', 'treasure', 'creative', 'medium', 'horror']


def choose_word(wordlist):
    return random.choice(wordlist)  # 随机获取一个单词


# 判断玩家猜测是否正确
def is_word_guessed(secret_word, letters_guessed):
    list_secret = list(secret_word)
    # 只要目标中出现一个字母不在玩家猜测结果中，返回False,都在的话，返回True
    for i in list_secret:
        if i not in letters_guessed:
            return False
    return True


# 获取玩家已猜对字母
def get_guessed_word(secret_word, letters_guessed):
    length = len(secret_word)
    list_secret = ['_ '] * length  # 列表元素先全部初始化为'_'
    for i in letters_guessed:
        for j in range(length):
            if i == secret_word[j]:  # 用猜对的字母替换掉对应位置的'_'
                list_secret[j] = secret_word[j]

    string = "".join(map(lambda x: str(x), list_secret))  # 列表转字符串
    return string


# 获取剩余可猜测字母范围
def get_available_letters(letters_guessed):
    # 初始化可猜字母为全部小写字母
    letters_all = "abcdefghijklmnopqrstuvwxyz"
    for i in letters_all:
        if i in letters_guessed:  # 如果玩家已经猜过 i 则将其替换为'_ '
            letters_all = letters_all.replace(i, '')
    return letters_all


def hangman(secret_word):
    list_unique = []  # 用于secret_word去重
    for i in secret_word:
        if i not in list_unique:
            list_unique.append(i)
    unique_numbers = len(list_unique)  # 目标单词中不同字符的数量，用于计算玩家分数
    vowels = "aeiou"  # 元音字母
    print("Welcome to the game hangman!")
    length = len(secret_word)  # 目标单词长度
    print("I'm thinking of a word that is {} letters long!".format(length))
    times_left = 6  # 玩家剩余猜测次数
    warning_left = 3  # 玩家剩余警告次数
    print("You have {} warnings left.".format(warning_left))
    print("------------- ")
    list_guessed = []
    while times_left > 0:  # 玩家猜测次数没用完
        print("You have {} guesses left.".format(times_left))
        print("Available letters:", get_available_letters(list_guessed))
        char = input("Please guess a letter:")
        x = str.lower(char)
        if x in list_guessed:  # 玩家已经猜过这个字母
            if warning_left > 0:  # 警告次数没用完
                warning_left -= 1
                print("Oops! You've already guessed that letter.You have {} warnings left:".format(warning_left),
                      get_guessed_word(secret_word, list_guessed))
            else:  # 警告次数为0了 减少猜测次数
                times_left -= 1
                print("Oops! You've already guessed that letter.You have no warnings left,so you lose one guess:",
                      get_guessed_word(secret_word, list_guessed))

        else:  # 玩家尚未猜测过这个字母
            list_guessed.append(x)  # 先存储玩家猜测结果
            if not str.isalpha(x):  # 玩家输入不是是字母
                if warning_left > 0:
                    warning_left -= 1
                    print("Oops!That is not a valid letter.You have {} warnings left:".format(warning_left),
                          get_guessed_word(secret_word, list_guessed))
                else:
                    times_left -= 1
                    print(" Oops! That is not a valid letter. You have no warnings left,so you lose one guess:",
                          get_guessed_word(secret_word, list_guessed))
            # 玩家输入是字母时
            elif x in secret_word:  # 玩家猜测字母在目标中
                print("Good guess:", get_guessed_word(secret_word, list_guessed))
                # 玩家猜出全部字母
                if secret_word == get_guessed_word(secret_word, list_guessed):
                    print("------------- ")
                    print("Congratulations, you won!")
                    total_score = times_left * unique_numbers
                    print("Your total score for this game is:", total_score)
                    return
            else:  # 玩家猜测字母不在目标中
                print("Oops! That letter is not in my word.", get_guessed_word(secret_word, list_guessed))
                if x in vowels:  # 没有猜中，且是元音字母
                    times_left -= 2
                else:
                    times_left -= 1
        print("------------- ")
    print("Sorry, you ran out of guesses.The word was {}".format(secret_word))  # 玩家失败，游戏结束
    return


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman(secret_word)

    # secret_word = choose_word(wordlist)
    # hangman_with_hints("apple")
