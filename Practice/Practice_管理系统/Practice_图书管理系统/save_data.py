import xlwt,xlrd
from xlutils.copy import copy

def save_data(list_data,file_name):
    my_file = file_name
    data = xlrd.open_workbook(my_file)
    excel = copy(wb=data)  # 完成xlrd对象向xlwt对象转换
    excel_table = excel.get_sheet(0)  # 获得要操作的页
    table = data.sheets()[0]
    nrows = table.nrows  # 获得行数
    ncols = 0  # 获得列数
    values = list_data

    for value in values:
        excel_table.write(nrows, ncols, value)  # 因为单元格从0开始算，所以row不需要加一
        ncols = ncols + 1
    # os.remove('excel_test.xls')
    excel.save(my_file)
    return