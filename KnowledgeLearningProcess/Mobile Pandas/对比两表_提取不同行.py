# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/9/6 17:32

input: 

output: 

Short Description: 

Change History:
    
"""
import pandas as pd


def main():
    # 读取 '表1.xlsx' 单列(Series)，转为list
    df1 = pd.read_excel(xlsx1_path)
    base_data = df1['学号'].tolist()
    # 读取 '表2.xlsx'
    df2 = pd.read_excel(xlsx2_path)

    all_row = list()
    for _, row in df2.iterrows():
        if row['学号'] not in base_data:
            all_row.append(row.tolist())
    df = pd.DataFrame(all_row, columns=[col for col in df2.columns.values])
    df.to_excel(xlsx3_path, encoding="utf-8", index=False)


if __name__ == '__main__':
    xlsx1_path = r'../../EthanFileData/表1.xlsx'
    xlsx2_path = r'../../EthanFileData/表2.xlsx'
    xlsx3_path = r'../../EthanFileData/表3.xlsx'
    main()
