# -*- coding: UTF-8 -*-

import pandas as pd


def main(excel_file):
    """
    原始表新添子表Sheet2
    :param excel_file: excel文件路径
    :return: None
    """

    name_list = []
    new_sheet = []

    df = pd.read_excel(excel_file)
    # 根据'prod'分组
    group_ = df.groupby('prod')
    # 遍历得到每一组 ：获取 name(产品类型)， g(Series(Q_tij))
    for name, g in group_:
        # Series类型需要遍历获取值
        Q_tij_data = [Q for Q in g['Q_tij']]
        # 将产品类型写入列表 作为index使用
        name_list.append(name)
        # 将Q_tij值写入列表 作为数据
        new_sheet.append(Q_tij_data)
    # Sheet2 的 DataFrame：将Q_tij数据转为DataFrame，产品类型为索引
    new_sheet_df = pd.DataFrame(new_sheet, index=name_list)

    # 多表写入
    with pd.ExcelWriter(excel_file) as writer:
        # Sheet1：写入原有数据
        df.to_excel(writer, sheet_name='Sheet1', index=None)
        # Sheet2：索引根据产品类型，无头部(列名)
        new_sheet_df.to_excel(writer, sheet_name='Sheet2', index=True, header=None)


if __name__ == "__main__":
    # 输入文件绝对路径，如：r"C:\···路径···\data.xlsx"
    # main(r'')
    # 当前excel与py脚本同路径 时 可用
    main(r"data.xlsx")
