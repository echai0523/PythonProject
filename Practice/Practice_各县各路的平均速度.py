# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/9/25 21:42

input: 

output: 

Short Description: 

Change History:
    
"""
from collections import defaultdict


def calculate_average(save_file_name, map_group, flag=False):
    with open(save_file_name, mode='w', encoding='gbk') as writefile:
        writefile.write("道路编号\t县区\t平均速度\n")
        i = 0
        for key, value in map_group.items():
            i += 1

            if flag:
                xian, lu = key.split('-')
                # 计算平均速度
                average_speed = sum(value) / len(value)
                writefile.write(f"{i}\t{xian}\t{lu}\t{average_speed}\n")
            else:
                # 计算平均速度
                average_speed = sum(value) / len(value)
                writefile.write(f"{i}\t{key}\t{average_speed}\n")


# 按行读取txt所有行
with open('../EthanFileData/txt/【input】县区-道路等级-速度.txt', mode='r', encoding='gbk') as readfile:
    lines = readfile.readlines()

# 用于做映射{县-路: 速度list}
counties_road_group = defaultdict(list)
# 用于做映射{县: 速度list}
counties_group = defaultdict(list)
# 用于做映射{路: 速度list}
road_group = defaultdict(list)

for line in lines[1:]:
    # 处理单行：去掉换行符,并以tab切割
    num, counties, road, speed = line.strip('\n').split('\t')

    # 生成映射{县-路: 速度list}
    counties_road_group[f'{counties}-{road}'].append(float(speed))
    # 生成映射{县: 速度list}
    counties_group[counties].append(float(speed))
    # 生成映射{路: 速度list}
    road_group[road].append(float(speed))

# {县-路: 速度}
calculate_average('县_路_平均速度.txt', counties_road_group, flag=True)

# {县: 速度}
calculate_average('县_平均速度.txt', counties_group)

# {路: 速度}
calculate_average('路_平均速度.txt', road_group)

