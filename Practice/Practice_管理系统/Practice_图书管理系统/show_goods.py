from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import xlrd

class ShowGoods(Frame): # 继承Frame类
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master  # 定义内部变量root
        self.createPage()

    def createPage(self):
        Label(self, text='    ').pack()                     #空白格，占地方，好看
        Label(self, text='浏览商品界面', font=("仿宋", 28), fg='#6633cc').pack()
        self.get_data()

    def get_data(self):
        GID = 0
        GNAME = 1
        GTYPE = 2
        GCHUBAN = 3
        GZUOZHE = 4

        workbook = xlrd.open_workbook('goods.xls')
        table = workbook.sheet_by_index(0)
        nrows = table.nrows

        tree_table = ttk.Treeview(self, height=nrows-1, show="headings")
        tree_table['columns'] = ['gid', 'gname', 'gtype', 'gchuban', 'gzuozhe']
        tree_table.pack()

        tree_table.heading('gid', text='图书ID')
        tree_table.heading('gname', text='图书名字')
        tree_table.heading('gtype', text='图书类型')
        tree_table.heading('gchuban', text='出版社')
        tree_table.heading('gzuozhe', text='作者')

        tree_table.column('gid', width=50)  # 设定列宽度

        for i in range(1, nrows):
            gid = int(table.cell(i, GID).value)
            gname = table.cell(i, GNAME).value
            gtype = table.cell(i, GTYPE).value
            gchuban = table.cell(i, GCHUBAN).value
            gzuozhe = table.cell(i, GZUOZHE).value
            tree_table.insert('', i, text=i, values=(gid, gname, gtype, gchuban, gzuozhe))







