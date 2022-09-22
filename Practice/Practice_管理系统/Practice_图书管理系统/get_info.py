import xlrd


def get_info(g_id):
    workbook = xlrd.open_workbook('goods.xls')  # 打开excel文件
    table = workbook.sheet_by_index(0)  # 获取第1个sheet
    nrows = table.nrows  # 获取行数

    goods_name = ''   #变量初始化
    goods_type = ''
    goods_chuban = ''
    goods_zuozhe = ''
    goods_price = 0.0
    goods_img = ''


    for i in range(1,nrows):
        if g_id == table.cell(i, 0).value:
            goods_name = table.cell(i, 1).value
            goods_type = table.cell(i, 2).value
            goods_chuban = table.cell(i, 3).value
            goods_zuozhe = table.cell(i, 4).value
            goods_price = table.cell(i, 5).value
            goods_img = table.cell(i, 6).value

            break

    return goods_name, goods_type, goods_chuban, goods_zuozhe, goods_price, goods_img
