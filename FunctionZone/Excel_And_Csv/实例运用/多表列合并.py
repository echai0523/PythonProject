# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/5 13:07

input:
    - folder：excel表格上一级文件夹，即excel包
output:
    - excel：合并后的表格
"""
import pandas as pd
from peutils.fileutil import list_files_deep


def main():
    file_list = list_files_deep(excel_list_folder_path)

    left_df = pd.read_excel(file_list[0])
    for file in file_list[1:]:
        right_df = pd.read_excel(file, sheet_name='Sheet1')
        header = [h for h in right_df.columns.values if h != None or h != "项目"]
        for h in header:
            left_df[h] = right_df[h]

    left_df.to_excel(r'Result_info.xlsx', index=False)


if __name__ == '__main__':
    excel_list_folder_path = r'excel包'
    main()
