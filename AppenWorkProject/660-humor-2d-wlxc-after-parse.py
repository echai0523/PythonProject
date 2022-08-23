# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/22 16:20

input:
    - .csv
output:
    - .json
Short Description: 
    {
        "producer": '',#该属性为标注供应商公司名称，英文小写
        "timestamp":'',#图片的时间戳，整型(int)
        "imgUid": '',#图片的全局id，字符串
        "imgUrl": ‘’,#图片在数据引擎上oss地址
        "imgHttp":‘’#图片的httpurl
        "camera_type": "sensing-AR0231", #相机型号
        "camera_orientation": "front_middle_camera", #图片所属的相机
        "width": 1920,
        "height": 1080, #图像的像素信息，需要根据实际图像的像素信息填写
        "objects":[
            {
            "id": 0, #障碍物在这帧图片中的唯一id，从0开始编号
            "className": "car", #障碍物类别，英文小写：
            "bbox": [x_min, y_min, w, h], #整体2D框
            "occlusion": 0, #遮挡属性,0/1/2; 如果某些类别不需要标注该属性，则该类别的障碍物中不出现该字段
            "truncation": 0, #截断属性, 0/1; 如果某些类别不需要标注该属性，则该类别的障碍物中不出现该字段
            "crowding": 0, #拥挤属性，0/1/2; 如果某些类别不需要标标注该属性，则该类别的障碍物中不出现该字段
            "group": 0, #group属性，0/1; 如果某些类别不需要标注该属性，则该类别的障碍物中不出现该字段
            "pose": "standing", #行人姿态属性，
            standing/sitting/other; 如果某些类别不需要标注该属性，则该类别的障碍物中不出现该字段
            },
            ......
        ]
    }
Change History:

"""
import os
import sys
import json
import pandas as pd
import numpy as np
from peutils.fileutil import list_files_deep, list_current_file
from peutils.transform.v1.base import get_session
from peutils.transform.v1.img_com.parser import ImgComParse, ImgComDataConfig
from peutils.wooeyutil import WooeyBaseZipHandlerFile
from pprint import pprint


tmp = {
        "轿车": 'car',
        "巴士": 'bus',
        "面包车": 'van',
        "货车": 'truck',
        "物流小车": 'AGV',
        "工程车": 'engineering-vehicle',
        "其它异性车辆": 'othervehicle',
        "骑自行车的骑行者": 'rider-bicycle',
        "骑摩托车的骑行者": 'rider-motorcycle',
        "自行车": 'bicycle',
        "摩托车": 'motorcycle',
        "三轮车": 'tricycle',
        "行人": 'pedestrian',
        "锥桶": 'cone',
        "水马": 'waterfilledbarrier',
        "禁停牌": 'no-parking',
        "施工标志牌": 'construction',
        "遮阳伞": 'parasol',
        "迎宾台": 'security-desk',
        "静态障碍物": 'static',
        "动态障碍物": 'dynamic'
    }


def main(csv_path, data_type):
    session = get_session()
    df = pd.read_csv(csv_path, encoding='utf-8')
    for _, row in df.iterrows():
        img = ImgComParse(url=row["annotation"], config=ImgComDataConfig())

        for frame_index, frame in enumerate(img.frames_lst):
            if data_type == '单帧':
                data_json_url = row["image_json_url"]

            elif data_type == '连续帧':
                data_json_url = row["client_json_url"].split(',')[frame_index]

            else:
                print("请输入正确的帧类型(单帧 or 连续帧)：")

            for frame_item in frame.frame_items:
                pass

            pass


if __name__ == '__main__':
    main(r"C:\Users\echai\Downloads\process\660 humor物流小车2d单连续帧通用\Result_2022-06-17T07_23_20.287920Z.csv")
    # h = WooeyBaseZipHandlerFile("Humor物流小车视觉障碍物2D标注后处理(单、连帧通用)", ".csv", process_func=main)
    # sys.exit(h.main())
