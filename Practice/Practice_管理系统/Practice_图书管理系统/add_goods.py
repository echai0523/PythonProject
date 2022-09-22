from tkinter import *
from tkinter import ttk
import xlwt, xlrd
from xlutils.copy import copy
from save_data import *
from tkinter.messagebox import *


class AddGoods(Frame):  # 继承Frame类

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.goods_id = StringVar()
        self.goods_name = StringVar()
        self.goods_typoe = StringVar()
        self.goods_chuban = StringVar()
        self.goods_zuozhe = StringVar()
        self.goods_price = StringVar()
        self.goods_img = StringVar()

        self.createPage()

    def createPage(self):
        Label(self, text='    ').pack()
        Label(self, text='添加用户', font=("微软雅黑", 28), fg='#0000ff').pack()

        Label(self, text='    ').pack()
        Label(self, text='    ').pack()
        Label(self, text='输入图书ID:', font=("微软雅黑", 14)).pack()
        en1 = Entry(self, font=("微软雅黑", 14), textvariable=self.goods_id)
        en1.pack()

        Label(self, text='    ').pack()
        Label(self, text='输入图书名:', font=("微软雅黑", 14)).pack()
        en2 = Entry(self, font=("微软雅黑", 14), textvariable=self.goods_name)
        en2.pack()

        Label(self, text='    ').pack()
        Label(self, text='输入图书类型:', font=("微软雅黑", 14)).pack()
        en3 = Entry(self, font=("微软雅黑", 14), textvariable=self.goods_typoe)
        en3.pack()

        Label(self, text='    ').pack()
        Label(self, text='输入图书出版社:', font=("微软雅黑", 14)).pack()
        en4 = Entry(self, font=("微软雅黑", 14), textvariable=self.goods_chuban)
        en4.pack()

        Label(self, text='    ').pack()
        Label(self, text='输入图书作者:', font=("微软雅黑", 14)).pack()
        en5 = Entry(self, font=("微软雅黑", 14), textvariable=self.goods_zuozhe)
        en5.pack()

        Label(self, text='    ').pack()
        Label(self, text='输入图书价格:', font=("微软雅黑", 14)).pack()
        en6 = Entry(self, font=("微软雅黑", 14), textvariable=self.goods_price)
        en6.pack()

        Label(self, text='    ').pack()
        Label(self, text='输入图书gif文件名:', font=("微软雅黑", 14)).pack()
        en7 = Entry(self, font=("微软雅黑", 14), textvariable=self.goods_img)
        en7.pack()

        Label(self, text='    ').pack()
        en8 = Button(self, text="确定", font=("微软雅黑", 14), command=self.mClick)
        en8.pack()

    def mClick(self):
        data_list = []
        g_id = int(self.goods_id.get())  # 因为id是整数类型，所以要进行类型转换
        g_price = int(self.goods_price.get())  # 因为price是整数类型，所以要进行类型转换
        data_list.append(g_id)
        data_list.append(self.goods_name.get())
        data_list.append(self.goods_typoe.get())
        data_list.append(self.goods_chuban.get())
        data_list.append(self.goods_zuozhe.get())
        data_list.append(g_price)
        data_list.append(self.goods_img.get())
        file_name = 'goods.xls'
        save_data(data_list, file_name)
        showinfo(title='添加用户成功！', message='添加用户成功！')
