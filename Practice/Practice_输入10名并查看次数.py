# -*- coding: UTF-8 -*-

"""
1.先定义一个空的dict，用来存放名字和对应的次数，如{name: 1}
2.添加10个名字，构建死循环，添加10次后退出
3.最后输出名字输入次数
"""

# 定义空dict
name_info = dict()

# 循环10次
num = 10
while num:
    # 输入名字
    name = input("请输入名字：")
    # 判断名字是否在字典里
    if name not in name_info:
        # 如果不在字典里，则在字典里添加name: 1  ---> 某某：输入1次
        name_info[name] = 1
    else:
        # 如果在字典里，则在字典中name的值+1  ---> 某某： 输入 1+1次
        name_info[name] += 1
    # 循环减少一次，当循环10次后，num==0，退出循环
    num -= 1

# 遍历字典name_info里面的名字name和对应的值count
for name, count in name_info.items():
    print(name, "输入次数：", count, "次")






