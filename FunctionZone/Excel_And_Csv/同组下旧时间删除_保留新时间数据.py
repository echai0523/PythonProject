# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/18 15:53

input:
    - csv
        - eg:
            df = pd.DataFrame({
                "name": ["a", "b", "c", "c"],
                "nd": ['1', '2', "b", "c"],
                "date": [20201122, 20111205, 20001231, 20151111]
            })
output:
    - csv
Short Description: 
    - 知识点：
        - df.groupby()
            - .groups 以某列分组，该列的值
        - df.groupby().agg({'': max})
            - .values 统计某列的max，该列的max值
        - df[(df['name'] == name) & (df['date'] == date)]
    - 需求：
        - 将同一name下的date旧时间删除，保留新时间数据
Change History:

"""
import pandas as pd


def main():
    df = pd.read_csv(file_path)
    # 根据name分组，并指定date指出最大值max -> 前提：date为int型
    group_names = [k for k in df.groupby('name').groups]
    date_max = [v[0] for v in df.groupby('name').agg({'date': max}).values]

    result_df_list = list()
    for name, date in zip(group_names, date_max):
        result_df_list.append(df[(df['name'] == name) & (df['date'] == date)])

    result_df = pd.concat(result_df_list)

    result_df.to_csv(out_path, encoding='utf-8', index=False)


if __name__ == '__main__':
    file_path = ''
    out_path = ''
    main()
