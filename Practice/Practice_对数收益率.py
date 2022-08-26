# -*- coding: UTF-8 -*-
"""
Author: Ethan Chai
Date: 2022/8/25 17:02

input:
output:

Short Description:
Change History:

"""
import pandas as pd
import numpy as np


def main():
    # 数据：网盘https://pan.baidu.com/s/13o52M-wFhhCNACEp6dL05w 密码96z0
    # 公式: [log(n日的收盘价)-log(n-1日的收盘价)] ** 2
    df_ih = pd.read_csv('IH_main_00.csv', encoding='utf-8')
    print('初始数据\n', df_ih.head())

    df_ih['tradeDate'] = pd.to_datetime(df_ih['tradeDate'])
    df_ih.sort_values(by='tradeDate', ascending=True, inplace=True)

    # # 方法一： 对数收益率 = log(收盘价)-log(前一天收盘价)
    # df_ih['pe_log_1'] = np.log(df_ih['closePrice']) - np.log(df_ih['closePrice'].shift(1))
    # # 方法二：对数收益率 = log(收盘价/前一个收盘价)
    # df_ih['pe_log_2'] = np.log(df_ih['closePrice'] / df_ih['closePrice'].shift(1))

    df_ih['收益率'] = (np.log(df_ih['closePrice']) - np.log(df_ih['closePrice'].shift(1))) ** 2

    print('计算后数据\n', df_ih.head())

    pass
    
    
if __name__ == "__main__":
    main()










