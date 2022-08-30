# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/25 17:02

input: 
output: 

Short Description: 
    - 知识点：
        - http://c.biancheng.net/matplotlib/9285.html
            - 双轴图twinx添加双轴
            - 柱状图bar
            - 直方图hist
            - 饼状图pie
            - 折线图plot
            - 散点图
            - 等高线图
            - 振动图
            - 箱型图
            - 提亲图
Change History:

"""
from matplotlib import pyplot as plt
from pylab import mpl
import pandas as pd
import numpy as np
from matplotlib import font_manager
from matplotlib import patches

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]
# 设置正常显示符号
mpl.rcParams["axes.unicode_minus"] = False
# # 设置字体大小
# plt.rcParams['font.size'] = 20


def patchs_use():
    figures, ax = plt.subplots(figsize=(50, 30))
    list_x = [201, 153, 144, 26, 58]
    list_y = [13, 44, 43, 136, 11]
    list_r = [3, 6, 1, 9, 7]
    for i in range(len(list_x)):
        c_x = list_x[i]
        c_y = list_y[i]
        c_r = list_r[i]
        ax.add_artist(patches.Circle((c_x, c_y), radius=c_r))
    plt.xlim(0, 250)
    plt.ylim(0, 500)
    ax.set_aspect(1)
    plt.show()



def main():
    """折线图：天气数据，5月气温走势"""
    # 0.准备数据
    date = [d + 1 for d in range(31)]
    highest = [26, 21, 26, 26, 22, 20, 17, 19, 22, 28, 30, 28, 24, 28, 25, 26, 25, 26, 25, 23, 24, 30, 32, 31, 30, 27,
               26,
               27, 29, 25, 25]
    lowest = [17, 13, 17, 18, 18, 17, 14, 15, 16, 18, 19, 20, 18, 18, 20, 20, 20, 20, 20, 16, 17, 19, 21, 24, 24, 23,
              20,
              18, 19, 18, 19]
    # 1.创建画布
    plt.figure(figsize=(15, 5), dpi=100)
    # 2.绘制图像  # marker 设置坐标点 显示方式 'o'圆点
    plt.plot(date, highest, marker='o', color="red", label="最高温度（℃）")
    plt.plot(date, lowest, marker='o', color="blue", label="最低温度（℃）")
    # 2.1 添加x,y轴刻度显示
    plt.xticks([i + 1 for i in range(31)])
    plt.yticks(range(10, 40)[::5])
    # 2.2 添加网格显示
    plt.grid(True, linestyle="--", alpha=0.5)
    # 2.3 添加描述信息
    plt.xlabel("日期（天）")
    plt.ylabel("温度（℃）")
    plt.title("长沙5月份气温走势", fontsize=20)
    # 2.4 图像保存
    plt.savefig("长沙5月份气温走势.png")
    # 2.5 添加图例
    plt.legend(loc="best")
    # 3.图像显示
    plt.show()


if __name__ == '__main__':
    main()
