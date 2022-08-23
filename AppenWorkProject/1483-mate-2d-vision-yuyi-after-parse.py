# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/19 18:00

input:
    - .csv
output:
    - .txt
Short Description:
    - 美团视觉语义分割后处理
Change History:

"""
import os
import sys
import json
from urllib.parse import unquote
import pandas as pd
from peutils.transform.v1.img_com.parser import ImgComParse, ImgComDataConfig
from peutils.wooeyutil import WooeyBaseZipHandlerFile
from pprint import pprint


# "路面坑洼(无水）"右括号必须为中文'）'
CATE_OBJID_MAP = {
    "隔离栏": 248,
    "路沿": 86,
    "可行使区域": 99,
    "步行道": 102,
    "停止线": 8,
    "斑马线": 9,
    "树枝/树叶": 98,
    "低矮植被": 271,
    "水洼/路面结冰": 300,
    "草": 97,
    "可行使区域内的障碍物": 251,
    "交通标志牌": 252,
    "其他隔离物": 250,
    "路面积雪": 302,
    "地面箭头_左转": 310,
    "地面箭头_右转": 311,
    "地面箭头_直行": 312,
    "地面箭头_掉头": 313,
    "地面箭头_其他": 314,
    "施工区域隔离栏": 301,
    "路面坑洼(无水）": 303
}


def main(csv_file_path):
    df = pd.read_csv(csv_file_path)

    img_regions_map = dict()
    img_count = 0
    box_count = 0
    for _, row in df.iterrows():
        img = ImgComParse(url=row["annotation"], config=ImgComDataConfig())

        img_count += len(img.frames_lst)
        regions = list()
        for instance in img.instance_lst:

            for obj in instance.obj_list:
                box_count += 1
                x = list()
                y = list()

                for point in obj.shape['points']:
                    # round()四舍五入后int()取整
                    x.append(int(round(point["x"])))
                    y.append(int(round(point["y"])))

                regions.append({
                    "shape_attributes": {
                        "name": obj.shapeType,
                        "all_points_x": x,
                        "all_points_y": y
                    },
                    "region_attributes": {
                        "object_id": CATE_OBJID_MAP[instance.category],
                        "id": instance.number
                    }
                })
        img_regions_map[f"{unquote(os.path.basename(row['image_url']))}"] = json.dumps({"regions": regions})
        # print(f"{unquote(os.path.basename(row['image_url']))}\t" + json.dumps({"regions": regions}) + '\n')
    filename = f'Mate视觉语义分割_annotation_{img_count}_{box_count}.txt'
    with open(filename, 'w', encoding="utf-8-sig") as WriteFile:
        for key, value in img_regions_map.items():
            WriteFile.write(key + "\t" + value + '\n')


if __name__ == '__main__':
    # main(r"C:\Users\echai\Downloads\process\1483\Result_2022-08-19T03_17_43.572205Z.csv")
    h = WooeyBaseZipHandlerFile('Mate视觉语义分割后处理', '.csv', process_func=main)
    sys.exit(h.main())
