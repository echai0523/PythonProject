# -*- coding: UTF-8 -*-

'''
Author: Henry Wang
Date: 2021-05-28 12:50
Short Description:


- checklist  check脚本wooey_utils/check/check_vec_line_new.py
1. 整体图像非sepical时候，不能没有线的标注。(接口控制)
2. 线型类别(模版配置，接口双重检查)
车道线： 单实线(Single Solid)，单虚线(Single Dashed)，双实线(Double Solid)，双虚线(Double Dashed)，等等
    - function
    - color
    - 主编号 -5到5。 other -10 选择ohter会有两种情况，一种是other还有一种是车道线不能和临近的车道线形成一条车道，那么编号标注为-10
    - 副编号 主编输入主线的编号，副编号输入当前自己的副编号 +-1 到+-2  当有副编号的时候表示这个是副线 副编号也必须选择，如果是0的时候代表是主线。
    - occlusion_vec
道路边缘线 Physical，estimated，visual
    - 边缘线编号 +-1到+-5     +-10 到+-16等
    - occlusion_edge
    - current

3. function Other的时候主线必须是-10  --OK

4.车道线的主线编号不能重复以下两种情况除外  --OK
- 功能类型为道路分界线的时候忽略重复问题
- Other的时候也忽略重复

5. 不能有选择了副线，副线填写的主编号找不到对应的主线 --还没做

6.道路边缘线编号不能重复  --OK

# Henry Wang, 2021-06-04 17:34 Changed:
- 车道线，如果是+-5和-10不需要检查重复问题
- 道路边缘线 检查编号的时候各个方向允许重复一次编号


# Henry Wang, 2021-07-05 14:17 Changed:
取消道路分界线重复的问题.不允许道路分界线存在重复，更改了规则4。



Change History:

'''
from collections import defaultdict

import requests
from requests.adapters import HTTPAdapter

from wooey_utils.projects.haomo_2d.check.check_haomo_2d_visual_obstacle import get_image_json_info_from_db, \
    remove_key_if_exists

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))


class CHECK_CONFIG_MAP():
    line_class_map = {
        "单实线": "Single_Solid",
        "单虚线": "Single_Dashed",
        "双实线": "Double_Solid",
        "双虚线": "Double_Dashed",
        "左实右虚线": "Double_Mixed_Left",
        "左虚右实线": "Double_Mixed_Right",
        "道路边缘线": "Road_Edge",
        "物理实体分隔线": "Physical",
        "虚拟线": "visual",
        "脑补线": "estimated",
        "动态线": "dynamic"
    }
    edge_line_set = {x for x in line_class_map if x in {"物理实体分隔线", "虚拟线", "脑补线", "动态线"}}
    vech_line_set = line_class_map.keys() - edge_line_set
    special_map = {
        "not_special": 0,
        "sepecial": 1,
    }


# print(CHECK_CONFIG_MAP.edge_line_set)

class ERROR_MSG_LOG():
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


