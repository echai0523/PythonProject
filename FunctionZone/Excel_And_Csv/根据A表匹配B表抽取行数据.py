# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/16 20:17

input:
    - 学号表.xlsx (链接: https://pan.baidu.com/s/1WI-WEeoXQSUXxQRzotkyvA?pwd=icpy)
    - 学生信息表.xlsx (链接: https://pan.baidu.com/s/1g_UbW46QVLcmjImJTt8mjA?pwd=icpy)
output:
    - Result_学生信息表.xlsx
Short Description: 
    - 知识点：
        - pd.read_excel(header=None, names=["学号"])
        - Series.tolist()
        - pd.concat(df_list)
    - 需求：
        根据'学号表'的学号匹配'学生信息表'中学号相同的学生信息并抽取处理
Change History:

"""
import pandas as pd


def main():
    # 读取 '学号表.xlsx' 单列(Series)，转为list
    num_df = pd.read_excel(base_path, header=None, names=["学号"])
    num_list = num_df["学号"].tolist()
    # 读取 '学生信息表.xlsx'
    info_df = pd.read_excel(info_path)
    # 列表推导式，遍历抽取info_df中学号符合的行，构造DataFrame_list
    df_list = [info_df[info_df["学号"] == num] for num in num_list]
    # pandas.concat()将多个DataFrame_list合并
    result_df = pd.concat(df_list)
    # 保存
    result_df.to_excel(out_path, encoding="utf-8", index=False)


if __name__ == '__main__':
    base_path = '../../EthanFileData/学号表.xlsx'
    info_path = '../../EthanFileData/学生信息表.xlsx'
    out_path = "Result_学生信息表.xlsx"

    main()
