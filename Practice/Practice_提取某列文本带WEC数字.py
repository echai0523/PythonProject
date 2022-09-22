# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/30 16:30

input: 

output: 

Short Description: 

Change History:
    
"""
import pandas as pd
import re


def main(file_path):

    df = pd.read_excel(file_path)

    out_data = {
        "平台参考号": list(),
        "系统备注": list()
    }
    for index, row in df.iterrows():
        number = row["平台参考号"]
        info = row["系统备注"]

        if "WEC" in info and "拆分" in info:
            # print(f"{index}, 平台参考号: {number}, 系统备注: {info}")
            data_list = re.findall(r"WEC\d+", info)
            if data_list:
                for data in data_list:
                    if data:
                        out_data["平台参考号"].append(number)
                        out_data["系统备注"].append(data)
    out_df = pd.DataFrame(out_data)
    out_df.to_excel("Result.xlsx", encoding='utf-8', index=False)


if __name__ == '__main__':
    main(r"../../EthanFileData/拆分单-ok.xlsx")
