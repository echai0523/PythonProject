# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/17 11:21

input:
    - A表 (链接: https://pan.baidu.com/s/1hyJUgl0qF7T41xmt7WhdTw?pwd=icpy)
    - B表 (链接: https://pan.baidu.com/s/1hKamT7E1Emxy0UNrKI1kQw?pwd=icpy)
output:
    - new_B表
Short Description:
    - 知识点：
        - pd.concat(df_list)
        - sort_values("name")
        - datetime.hour
        - datetime.minuter
    - 需求：
        - 根据A表"name"匹配"B表"并抽取行数据。
Change History:

"""
import pandas as pd


def time_parse():
    # 读取 'A表.xlsx' 单列name(Series)，转为list
    a_df = pd.read_excel(A_xlsx)
    # 若类型为datetime直接用，若为其他类型，需要先转str,再转为datetime，可参考：https://www.jianshu.com/p/041872dea090
    # a_time = pd.DatetimeIndex(a_df['date'])
    a_df['time_count'] = a_df["date"].apply(lambda a_time: a_time.hour * 60 + a_time.minute)


def main():
    # 读取 'A表.xlsx' 单列name(Series)，转为list
    a_df = pd.read_excel(A_xlsx)
    a_name_list = a_df["name"].tolist()
    # 读取 'B表.xlsx'
    b_df = pd.read_excel(B_xlsx)
    # 列表推导式，遍历抽取info_df中学号符合的行，构造DataFrame_list
    df_list = [b_df[b_df["name"] == a_name] for a_name in a_name_list]

    # pandas.concat()将多个DataFrame_list合并
    concat_df = pd.concat(df_list)
    # 拼接到A表
    result_df = pd.concat([a_df, concat_df])
    # 保存
    # result_df.to_excel(out_path, encoding="utf-8", index=False)
    # 排序name
    df_name = result_df.sort_values('name')
    # 保存
    df_name.to_excel(out_path, encoding="utf-8", index=False)


if __name__ == '__main__':
    A_xlsx = "A表.xlsx"
    B_xlsx = "B表.xlsx"
    out_path = "Result_A表.xlsx"

    main()

    # 时间处理不完善
    # time_parse()
