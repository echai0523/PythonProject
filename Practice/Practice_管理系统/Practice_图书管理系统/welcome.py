from tkinter import *
import turtle  # 导入turtle模块
import time

class ShowWelcome(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.createPage()

    def createPage(self):
        canva = Canvas(self.root, width=400, height=400)  # 设定画布
        canva.pack()

        theScreen = turtle.TurtleScreen(canva)  # 设定turtle屏幕
        path = turtle.RawTurtle(theScreen)  # 设定画笔

        path.color('blue')  # 设定画笔颜色
        path.left(180)
        path.up()  # 抬笔
        path.forward(80)
        path.down()  # 落笔
        path.write('欢迎进入本系统', font=('宋体', 18))
        path.up()
        path.forward(100)
        path.down()
        path.left(90)
        path.forward(100)
        path.left(90)
        path.forward(350)
        time.sleep(3)
        canva.pack_forget()