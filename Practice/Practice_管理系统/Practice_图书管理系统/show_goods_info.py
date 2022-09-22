from tkinter import *
import xlrd
from tkinter import ttk
from get_info import *

class ShowGoodsInfo(Frame):                     #继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master                      #定义内部变量root
        self.txt1 = StringVar()
        self.createPage()

    def createPage(self):
        Label(self, text='     ').pack()
        Label(self, text='展示商品详情', font=("宋体", 28), fg='#00CED1').pack()

        goods_name, goods_type, goods_chuban, goods_zuozhe, goods_price, goods_img = get_info(1)

        self.img= PhotoImage(file='img/'+goods_img)
        goods_pic=Label(self, image=self.img, height=789, width=793)
        goods_pic.place(x=540, y=150)

        Label(self, text=goods_name, font=("微软雅黑", 18)).place(x=260, y=160)
        Label(self, text=goods_type, font=("微软雅黑", 8)).place(x=260, y=220)
        Label(self, text=goods_chuban, font=("微软雅黑", 8)).place(x=260, y=320)
        Label(self, text=goods_zuozhe, font=("微软雅黑", 8)).place(x=260, y=280)
        Label(self, text=str(goods_price) + '元', font=("微软雅黑", 8)).place(x=250, y=250)

        Label(self, text='输入商品ID').place(x=120, y=390)
        en1 = Entry(self, width=3, textvariable=self.txt1)  # 输入框
        en1.place(x=250, y=390)

        B = Button(self, text="确定", command=self.mClick)  # 定义确定按钮,并设定响应函数！
        B.place(x=300, y=380)

    def mClick(self):
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text='     ').pack()
        Label(self, text='展示商品详情', font=("宋体", 28), fg='#00CED1').pack()

        goods_id=int(self.txt1.get())
        goods_name, goods_type, goods_chuban, goods_zuozhe, goods_price, goods_img = get_info(goods_id)

        self.img = PhotoImage(file='img/' + goods_img)
        goods_pic = Label(self, image=self.img, height=789, width=793)
        goods_pic.place(x=540, y=150)

        Label(self, text=goods_name, font=("微软雅黑", 18)).place(x=260, y=160)
        Label(self, text=goods_type, font=("微软雅黑", 8)).place(x=260, y=220)
        Label(self, text=goods_chuban, font=("微软雅黑", 8)).place(x=260, y=320)
        Label(self, text=goods_zuozhe, font=("微软雅黑", 8)).place(x=260, y=280)
        Label(self, text=str(goods_price) + '元', font=("微软雅黑", 8)).place(x=250, y=250)

        Label(self, text='输入商品ID').place(x=120, y=390)
        en1 = Entry(self, width=3, textvariable=self.txt1)  # 输入框
        en1.place(x=250, y=390)

        B = Button(self, text="确定", command=self.mClick)  # 定义确定按钮,并设定响应函数！
        B.place(x=300, y=380)





