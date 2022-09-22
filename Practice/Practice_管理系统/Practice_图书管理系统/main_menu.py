import tkinter
from tkinter import *
from welcome import *
from count_goods import ShowCountGoods
from show_goods import *
from show_goods_info import *
from add_goods import *
from add_user import *


class MainMenu:

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("主界面   matianxiang 2021100424")  # 加入自己姓名、学号
        self.root.geometry('800x500')
        self.createPage()
        self.root.mainloop()

    def createPage(self):
        self.welcomePage = ShowWelcome(self.root)
        self.showGoodsPage = ShowGoods(self.root)
        self.showGoodsInfoPage = ShowGoodsInfo(self.root)
        self.addGoodsPage = AddGoods(self.root)
        self.addUserPage = AddUser(self.root)
        self.ShowCountGoodsPage = ShowCountGoods(self.root)

        menubar = Menu(self.root)  # 定义菜单条
        self.root.config(menu=menubar)

        # 创建下拉菜单，并添加到菜单条
        operationMenu = Menu(menubar, tearoff=0)  # 在菜单条中定义“浏览”菜单
        menubar.add_cascade(label="浏览", menu=operationMenu)

        operationMenu.add_command(label="商品浏览", command=self.show_goods_command)
        operationMenu.add_command(label="商品详情", command=self.show_goods_info_command)
        operationMenu.add_command(label="公告信息", command=self.show_goods_command)

        setMenu = Menu(menubar, tearoff=0)  # 在菜单条中增加“管理”菜单
        menubar.add_cascade(label="管理", menu=setMenu)
        setMenu.add_command(label="添加图书", command=self.show_add_goods_command)
        setMenu.add_command(label="添加用户", command=self.show_add_user_command)

        countMenu = Menu(menubar, tearoff=0)  # 在菜单条中定义“统计”菜单
        menubar.add_cascade(label="统计", menu=countMenu)
        countMenu.add_command(label="商品统计", command=self.show_count_goods_command)

        exitMenu = Menu(menubar, tearoff=0)  # 在菜单条中定义“退出”菜单
        menubar.add_cascade(label="退出", menu=exitMenu)
        exitMenu.add_command(label="退出", command=self.root.quit)

    def show_count_goods_command(self):
        self.ShowCountGoodsPage.pack(fill="both", expand=True)
        self.showGoodsInfoPage.pack_forget()  # 用于切换
        self.addUserPage.pack_forget()  # 用于切换
        self.showGoodsPage.pack_forget()
        self.addGoodsPage.pack_forget()

    def show_goods_command(self):
        self.showGoodsPage.pack(fill="both", expand=True)
        self.showGoodsInfoPage.pack_forget()  # 用于切换
        self.addUserPage.pack_forget()  # 用于切换
        self.ShowCountGoodsPage.pack_forget()
        self.addGoodsPage.pack_forget()

    def show_goods_info_command(self):
        self.showGoodsInfoPage.pack(fill="both", expand=True)
        self.showGoodsPage.pack_forget()  # 用于切换
        self.addUserPage.pack_forget()  # 用于切换
        self.ShowCountGoodsPage.pack_forget()
        self.addGoodsPage.pack_forget()

    def show_add_user_command(self):
        self.addUserPage.pack(fill="both", expand=True)
        self.showGoodsPage.pack_forget()  # 用于切换
        self.showGoodsInfoPage.pack_forget()  # 用于切换
        self.ShowCountGoodsPage.pack_forget()
        self.addGoodsPage.pack_forget()

    def show_add_goods_command(self):
        self.addGoodsPage.pack(fill="both", expand=True)
        self.addUserPage.pack_forget()
        self.showGoodsPage.pack_forget()  # 用于切换
        self.showGoodsInfoPage.pack_forget()  # 用于切换
        self.ShowCountGoodsPage.pack_forget()

    def welcome_command(self):
        self.welcomePage.pack(fill='both', expand=True)


MainMenu()
