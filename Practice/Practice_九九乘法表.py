# -*- coding: UTF-8 -*-
"""
Author: Ethan Chai
Date: 2022/8/25 17:02

input:
    - 九九乘法表
    - 字符串拆分后一个数比前一个数大
        - "314159265"
        - 3 14 15 92
    - 1000以下的数字转换为对应的大写
output:

Short Description:

Change History:

"""
def nine_x_nine():
    """九九乘法表"""
    for i in range(1, 10):
        for j in range(1, i+1):
            print(f'{j}x{i}={i*j}\t', end='')
        print()


def str_split():
    """字符串拆分后一个数比前一个数大"""
    # 例如输入"314159265"
    Input = input("INPUT:")

    # 输出3 14 15 92 ->先将每个数用list列表保存，在通过' '.join(list)方法按空格拼接在一起
    Output = list()

    # 定义第一位数
    Org = int(Input[0])
    # 先将第一个数添加到Output
    Output.append(str(Org))
    # 切片：list[star: end]
    # 定义切片star
    star = 1
    # for遍历Input索引获取切片end，因为第一个数占了索引0，切片star是1开始，所以end从2开始遍历
    for end in range(star + 1, len(Input)):
        # 判断int(Input[star:end])是否大于前一个数
        if int(Input[star:end]) > Org:
            # 如果大于前一个数，则将这个数添加到Output
            Output.append(Input[star:end])
            # 更新前一个数
            Org = int(Input[star:end])
            # 更新切片star
            star = end

    print("OUTPUT:" + ' '.join(Output))


def num_1000_to_NUM_1000():
    """1000以下的数字转换为对应的大写"""
    while True:
        input_num = input("请输入0-999内的数字: ")
        number = input_num if isinstance(input_num, str) else str(input_num)
        ch_num = '零一二三四五六七八九'
        if len(input_num) == 1:
            print(ch_num[int(number)])
        elif len(input_num) == 2:
            if int(input_num[0]) == 1 and int(input_num[1]) == 0:
                print("十")
            elif int(input_num[1]) == 0:
                print(f"{ch_num[int(number[0])]}十")
            else:
                print(f"{ch_num[int(number[0])]}十{ch_num[int(number[1])]}")
        elif len(input_num) == 3:
            if int(input_num[1]) == 0:
                print(f"{ch_num[int(number[0])]}百{ch_num[int(number[1])]}{ch_num[int(number[2])]}")
            elif int(input_num[2]) == 0:
                print(f"{ch_num[int(number[0])]}百{ch_num[int(number[1])]}十")
            else:
                print(f"{ch_num[int(number[0])]}百{ch_num[int(number[1])]}十{ch_num[int(number[2])]}")
        else:
            print("您输入非0-999内的数字，格式错误，退出程序")
            break



