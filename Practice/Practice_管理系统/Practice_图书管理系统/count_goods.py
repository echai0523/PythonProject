from tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter


class ShowCountGoods(Frame):  # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master #定义内部变量root
        self.createPage()

    def createPage(self):
        Label(self, text='    ').pack()
        Label(self, text='图书统计信息', font=("微软雅黑", 28), fg='#0000ff').pack()
        self.drawPie()       #---------添加调用语句--------

    def drawPie(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体，便于显示中文
        matplotlib.use('TkAgg')

        pie = plt.figure(figsize=(4.4, 4.4), facecolor="#F0F0F0")  # 调节图形大小、背景色

        # pie.labels = ['小说', '科普', '考试', '传统文化']  # 给出要展示的内容（标签）
        # pie.sizes = [2, 1, 1, 1]  # 每个饼块的值
        # pie.colors = ['green', 'red', 'blue', 'orange']  # 自定义颜色
        # pie.explode = (0.04, 0.04, 0.04, 0.04)  # 分割，值越大分割出的间隙越大
        df = pd.read_excel("goods.xls")
        results = Counter([i for i in df['goods_type']])
        pie.labels = [k for k in results.keys()]
        pie.sizes = [results[k] for k in results.keys()]
        pie.colors = ['green', 'red', 'blue', 'orange', 'black', 'tan', 'brown']  # 自定义颜色
        pie.explode = (0.04, ) * len(results)  # 分割，值越大分割出的间隙越大

        pie.patches, pie.text2, pie.text1 = plt.pie(pie.sizes,
                                                    explode=pie.explode,
                                                    labels=pie.labels,
                                                    colors=pie.colors,
                                                    autopct='%3.1f%%',  # 数值保留小数位数
                                                    shadow=True,  # 有、无阴影设置
                                                    startangle=90,  # 逆时针起始角度设置
                                                    pctdistance=1.4,  # 标签数字和圆心的距离
                                                    textprops={'fontsize': 8, 'color': '#000080'}
                                                    )
        plt.axis('equal')  # 正圆

        for t in pie.text2:  # 设置饼图标签的字体大小
            t.setsize = 8

        canvas_statis = FigureCanvasTkAgg(pie, self)

        # canvas_statis.get_tk_widget().place(x=140, y=140)#根据坐标，放在指主窗口的指定位置

        canvas_statis.get_tk_widget().pack()

