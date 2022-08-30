# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/24 17:18

input:
output: 

Short Description: 
    - 知识点：
        - drop_duplicates函数不配置筛选项，使用默认筛选逻辑
Change History:

"""
import pandas as pd
from peutils.fileutil import list_files_deep


def Drop_Duplicates():
    """去重"""
    df = pd.read_excel(filename)
    print('去重前excel 长度为：', df.shape[0])

    # 去重部分，使用 drop_duplicates 函数
    df_filt = df.drop_duplicates(keep='first')
    print('去重后excel 的长度为：', df_filt.shape[0])
    print('重复数据量为：', df.shape[0] - df_filt.shape[0])

    df_filt.to_excel('excel_filter.xlsx', index=False)
    print('去重完成！')


def Count_Drop_Duplicates():
    """去重查看数量"""
    result_df = pd.read_excel(filename)
    # 5397
    print(result_df.groupby("SampleId").count())
    print(result_df.drop_duplicates(subset='SampleId').shape)
    print(len(set(result_df['SampleId'].values.tolist())))


def Concat():
    """合并多个子表数据"""
    # 遍历所有子表表名
    sheet_name_list = pd.read_excel(filename).sheet_names

    df_list = [pd.read_excel(filename, sheet_name=sheet_name) for sheet_name in sheet_name_list]
    result_df = pd.concat(df_list)
    print(result_df.shape)
    result_df.to_excel("result.xlsx", index=False, encoding="utf-8-sig")


def disrupt_order():
    """打乱行顺序"""
    csv_file_list = list_files_deep(folderpath)
    for csv_file in csv_file_list:
        df = pd.read_csv(csv_file)
        # DataFrame.sample(frac根据百分比取几行数据，1取所有行，0.3取前30%行)打乱行顺序
        df = df.sample(frac=1)
        df.to_csv(csv_file, index=False, encoding="utf-8-sig")


if __name__ == '__main__':
    filename = ""
    folderpath = ""
    # 去重
    Drop_Duplicates()
    # 去重后统计shape
    Count_Drop_Duplicates()
    # 合并
    Concat()
