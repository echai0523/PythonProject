# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
import ast
from collections import defaultdict

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]
# 设置正常显示符号
mpl.rcParams["axes.unicode_minus"] = False


def top30_parse(df):
    # 按评分降序排列
    df_score = df.sort_values('score', ascending=False)
    name = df_score.name[:30]  # x轴坐标名
    score = df_score.score[:30]  # 坐标点

    # 设置图片大小
    fig = plt.figure(figsize=(12, 8))
    # 绘制图像  # marker 设置坐标点 显示方式 'o'圆点
    plt.plot(name, score, marker='o', color="red", label="评分")
    # 添加x,y轴刻度显示
    plt.xticks(name, rotation=270, fontsize=7)
    # 使用numpy遍历步长为0.1
    plt.yticks([round(num, 1) for num in np.arange(9.1, 10.1, 0.1)])
    # 添加网格显示
    plt.grid(True, linestyle="--", alpha=0.5)
    # 添加描述信息
    plt.xlabel("电影名称")
    plt.ylabel("评分")
    plt.title("电影评分最高top30", fontsize=20)
    # 图像保存
    plt.savefig("电影评分最高top30.png", bbox_inches='tight')
    # 添加图例
    plt.legend(loc="best")
    # 图像显示
    plt.show()


def year_parse(df):
    grouped_year = df.groupby('year')
    grouped_year_amount = grouped_year.year.count()
    # top_year = grouped_year_amount.sort_values(ascending=False)
    year_info = grouped_year_amount.index.values
    year_count = grouped_year_amount.tolist()
    # 绘图
    # 设置图片大小
    fig = plt.figure(figsize=(23, 8))
    # year_count.plot(kind='bar', color='blue')
    plt.bar(range(len(year_info)), year_count, width=0.5)
    for x, y in enumerate(year_count):
        plt.text(x, y + 0.1, '%s' % round(y, 1), ha='center', color="blue")
    plt.title('各年份电影数量分析')
    plt.xlabel('年份(年)')
    plt.ylabel('数量(部)')
    plt.xticks(list(range(0, 56, 1)), year_info, rotation=45)
    plt.savefig('各年份电影数量分析.png')
    plt.show()


def label_parse(df):
    label_count_map = defaultdict(int)
    df = pd.read_excel('DouBan.xlsx')
    for _, row in df.iterrows():
        for label in ast.literal_eval(row["label"]):
            label_count_map[label] += 1

    x_data = [label for label in label_count_map.keys()]
    y_data = [count for count in label_count_map.values()]
    # y = np.array([35, 25, 25, 15])
    # 设置图片大小
    fig = plt.figure(figsize=(23, 8))
    plt.barh(x_data, y_data)
    for i, y in enumerate(y_data):
        plt.text(y + 2,  # 数值与柱体相对x轴的距离
                 i - 0.2,  # 数值与柱体相对y轴的距离
                 str(y),  # 数值
                 ha='center',
                 color="blue")
    plt.xlabel("类型")
    plt.ylabel("条数")
    plt.title("各类型电影数量分析")  # 设置标题
    plt.savefig("各类型电影数量分析.png")
    plt.show()


# 读取数据表
data_frame = pd.read_excel('DouBan.xlsx')
# 电影评分最高top30
top30_parse(df=data_frame)
# 统计各年上映的电影数量
year_parse(df=data_frame)
# 统计label
label_parse(df=data_frame)
