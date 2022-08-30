# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/26 10:28

input: 

output: 

Short Description: 

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

def main():
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


if __name__ == '__main__':
    main()
