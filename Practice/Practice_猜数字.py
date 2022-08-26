# -*- coding: UTF-8 -*-
"""
Author: Ethan Chai
Date: 2022/8/25 17:02

input:
output:

Short Description:
    - 需求：
        0、执行guess.py(代码文件名称)运行游戏
        1、一方出数字(random随机数)，随机生成一个没有重复数字的4位数序列（可以0为首）
        2、一方猜(input输入)，处于待输入状态等待用户输入
        3、每猜一次，游戏根据输入打印出几A几B的反馈信息
            - A前的数字表示 位置正确 的数的个数
            - B前的数字表示 数字正确而位置不对 的数的个数
            如：正确答案为 5234，而猜的人猜 5346，则是 1A2B，
                - 有一个5的位置对了，记为 1A
                - 3和4这两个数字对了，而位置没对，因此记为 2B
        4、玩家重复输入4个阿拉伯数字，直到游戏反馈4A0B的结果结束
            1、死循环：最外层循环(表示游戏不终止，需输入执行选项退出游戏)
            2、反馈信息：几A几B
            3、4A0B退出循环
        5、玩家可以通过输入特别的指令，用于查询、修改重置被猜数字序列
            1. 死循环：重置被猜数字  用户重新猜
            2、反馈信息：几A几B
            3、4A0B退出循环

游戏功能完整，逻辑正确；游戏交互友好，不纠结不报错。
Change History:

"""
"""

"""
from random import choice


def random_four_num():
    # 出数字(random随机数)，随机生成一个没有重复数字的4位数序列（可以0为首）
    org_num_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    random_num = str()
    for _ in range(4):
        # 随机在0-9中选择一个数，并通过pop方法将该数从list中删除，避免重复选择
        random_num += str(org_num_list.pop(org_num_list.index(choice(org_num_list))))
    return random_num


#  统计猜测次数
guess_count = 0
# 要实现死循环，一直猜，直到4A0B退出
org_tag = True  # 初始死循环标志
while org_tag:
    # 出数字(随机四位数)
    random_four = random_four_num()

    # 再套死循环，实现查询、重置功能
    query_reset_tag = True  # 查询标志
    while query_reset_tag:
        # 猜(input输入)
        input_four = input("请输入一个没有重复数字的4位阿拉伯数字的序列（可以0为首）：")
        # 猜测次数开始累加
        guess_count += 1

        if len(input_four) != 4:
            print("您输入{}个数，不符合要求。".format(len(input_four)))
            continue

        # 统计A的个数
        A_count = 0
        # 统计B的个数
        B_count = 0

        for i in range(4):
            # 数字和位置都相同，则A+1
            if input_four[i] == random_four[i]:
                A_count += 1
            # 位置不同，数字在随机数中出现，则B+1
            elif input_four[i] != random_four[i] and input_four[i] in random_four:
                B_count += 1
            # 以上情况没有出现，则A==0,B==0
            else:
                continue

        # 几A几B
        xAyB = "{}A{}B".format(A_count, B_count)
        # 输入打印出几A几B的反馈信息
        # 4A0B退出循环
        if xAyB == "4A0B":
            print("""
**************************
* 哇！恭喜你{}次猜对！你真棒！*
**************************
""".format(guess_count))
            # 如果4A0B则退出游戏
            function = "Q"
#             # 如果猜测正确则提供选择下一局或者退出游戏
#             function = input("""
# ************************************
# 请选择是否需要退出游戏(如:输入Q表示退出):
#         N. 进入下一回合
#         Q. 退出游戏
# ************************************
#         您的选项：
# """)
#             # 捕获 任意 异常，退出游戏
#             try:
#                 # 断言：输入的选项在列表中出现，否则 print 并抛出异常
#                 assert function in ['N', 'Q'], print(f"您输入 {function} 选项，不符合要求。惩罚：退出游戏。", end='\t')
#             except Exception:
#                 query_reset_tag = False
#                 org_tag = False
        # 未出现4A0B，则输出几A几B的反馈信息
        else:
            print("******  您的猜测有些小问题，请再接再厉哟！温馨小提示：{}  ******".format(xAyB))
            # 添加查询、修改功能
            function = input("""
***************************************
请选择接下来的操作(如:输入3表示查询被猜数字): 
    1. 继续进行盲猜
    2. 查询被猜数字
    3. 重置被猜数字
    0. 退出游戏
***************************************
    您的选项：
""")
            if function not in ['1', '2', '3', '0']:
                print("您输入 {} 选项，不符合要求。惩罚：退出游戏。".format(function))
                query_reset_tag = False
                org_tag = False

        # 继续进行盲猜
        if function == "1":
            guess_count = guess_count
            continue
        # 查询被猜数字
        elif function == "2":
            print("正确答案：{}".format(random_four))
        # 重置被猜数字
        elif function == "N" or function == "3":
            random_four = random_four_num()
            guess_count = 0
            print("******  当前谜底正确答案已重置，欢迎来到新回合  ******")
        # 退出游戏
        elif function == "Q" or function == "0":
            Quit_tag = True
            while Quit_tag:
                Quit = input("""
***********************
请确认是否要退出游戏(y/n)?
***********************
        您的选项：
""")
                if Quit == "y" or Quit == "Y":
                    Quit_tag = False
                    query_reset_tag = False
                    org_tag = False
                elif Quit == "n" or Quit == "N":
                    Quit_tag = False
                else:
                    print("****您是分不清 y(Y) or n(N) 吗****")
                    Quit_tag = True


















