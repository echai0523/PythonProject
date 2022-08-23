# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/23 11:25

input: 
output: 
Short Description:
    - 知识点：
        - plot
            - plot methods: 'bar', 'hist', 'box', 'kde', 'area', scatter', hexbin', 'pie'
Change History:

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def pandas_plot_v1():
    # Series
    data = pd.Series(np.random.randn(1000), index=np.arange(1000))
    data = data.cumsum()
    ##data.plot()

    # DataFrame
    data = pd.DataFrame(np.random.randn(1000, 4), index=np.arange(1000), columns=list("ABCD"))
    data = data.cumsum()
    # plot methods: 'bar', 'hist', 'box', 'kde', 'area', scatter', hexbin', 'pie'
    ax = data.plot.scatter(x='A', y='B', color='DarkBlue', label="Class 1")
    data.plot.scatter(x='A', y='C', color='LightGreen', label='Class 2', ax=ax)

    plt.show()


def pandas_plot():
    # Q1成绩折线分布
    df['Q1'].plot()
    plt.show()

    # ben四季度的成绩变化
    df.loc['Ben', 'Q1':'Q4'].plot()         # 折线图
    df.loc['Ben', 'Q1':'Q4'].plot().bar()   # 柱状图
    df.loc['Ben', 'Q1':'Q4'].plot().barh()  # 横向柱状图

    # 各Team四季度总成绩趋势
    df.groupby('team').sum().T.plot()
    df.groupby('team').count().Q1.plot.pie()    # 饼图


def main():
    # 画图
    pandas_plot()


if __name__ == '__main__':
    df = pd.read_excel('https://www.gairuo.com/file/data/dataset/team.xlsx')
    main()
