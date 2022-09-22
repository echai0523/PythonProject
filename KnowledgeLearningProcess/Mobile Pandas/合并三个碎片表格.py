# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/9/7 9:44

input: 

output: 

Short Description: 

Change History:
    
"""
import pandas as pd


def main():
    df1 = pd.read_excel(xlsx1_path, header=None)
    df2 = pd.read_excel(xlsx2_path, header=None)
    df3 = pd.read_excel(xlsx3_path)
    result = {
        "名字": df1[0].tolist(),
        "班级": df2[0].tolist(),
        "学号": df3["学号"].tolist(),
        "母亲电话": df3["母亲电话"].tolist(),
        "此处空着1": [None] * len(df3),
        "父亲电话": df3["父亲电话"].tolist(),
        "此处空着2": [None] * len(df3),
    }
    result_df = pd.DataFrame(result)
    result_df.to_excel(result_path, encoding='utf-8', index=False)


if __name__ == '__main__':
    xlsx1_path = r"../EthanFileData/碎片一.xlsx"
    xlsx2_path = r"../EthanFileData/碎片二.xlsx"
    xlsx3_path = r"../EthanFileData/碎片三.xlsx"
    result_path = r"../EthanFileData/最后呈现结果.xlsx"
    main()
