# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/19 9:18

input:
    - 表1的路径：eg: [JP_CQ_2022_W16.xlsx](https://pan.baidu.com/s/1ltiPROzQvF_9oKuHkOod3Q?pwd=icpy)
    - 表2的路径：eg: [ASIN-Vendor+pairs+exclusions_30_May.xlsx](https://pan.baidu.com/s/1VYfsoIJ2kUyoAm4VfYbdaw?pwd=icpy)
    - 表3的路径：eg: ROOS_Carton+Quantity.xlsx
output: 
Short Description:
    - 知识点：
        - apply()
    - 需求：
        - 表1中某一行  如果D列的值  在表2的D列中存在  就把D列的这个值   放在AC列
        - 表1中某一行  如果W列的值  在表2的F列中存在  就把W列的这个值   放在AD列
        - 如果表1中的AC和AD 都有值 就在AE列写上“value didn't get through”
        - 将3所述的数据   放进表3   表3的ABCDE列分别对应表1的 WWDIM列
Change History:

"""
import pandas as pd
from collections import defaultdict


def ac_ad_to_ae(ac, ad):
    if ac and ad:
        return "value didn't get through"
    else:
        return None


def main():
    # 1.由于要判断是否在表2中某列存在，先把表2的部分列生成list数据
    df2 = pd.read_excel(excel2_path)
    df2_D = [d for d in df2['asin']]
    df2_F = [f for f in df2['parent_vendor_code']]

    # 2.读取表1，使用apply逐行判断表1'值'是否在表2'列_list'中存在
    df1 = pd.read_excel(excel1_path)
    df1["ASIN"] = df1['asin'].apply(lambda x: x if x in df2_D else None)
    df1["Vendor"] = df1['parent_vendor_code'].apply(lambda x: x if x in df2_F else None)
    # 3.使用函数ac_ad_to_ae判断AC and AD列是否同时有值，有值则AE写入"value didn't get through"
    df1["Didn't get through"] = df1.apply(lambda x: ac_ad_to_ae(x.ASIN, x.Vendor), axis=1)

    # 4.将标注完成的表1保存
    df1.to_excel(excel2_save_path, index=False, encoding='utf-8-sig')

    # 5.根据判断表1的AE列是否为"value didn't get through"，将不为"value didn't get through"的行中某5列抽取并写入表3并保持
    excel_3_abcde = defaultdict(list)
    for _, row in df1.iterrows():
        if row["Didn't get through"] != "value didn't get through":
            excel_3_abcde['Key'].append(row['parent_vendor_code'])
            excel_3_abcde['Vendor Code'].append(row['parent_vendor_code'])
            excel_3_abcde['ASIN'].append(row['asin'])
            excel_3_abcde['調整前の発注カートン数'].append(row['old_cq'])
            excel_3_abcde['調整後の発注カートン数'].append(row['new_cq'])
    df3 = pd.DataFrame(excel_3_abcde)
    df3.to_excel(excel3_path, index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    # 表1路径
    excel1_path = r'../../../Ethan_File_Data/JP_CQ_2022_W16.xlsx'
    # 表2路径
    excel2_path = r'../../../Ethan_File_Data/ASIN-Vendor+pairs+exclusions_30_May.xlsx'
    # 表2标注完后，另存的路径，避免覆盖表2原表
    excel2_save_path = r'ASIN-Vendor+pairs+exclusions_30_May_Result.xlsx'
    # 空表3路径
    excel3_path = r'ROOS_Carton+Quantity.xlsx'

    main()

