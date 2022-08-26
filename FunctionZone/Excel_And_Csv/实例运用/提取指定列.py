# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/7 10:19

input: 
output: 
Short Description: 

Change History:

"""
import pandas as pd
from peutils.transform.v1.img_com import pre_parser


def main():
    df = pd.read_excel(ExcelPath)
    # XXEJN -> 需要抽取的列名按顺序写入 -> 下面是以Carton+Quantity+-+Operation+Tracking+List_2022的XXEJN5列为例
    result_df = df[['parent_vendor_code', 'parent_vendor_code', 'asin', 'old_cq', 'new_cq']]
    result_df.to_excel(SavePath, index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    # excel路径 -> 需要处理的excel路径，下面是以Carton+Quantity+-+Operation+Tracking+List_2022为例
    ExcelPath = r"Carton+Quantity+-+Operation+Tracking+List_2022.xlsx"
    # 保存路径 -> 将抽取的5列另存为新的表格，下面是以另存为新表格Result为例
    SavePath = r'Result.xlsx'
    main()
