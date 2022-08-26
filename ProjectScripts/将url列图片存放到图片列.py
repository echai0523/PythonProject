# -*- coding: UTF-8 -*-
"""
Author: Ethan Chai
Date: 2022/7/22 16:29

input: 
output: 
Short Description: 

Change History:

"""
import os
import requests
import xlsxwriter
from PIL import Image
import pandas as pd


# 要固定图片的大小，插入图片的那个单元格的大小也得调整
image_width = 120
image_height = 160

img_df = pd.read_excel("data.xlsx")
workbook = xlsxwriter.Workbook('data.xlsx')
sheet = workbook.add_worksheet()
# 定义一下两列的name,再把要匹配的昵称填充进去。
sheet.write("A1", "image_url")
sheet.write("B1", "image")
base_path = r"C:\Users\echai\UserProject\Ethan_File_Data"
for index, row in img_df.iterrows():
    img_url = row['image_url']
    res = requests.get(img_url).content

    image_path = os.path.join(base_path, os.path.basename(img_url))
    row['img'] = requests.get(img_url).content
    with open(image_path, 'wb') as f:
        f.write(res)

    x_scale = image_width / (Image.open(image_path).size[0])  # 固定宽度/要插入的原始图片宽
    y_scale = image_height / (Image.open(image_path).size[1])  # 固定高度/要插入的原始图片高
    sheet.set_column("A:A", len(img_url))  # 设置A单元格列宽
    sheet.set_column("B:B", 20)  # 设置B单元格列宽
    sheet.set_row(index + 1, 160)  # 设置行高
    sheet.write(f"A{index + 2}", img_url)
    sheet.insert_image(f"B{index + 2}", image_path, {"x_scale": x_scale, "y_scale": y_scale, "x_offset": 15, "y_offset": 20},)  # 设置一下x_offset和y_offset让图片尽量居中

workbook.close()



