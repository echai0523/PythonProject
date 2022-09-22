# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/9/15 15:37

input:

output:

Short Description:
    - 逻辑：
        - 1. 计算机(CPU)随机出拳，玩家(player)手动输入出拳
        - 2. 石头可以击毁剪刀：Rock smashes Paper
        - 3. 剪刀可以剪碎布：Paper cut Scissors
        - 4. 布可以覆盖石头：Scissors covers Rock
        - 5. CPU赢则CPU+1分，player赢则player+1，Tie平局玩家重新出拳
        - 6. 玩家输入'E'则展示CPU与player得分情况并退出游戏
Change History:
    
"""
import random

# CPU随机出剪刀石头布
choices = ["Rock", "Paper", "Scissors"]
computer = random.choice(choices)

player = False
cpu_score = 0
player_score = 0
while True:
    # 玩家输入，并将输入的内容转为首字母大写
    player = input("Rock, Paper or Scissors?").capitalize()
    # 判断游戏者和电脑的选择
    # 当玩家出拳与CPU出拳一致：平局，玩家重新输入
    if player == computer:
        print("Tie!")
    # 当玩家猜"Rock"时
    elif player == "Rock":
        # 如果CPU猜"Scissors"，布 包裹 石头， CPU赢 +1
        if computer == "Scissors":
            print("You lose!", computer, "covers", player)
            cpu_score += 1
        # 否则CPU猜"Paper"， 石头 击毁 剪刀， 玩家赢 +1
        else:
            print("You win!", player, "smashes", computer)
            player_score += 1
    # 当玩家猜"Paper"时
    elif player == "Paper":
        if computer == "Rock":
            print("You lose!", computer, "smashes", player)
            cpu_score += 1
        else:
            print("You win!", player, "cut", computer)
            player_score += 1
    # 当玩家猜"Scissors"时
    elif player == "Scissors":
        if computer == "Paper":
            print("You lose!", computer, "cut", player)
            cpu_score += 1
        else:
            print("You win!", player, "covers", computer)
            player_score += 1
    elif player == 'E':
        print("***Final Scores:***")
        print(f"\tCPU:{cpu_score}")
        print(f"\tPlaer:{player_score}")
        break
    else:
        print("That's not a valid play. Check your spelling!")
    computer = random.choice(choices)
