# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/18 12:37

input:
    - 修改列值.xlsx (链接: https://pan.baidu.com/s/1lsDV6sPi6DP2XVQwPA1bgw?pwd=icpy)
output:
    - Result_data.xlsx
Short Description:
    - 知识点；
        - pd.read_excel(header=None, names=["A1", "A2", "A3"])
        - pd.to_excel(header=None)
        - df[""].apply(lambda x: x)
    - 需求：
        第一列：把数字-3到0替换成“苹果”，1-5替换成香蕉，6-12替换成西瓜
        第二列：只替换-3到0成苹果其他1-12还是数字
        第三列：【1-12里】5，8，12，替换成梨。1-4and6-7and9-11替换成桃。【-3-0】替换成桃
Change History:


"""
import pandas as pd


def row_parse(row_index, data):
    data = str(data)
    if row_index == 1:
        if data in ["-3", "-2", "-1", "0"]:
            return "苹果"
        elif data in ["1", "2", "3", "4", "5"]:
            return "香蕉"
        elif data in ["6", "7", "8", "9", "10", "11", "12"]:
            return "西瓜"
        else:
            return data
    elif row_index == 2:
        if data in ["-3", "-2", "-1", "0"]:
            return "苹果"
        else:
            return data
    elif row_index == 3:
        if data in ["-3", "-2", "-1", "0"]:
            return "桃"
        elif data in ["1", "2", "3", "4", "6", "7", "9", "10", "11"]:
            return "香蕉"
        elif data in ["5", "8", "12"]:
            return "梨"
        else:
            return data


def main():
    names = ["A1", "A2", "A3"]
    df = pd.read_excel(re_value_excel, header=None, names=names)
    for i, name in enumerate(names):
        df[name] = df[name].apply(lambda x: row_parse(i+1, x))

    df.to_excel(result_excel, encoding='utf-8', index=False, header=None)


if __name__ == '__main__':
    # 表
    re_value_excel = '../../EthanFileData/修改列值.xlsx'
    # 生成表
    result_excel = 'Result_data.xlsx'

    main()
