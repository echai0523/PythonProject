# import xlrd
#
#
# def check_account(user_name, user_psd):
#     workbook = xlrd.open_workbook('user_account.xls')
#
#     table = workbook.sheet_by_index(0)
#
#     nrows = table.nrows
#     result = 0
#     user_id = 0
#
#     for i in range(1, nrows):
#         t1 = table.cell(i, 1).value if isinstance(table.cell(i, 1).value, str) else str(int(table.cell(i, 1).value))
#         t2 = table.cell(i, 2).value if isinstance(table.cell(i, 2).value, str) else str(int(table.cell(i, 2).value))
#
#         if user_name == t1 and user_psd == t2:
#             result = 1
#             user_id = table.cell(i, 0)
#
#     return result, user_id
#
#
# # check_account('xiaoli','1234')



import xlrd

def check_account(user_name,user_psd):

    workbook=xlrd.open_workbook('user_account.xls')

    table = workbook.sheet_by_index(0)

    nrows = table.nrows
    result=0
    user_id=0

    for i in range(1,nrows):
        t1 = table.cell(i,1).value if isinstance(table.cell(i,1).value, str) else str(int(table.cell(i, 1).value))
        t2 = table.cell(i,2).value if isinstance(table.cell(i,2).value, str) else str(int(table.cell(i, 2).value))
        if user_name==t1 and user_psd==t2:
            result=1
            user_id=table.cell(i,0)

    return result,user_id

#check_account('xiaoming','a123')