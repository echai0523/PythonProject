# -*- coding: UTF-8 -*-

'''
Author: Simon Wang
Date: 20210604
Short Description:
    毫末视觉红绿灯
Change History:


{
    "producer": "Appen",
    "imgUrl": "CARID_20201031163145/image/lf_wide_camera/1604133320666350.jpg",
    "camera_type": "sensing-AR0231",
    "camera_orientation": "front_wide_camera",
    "width": 1920,
    "height": 1080,
    "objects": [
        {
            "id": "xxxx",
            "className": "TL_Normal",
            "bbox": [
                "x_min",
                "y_min",
                "w",
                "h"
            ],
            "truncation": 0,
            "shelter": 0,
            "split": [
                [
                    "xmin",
                    "ymin",
                    "xmax",
                    "ymax"
                ],
                [
                    "xmin",
                    "ymin",
                    "xmax",
                    "ymax"
                ]
            ],
            "child_num": 3,
            "orientation": 0,
            "sub_light": [
                {
                    "index": 0,
                    "color": "Red",
                    "shape": "Circle"
                },
                {
                    "index": 1,
                    "color": "Dark",
                    "shape": "Unknown"
                },
                {
                    "index": 2,
                    "color": "Dark",
                    "shape": "Unknown"
                }
            ]
        }
    ]
}


Plan:
1. 需要和周林沟通，确认上传下来的CSV格式，因为现在做的是老版和新版 不确定 需要确定下
Checking:
1. 一个group_id分组内只能有一个拉框
2. 一个group_id分组内分割线数量应比红绿灯数量child_num少一个
3. 检测用户画的线必须得是直的横线（Y轴相同）或者直的竖线（X轴相同）

Thinking:
 1. 获取所有的objects内容，保存为objects_list
 2. 生成以group_id为key，groups为value的group_dict
 2. 给objects_list按group_id分组，保存为list[dict], group_id为key
 3. 循环生成的group_id的分组，在group_dict下通过group_id找到对应group下values所有属性，
 4. 生成一个个json文件
'''
from itertools import groupby
from operator import itemgetter

import requests

from wooey_utils.projects.haomo_2d.check.check_haomo_2d_visual_obstacle import get_image_json_info_from_db
from wooey_utils.projects.haomo_2d.haomo_2d import remove_key_if_exists


class CheckConfig:
    tag_dict = {
        "红绿灯": "红绿灯"
    }


class ErrorMessageLog:
    def __init__(self, group):
        self.group = group
        self.error_list = []

    def create_error(self, error_msg, obj):
        if obj is not None:
            classname = obj["className"]
            group_num = self.group[obj["group"]]["num"]
            obj_shape = obj["shape"]
            obj_num = obj["num"]
        else:
            classname = ''
            group_num = ''
            obj_shape = ''
            obj_num = ''
        self.error_list.append(f"DATA:{classname} {group_num} {obj_shape} {obj_num} ERROR:{error_msg}")

    def create_error_group(self, error_msg, group_obj):
        if group_obj is not None:
            classname = group_obj["className"]
            group_num = group_obj["num"]
        else:
            classname = ''
            group_num = ''
        self.error_list.append(f"DATA:{classname} {group_num} ERROR:{error_msg}")


