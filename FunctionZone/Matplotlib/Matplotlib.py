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


def plot_use():
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


def bar_use():
    """
    条形图：三类学校报名人数
    要求:
        以下的data数据是三类学校在2014-2018（包含2018）的报名人数，用DataFrame构建。
        把年份当做x轴，报名人数当做y轴的值。
        绘制分组条形图，同一个年份的放在一个组。
        图例横向排列（提示：用legend的ncol参数，ncol表示的是把图例分成多少列显示）
        把报名人数在图上绘制出来。
    """
    data = {
        "普通本科": [721, 738, 749, 761, 791],
        "中等职业教育": [620, 601, 593, 582, 557],
        "普通高中": [797, 797, 803, 800, 793]
    }
    df = pd.DataFrame(data=data)
    font = font_manager.FontProperties(fname=r"C:\\Windows\\Fonts\\msyh.ttc", size=12)
    # 设置图的大小
    plt.figure(figsize=(15, 5))
    bar_width = 0.2
    # x轴的刻度
    xticks = np.arange(2014, 2019)
    # 循环列，按照年份绘制条形图
    for index, column in enumerate(df.columns):
        values = df[column]
        c_xticks = xticks + bar_width * (index - 1)
        plt.bar(c_xticks, values, width=bar_width, label=column)
        for x, y in zip(c_xticks, values):
            plt.annotate(y, xy=(x, y), xytext=(x - 0.05, y + 10))
    # 设置Y轴顶部的最大值
    plt.ylim(top=1000)
    # 设置Y轴的标题显示，默认是垂直显示，使用rotation=horizontal变成横向显示，并且通过y修改在y轴的位置
    plt.ylabel("万人", fontproperties=font, rotation="horizontal")
    # 通过set_label_coords才能灵活设置ylabel的位置。以下代码可选实现（不懂删掉没有任何关系）
    plt.gca().yaxis.set_label_coords(-0.02, 1.02)
    # 设置图例，ncol表示要把图例显示成几列，loc表示在Axes中的哪个位置
    plt.legend(prop=font, ncol=3, loc='upper right')
    # 设置标题
    plt.title("2014-2018普通本科、中等职业教育、普通高中招生人数", fontproperties=font)
    plt.show()


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
    pass


if __name__ == '__main__':
    main()
