# -*- coding: UTF-8 -*-

'''
Author: Simon Wang
Date: 20210719
Short Description:
Json 格式：
{
    "producer": "haomo",
    "img_url": "CARID_20201031163145/image/lf_wide_camera/1604133320666350.jpg",
    "cam_type": "sensing-AR0231",
    "cam_orientation": "front_wide_camera",
    "width": 1920,
    "height": 1080,
    "period": 0,
    "weather": 0,
    "objects": [
        {
            "id": 0,
            "bbox": [x_min, y_min, w, h],
            "truncation": 0,
            "self_occlusion": 0,
            "ext_occlusion": 0,
            "valid": 0,
            "shape": 0,
            "color": 0,
            "arrow_orientation": 0
        },
        {
            "id": 1,
            "bbox": [x_min, y_min, w, h],
            "truncation": 0,
            "self_occlusion": 0,
            "ext_occlusion": 0,
            "valid": 0,
            "shape": 0,
            "color": 0,
            "arrow_orientation": 0
        }
    ]
}
Change History:

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

        for group_id, single_group_dict in self.group_dict.items():

            after_group_by_objects_list = self.group_by_objects_dict[group_id]
            after_group_by_shape_list = self.get_group_by_shape_dict(after_group_by_objects_list)
            rectangle_list = after_group_by_shape_list.get("rectangle", [])
            if len(rectangle_list) != 1:
                self.log.create_error_group("同一个分组下拉了不止一个框或者没画框", single_group_dict)

        return self.log.error_list

    def get_group_by_objects_dict(self):
        return {group: list(items) for group, items in groupby(self.obj_list, key=itemgetter("group"))}

    @staticmethod
    def get_group_by_shape_dict(after_group_by_objects_list):
        after_group_by_objects_list.sort(key=itemgetter('shape'))
        return {group: list(items) for group, items in groupby(after_group_by_objects_list, key=itemgetter("shape"))}

    def get_matched_object_by_group_id(self, group_id):
        for single_object in self.obj_list:
            if single_object["group"] == group_id:
                return single_object
        raise Exception(f"没有找到匹配的group_id，group_id={group_id}")

    def parse_row_func(self):

        if self.row_dict.get("image_json_url") is not None:
            info_dict = requests.get(self.row_dict["image_json_url"]).json()
        else:
            info_dict = get_image_json_info_from_db(self.row_dict["imgUrl"])

        addition_info = remove_key_if_exists(info_dict, ["producer", "objects"])  ## 删除可能覆盖重要结果的字段
        if isinstance(self.row_dict["weather"], float):
            weather = 0
        else:
            weather = self.row_dict["weather"]
        # weather = 0 if self.row_dict["weather"] is numpy.nan else self.row_dict["weather"]

        single_result = {
            "producer": "Appen",
            "imgUrl": addition_info["imgUrl"],
            "camera_type": "sensing-AR0231" if addition_info.get("camera_type") is None else addition_info.get(
                "camera_type"),
            "camera_orientation": "front_wide_camera" if addition_info.get(
                "camera_orientation") is None else addition_info.get("camera_orientation"),
            "width": self.json_result["json"][0]["width"] if addition_info.get("width") is None else addition_info.get(
                "width"),
            "height": self.json_result["json"][0]["height"] if addition_info.get(
                "height") is None else addition_info.get("height"),
            "timestamp": info_dict["timestamp"],
            "period": self.row_dict["period"],
            "weather": weather,
            "objects": []
        }

        i = 0

        for group_id, single_group_dict in self.group_dict.items():
            values = single_group_dict["values"]
            single_result["objects"].append({
                "id": i,
                "bbox": self.cal_bbox_by_polygon(self.get_matched_object_by_group_id(group_id)["polygon"]),
                "truncation": values["truncation"],
                "self_occlusion": values["self_occlusion"],
                "ext_occlusion": values["ext_occlusion"],
                "valid": values["valid"],
                "shape": values["shape"],
                "color": values["color"],
                "arrow_orientation": 4 if not values.get("arrow_orientation") else values["arrow_orientation"]
                # "toward_orientation": int(values["toward_orientation"])
            })
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