class SINGEL_ROW_PROCESS:
    def __init__(self, json_url, row_dict):
        self.json_result = requests.get(json_url).json()
        self.row_dict = row_dict

        self.groups = self.json_result["json"][0]["groups"]
        self.group_dict = self.get_group_maps()
        self.obj_list = sorted(self.json_result['json'][0]["objects"], key=itemgetter('group'))
        self.group_by_objects_dict = self.get_group_by_objects_dict()

        self.log = ErrorMessageLog(group=self.group_dict)  # 这行数据的所有错误

    def get_group_maps(self):
        group_dict = dict()
        for item in self.json_result['json'][0]["groups"]:
            group_dict[item["id"]] = item
        return group_dict

    @staticmethod
    def cal_bbox_by_polygon(polygon):
        # 第一点和第三个点计算x, y, w, h
        x = max(polygon[0]['x'], 0)
        y = max(polygon[0]['y'], 0)
        bbox = [
            round(x, 13),
            round(y, 13),
            round(polygon[2]['x'] - x, 13),
            round(polygon[2]['y'] - y, 13)
        ]
        assert all([x >= 0 for x in bbox]) is True, f"bbox四点坐标有错误{bbox}"
        return bbox

    def check_row_func(self):
        # Checking:
        # 一个group_id分组内只能有一个拉框
        # 一个group_id分组内分割线数量应比红绿灯数量child_num少一个
        # 检测用户画的线必须得是直的横线（Y轴相同）或者直的竖线（X轴相同）

        for group_id, single_group_dict in self.group_dict.items():

            values = single_group_dict["values"]
            orientation = values["orientation"]
            after_group_by_objects_list = self.group_by_objects_dict[group_id]
            after_group_by_shape_list = self.get_group_by_shape_dict(after_group_by_objects_list)
            rectangle_list = after_group_by_shape_list.get("rectangle", [])
            if len(rectangle_list) != 1:
                self.log.create_error_group("同一个分组下拉了不止一个框或者没画框", single_group_dict)
            line_list = after_group_by_shape_list.get("line", [])
            child_num = values["child_num"]

            ### 线的数量检查
            # if child_num - 1 != len(line_list):
            #     self.log.create_error_group("分组下线的数量不正确", single_group_dict)

            ### 线的坐标水平和垂直检查
            if child_num > 1:
                for single_line in line_list:
                    polygon = single_line["polygon"]
                    x1, y1, x2, y2 = polygon[0]["x"], polygon[0]["y"], polygon[1]["x"], polygon[1]["y"]
                    if x1 == x2 and y1 == y2:
                        self.log.create_error_group("发现两个点坐标相同", single_group_dict)
                    # 判断画线 是X轴相等 还是Y轴相等，就是判断用户是横着画的，还是竖着画的
                    if orientation == 0 and x1 != x2:
                        self.log.create_error_group("同一个分组下选择了横向红绿灯，X轴非垂直线", single_group_dict)
                    if orientation == 1 and y1 != y2:
                        self.log.create_error_group("同一个分组下选择了竖向红绿灯，Y轴非水平线", single_group_dict)

        return self.log.error_list

    def get_group_by_objects_dict(self):
        return {group: list(items) for group, items in groupby(self.obj_list, key=itemgetter("group"))}

    @staticmethod
    def get_group_by_shape_dict(after_group_by_objects_list):
        after_group_by_objects_list.sort(key=itemgetter('shape'))
        return {group: list(items) for group, items in groupby(after_group_by_objects_list, key=itemgetter("shape"))}

    def parse_row_func(self):
        objects = []

        if self.row_dict.get("image_json_url") is not None:
            info_dict = requests.get(self.row_dict["image_json_url"]).json()
        else:
            info_dict = get_image_json_info_from_db(self.row_dict["imgUrl"])

        addition_info = remove_key_if_exists(info_dict, ["producer", "objects"])  ## 删除可能覆盖重要结果的字段

        single_result = {
            "producer": "Appen",  # 该属性为标注供应商公司名称
            "imgUrl": addition_info["imgUrl"],  # 毫末提供的oss路径，保持不变
            "imgHttp": addition_info["imgHttp"],
            "camera_type": "sensing-AR0231" if addition_info.get("camera_type") is None else addition_info.get(
                "camera_type"),  # 相机型号，广角图片全部都是sensing-AR0231
            "timestamp": "999900000" if addition_info.get("timestamp") is None else addition_info.get("timestamp"),
            "camera_orientation": "front_wide_camera" if addition_info.get(
                "camera_orientation") is None else addition_info.get("camera_orientation"),
            "width": self.json_result["json"][0]["width"] if addition_info.get("width") is None else addition_info.get(
                "width"),
            "height": self.json_result["json"][0]["height"] if addition_info.get(
                "height") is None else addition_info.get("height"),  # 图像的像素信息
            "objects": objects,
            **addition_info
        }

        i = 0
        for group_id, single_group_dict in self.group_dict.items():

            values = single_group_dict["values"]
            after_group_by_objects_list = self.group_by_objects_dict[group_id]
            after_group_by_shape_list = self.get_group_by_shape_dict(after_group_by_objects_list)
            rectangle_list = after_group_by_shape_list["rectangle"]
            line_list = after_group_by_shape_list.get("line")
            single_rectangle_dict = rectangle_list[0]
            split = []
            if not line_list:
                pass
            else:
                # 生成存在线段情况下split字段内的值
                for single_line in line_list:
                    if not single_line:
                        break

                    polygon = single_line["polygon"]
                    x1, y1, x2, y2 = polygon[0]["x"], polygon[0]["y"], polygon[1]["x"], polygon[1]["y"]
                    # 判断画线 是X轴相等 还是Y轴相等，就是判断用户是横着画的，还是竖着画的
                    # 这块需要和周林沟通下 再决定
                    if x1 == x2:  ### 竖线
                        # 判断用户画线的方向
                        if y1 > y2:  # 从上往下边画
                            split.append([x2, y2, x1, y1])
                        elif y1 < y2:  # 从下往上边画
                            split.append([x1, y1, x2, y2])
                        else:
                            raise Exception("x和y坐标都相等")

                    elif y1 == y2:  ### 横线
                        if x1 > x2:  # 从右往左边画
                            split.append([x2, y2, x1, y1])
                        elif x1 < x2:  # 从左往右边画
                            split.append([x1, y1, x2, y2])
                        else:
                            raise Exception("x和y坐标都相等")
                    else:
                        self.log.create_error("同一个分组下画的线不是直线，请检查，然后使用快捷键重画", obj=single_group_dict)

            child_num = values["child_num"]
            light_color_list = [f"light_color_{i + 1}" for i in range(child_num)]
            light_shape_list = [f"light_shape_{i + 1}" for i in range(child_num)]

            sub_light = []
            for index, light_color in enumerate(light_color_list):
                sub_light.append({
                    "index": index,
                    "color": values[light_color],
                    "shape": values[light_shape_list[index]]
                })

            objects.append(
                {
                    "id": i,
                    "className": values["traffic_light_position"],
                    "bbox": self.cal_bbox_by_polygon(single_rectangle_dict["polygon"]),
                    "truncation": values["truncation"],
                    "shelter": values["shelter"],
                    "split": split,
                    "child_num": child_num,
                    "orientation": values["orientation"],
                    "sub_light": sub_light
                }
            )

            i += 1

        return single_result


if __name__ == "__main__":
    h = SINGEL_ROW_PROCESS(
        "https://oss-prd.appen.com.cn:9001/tool-prod/5e8f26b4-b1b8-4603-b81f-1faf5cf408f8/5e8f26b4-b1b8-4603-b81f-1faf5cf408f8.CMCbTRAA_2021-06-04T063514Z.1.ed78eaef-ace0-4fd0-b8c7-c4560b930e0c.json",
        {
            "imgUrl": 'ab',
            "imgHttp": 'dd'
        }
    )
    h.check_row_func()
