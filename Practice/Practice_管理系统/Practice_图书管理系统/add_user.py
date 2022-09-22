from tkinter import *
from tkinter import ttk
import xlwt,xlrd
from xlutils.copy import copy
from save_data import *
from tkinter.messagebox import *

class AddUser(Frame): # 继承Frame类

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master #定义内部变量root
        self.txt_id=StringVar()
        self.txt_name=StringVar()
        self.txt_psd=StringVar()
        self.createPage()

    def createPage(self):
        Label(self, text='    ').pack()
        Label(self, text='添加用户', font=("微软雅黑", 28), fg='#0000ff').pack()

        Label(self, text='    ').pack()
        Label(self, text='    ').pack()
        Label(self, text='输入用户ID:',font=("微软雅黑",14)).pack()
        en1 = Entry(self,  font=("微软雅黑", 14),textvariable=self.txt_id)
        en1.pack()

        Label(self, text='    ').pack()
        Label(self, text='输入用户名:',font=("微软雅黑",14)).pack()
        en2 = Entry(self,  font=("微软雅黑", 14),textvariable=self.txt_name)
        en2.pack()

        Label(self, text='    ').pack()
        Label(self, text='输入用户密码:',font=("微软雅黑",14)).pack()
        en3 = Entry(self,  font=("微软雅黑", 14),textvariable=self.txt_psd)
        en3.pack()

        Label(self, text='    ').pack()
        B = Button(self, text="确定",font=("微软雅黑", 14),command=self.mClick)
        B.pack()

    def mClick(self):
        data_list = []
        u_id = int(self.txt_id.get())  # 因为用户id是整数类型，所以要进行类型转换
        data_list.append(u_id)
        data_list.append(self.txt_name.get())
        data_list.append(self.txt_psd.get())
        file_name = 'user_account.xls'
        save_data(data_list, file_name)
        showinfo(title='添加用户成功！', message='添加用户成功！')
