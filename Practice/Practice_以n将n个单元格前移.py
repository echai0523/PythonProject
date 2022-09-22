# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/31 13:54

input: 

output: 

Short Description: 

Change History:
    
"""
import pandas as pd


def main():
    df = pd.read_excel("Practice_1.xlsx", header=None)
    result = list()
    for index, row in df.iterrows():
        lst = row.tolist()
        for i in range(int(row[0])):
            lst[i + 1] = lst[i + 4]
            lst[i + 4] = None
        result.append(lst)

    df1 = pd.DataFrame(result)
    df1.to_excel("Practice_to_1.xlsx", index=False, header=False, encoding='utf-8')


if __name__ == '__main__':
    main()