class SINGEL_ROW_PROCESS():
    def __init__(self, json_url, row_dict):
        self.json_row_data = s.get(json_url).json()
        self.row_dict = row_dict

        self.group_dict = self.get_group_maps()
        self.obj_list = [x for x in self.json_row_data['json'][0]["objects"] if
                         x["shape"] == 'line' and len(x["polygon"]) >= 2]

        self.log = ERROR_MSG_LOG(group=self.group_dict)  # 这行数据的所有错误

    def get_group_maps(self):
        group_dict = dict()
        for item in self.json_row_data['json'][0]["groups"]:
            group_dict[item["id"]] = item
        return group_dict

    def check_row_func(self):
        is_special = self.row_dict["is_special"]
        if is_special not in CHECK_CONFIG_MAP.special_map.keys():
            self.log.create_error("sepecial定义错误", obj=None)
        if is_special == 'not_special' and len(self.obj_list) == 0:
            self.log.create_error("not_special的时候，不能没有线", obj=None)

        main_vec_idx_check = set()  ###所有的主线集合
        edge_idx_check = set()
        split_num = 0
        # has_appear_id = []
        for x in self.obj_list:
            if x["className"] in CHECK_CONFIG_MAP.vech_line_set and x["values"].get("function") == 'Road_Boundary' and \
                    x["values"]["DeputyNumber"] == 0:
                # has_appear_id.append(x["values"]["ChiefEditor"])
                split_num += 1
        # split_num = len([x for x in self.obj_list if
        #                  x["className"] in CHECK_CONFIG_MAP.vech_line_set and x["values"].get(
        #                      "function") == 'Road_Boundary'])
        if split_num > 2:
            self.log.create_error("分界线超过两条，请检查", obj=None)

        for obj in self.obj_list:
            if len(obj["polygon"]) == 0:
                continue

            classname = obj["className"]
            obj_shape = obj["shape"]
            values = obj.get("values", None)

            if values == None or values == {}:
                self.log.create_error("属性表单未填写，请检查", obj=obj)

            # 检测object下是否存在空的坐标
            # for single_polygon in obj["polygon"]:
            #     if len(single_polygon) == 0 or not single_polygon:
            #         self.log.create_error("Object下存在空的坐标点，请检查并重画", obj=obj)

            if obj_shape == 'line' and values is not None:
                if classname not in CHECK_CONFIG_MAP.line_class_map.keys():
                    self.log.create_error("属性名不存在字典映射中", obj=obj)

                ### 检查车道线重复
                if classname in CHECK_CONFIG_MAP.vech_line_set:
                    main_idx = values["ChiefEditor"]
                    ### 功能类型是这两个的时候不用检查重复问题 副编号如果不是0的时候，代表是副线
                    if (values["function"] is not None and values["function"] in {"Other", "Parking"}) or main_idx in (
                            5, -5, -10) or values["DeputyNumber"] != 0:
                        pass
                    else:
                        if main_idx in main_vec_idx_check:
                            self.log.create_error(error_msg="车道线编号重复", obj=obj)
                        main_vec_idx_check.add(main_idx)  ###加入main

                    ##检查other -10
                    if values["function"] == 'Other':
                        if main_idx != -10:
                            self.log.create_error("Other的时候，主编号必须是-10", obj=obj)

                ### 道路边缘线的检查
                elif classname in CHECK_CONFIG_MAP.edge_line_set:
                    edge_idx = f'{values["current"]} {values["edge_index"]}'
                    if edge_idx in edge_idx_check:
                        self.log.create_error(error_msg="车道线编号重复", obj=obj)
                    edge_idx_check.add(edge_idx)  ###加edgeidx

        return self.log.error_list

    def cal_edges_objs(self, edge_obj_list):
        edges_list = []
        for obj in edge_obj_list:
            edges_list.append({
                "index": int(obj["values"]["edge_index"]),
                "type": CHECK_CONFIG_MAP.line_class_map[obj["className"]],
                "occlusion": int(obj["values"]["occlusion_edge"]),
                "current": obj["values"]["current"],
                "points": [[p["x"], p["y"]] for p in obj["polygon"]]
            })
        return edges_list

    def cal_vec_objs(self, vec_obj_list):
        lines_list = []

        subline_dict = defaultdict(list)
        ### 构造subline_dict
        for obj in vec_obj_list:
            if obj["values"]["DeputyNumber"] != 0:
                subline_dict[str(obj["values"]["ChiefEditor"])].append({  # 写入到对应的主线的map中
                    "index": int(obj["values"]["DeputyNumber"]),  # 这里是副线自己的编号
                    "type": CHECK_CONFIG_MAP.line_class_map[obj["className"]],
                    "function": obj["values"]["function"],
                    "color": obj["values"]["color"],
                    "occlusion": int(obj["values"]["occlusion_vec"]),
                    "points": [[p["x"], p["y"]] for p in obj["polygon"]]
                })

        #### 构造line_list
        for obj in vec_obj_list:
            if obj["values"]["DeputyNumber"] == 0:
                main_idx = int(obj["values"]["ChiefEditor"])
                subline_list = subline_dict[str(main_idx)]

                parse_obj = {
                    "index": int(obj["values"]["ChiefEditor"]),  # 这里是副线自己的编号
                    "type": CHECK_CONFIG_MAP.line_class_map[obj["className"]],
                    "function": obj["values"]["function"],
                    "color": obj["values"]["color"],
                    "occlusion": int(obj["values"]["occlusion_vec"]),
                    "points": [[p["x"], p["y"]] for p in obj["polygon"]],
                    "has_subline": True if len(subline_list) != 0 else False,
                }
                if len(subline_list) != 0:
                    parse_obj["subline"] = subline_list

                lines_list.append(parse_obj)

        return lines_list

    def parse_row_func(self):
        if self.row_dict.get("image_json_url") is not None:
            info_dict = s.get(self.row_dict["image_json_url"]).json()
        else:
            info_dict = get_image_json_info_from_db(self.row_dict["imgUrl"])

        addition_info = remove_key_if_exists(info_dict, ["producer", "special", "edges", "lines", "objects"])  ## 删除可能覆盖重要结果的字段
        vec_template = {
            "producer": "Appen",
            "imgUrl": addition_info["imgUrl"],
            "imgHttp": addition_info["imgHttp"],
            "camera_type": "sensing-AR0231" if addition_info.get("camera_type") is None else addition_info.get(
                "camera_type"),
            "timestamp": "999900000" if addition_info.get("timestamp") is None else addition_info.get("timestamp"),
            # "timestamp": str(addition_info.get("timestamp", "999900000")),
            "camera_orientation": "front_wide_camera" if addition_info.get(
                "camera_orientation") is None else addition_info.get("camera_orientation"),
            "width": self.json_row_data["json"][0]["width"] if addition_info.get(
                "width") is None else addition_info.get("width"),
            "height": self.json_row_data["json"][0]["height"] if addition_info.get(
                "height") is None else addition_info.get("height"),
            "special": CHECK_CONFIG_MAP.special_map[self.row_dict["is_special"]],
            "edges": [],
            "lines": [],
            **addition_info
        }

        vec_template["edges"] = self.cal_edges_objs(
            [x for x in self.obj_list if x["className"] in CHECK_CONFIG_MAP.edge_line_set])
        vec_template["lines"] = self.cal_vec_objs(
            [x for x in self.obj_list if x["className"] in CHECK_CONFIG_MAP.vech_line_set])

        return vec_template


if __name__ == '__main__':
    h = SINGEL_ROW_PROCESS(
        "https://oss-prd.appen.com.cn:9001/tool-prod/3673a1f9-4a44-458e-8fb4-2d0ff89fcf0f/3673a1f9-4a44-458e-8fb4-2d0ff89fcf0f.CNf0TBCxAQ3d3d_2021-06-04T010808Z.4.0b230bf8-bffb-4143-86b1-37608c092d89.json",
        {
            "is_special": "not_special",
            "imgUrl": 'ab',
            "imgHttp": 'dd'
        }
    )
    error_rs = h.check_row_func()
    print(error_rs)
    # # json_rs = h.parse_row_func()
    # print(json.dumps(json_rs,ensure_ascii=False))
