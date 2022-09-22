# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/9/4 20:13

input: 

output: 

Short Description: 

Change History:
    
"""
import pandas as pd
import re


def main(file_path):
    df = pd.read_excel(file_path)
    # 新增一列"re_评论内容" list形式写入
    # df["re_评论内容"] = df["评论内容"].apply(lambda x: re.findall('[\u4e00-\u9fa5]+', x))
    # 新增一列"re_评论内容" str形式写入
    df["re_评论内容"] = df["评论内容"].apply(lambda x: ''.join(re.findall('[\u4e00-\u9fa5]+', x)))

    # 会覆盖原列"评论内容" list形式写入
    # df["评论内容"] = df["评论内容"].apply(lambda x: re.findall('[\u4e00-\u9fa5]+', x))
    # 会覆盖原列"评论内容" str形式写入
    # df["评论内容"] = df["评论内容"].apply(lambda x: ''.join(re.findall('[\u4e00-\u9fa5]+', x)))

    df.to_excel(file_path, encoding='utf-8', index=False)


if __name__ == '__main__':
    main(r"../EthanFileData/评论1000条.xlsx")
