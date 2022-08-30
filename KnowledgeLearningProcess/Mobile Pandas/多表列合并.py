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
from pathlib import Path


def list_files_deep(path='.', suffix='', not_prefix=(('~', '.'))):
    files = []
    all_files = list(Path(path).glob('**/*.*'))
    if isinstance(suffix,str)==True:
        suffix = suffix.lower()
    elif isinstance(suffix,tuple) ==True:
        suffix = tuple([x.lower() for x in suffix])

    for filpath in all_files:
        if filpath.is_file() ==True and filpath.name.lower().endswith(suffix) and not filpath.name.startswith(not_prefix):
            files.append(filpath.resolve().as_posix())

    return files


def main():
    file_list = list_files_deep(excel_list_folder_path)

    SheetName = '人事'
    left_df = pd.read_excel(file_list[0], sheet_name=SheetName)
    for file in file_list[1:]:
        right_df = pd.read_excel(file, sheet_name=SheetName, thousands=',')
        header = [h for h in right_df.columns.values if h != None or h != "项目" or h != "序号"]
        for h in header:
            left_df[h] = right_df[h]

    left_df.to_excel(r'Result_info.xlsx', index=False, encoding='utf-8', sheet_name=SheetName)


if __name__ == '__main__':
    excel_list_folder_path = r'汇总1'
    main()
