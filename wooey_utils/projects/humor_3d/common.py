# -*- coding: UTF-8 -*-

'''
Author: Henry Wang
Date: 2022-06-23 13:49
Short Description:

Change History:

'''
import requests
import json
from copy import deepcopy

'''
front_middle_camera   VS   front_middle_camera
rear_middle_camera    VS   rear_middle_camera
front_left_camera         VS   lf_wide_camera
rear_left_camera          VS   lr_wide_camera
front_right_camera       VS   rf_wide_camera
rear_right_camera        VS   rr_wide_camera
'''
humor_camera_map = {
    "front_middle_camera": "front_middle_camera",
    "rear_middle_camera": "rear_middle_camera",
    "lf_wide_camera": "front_left_camera",
    "rr_wide_camera": "rear_right_camera",
    "rf_wide_camera": "front_right_camera",
    "lr_wide_camera": "rear_left_camera",

    ### addition
    "front_left_camera" :"lf_wide_camera",
    "rear_right_camera" :"rr_wide_camera",
    "front_right_camera":"rf_wide_camera",
    "rear_left_camera":"lr_wide_camera"
}


def remove_key_if_exists(d: dict, rm_list: list):
    new_dict = { k:v  for k,v in d.items() if k not in rm_list}
    return new_dict

def get_data_from_dict_by_name_lst(d,name_lst):
    for name in name_lst:
        if d.get(name):
            return d.get(name)
    raise Exception("key error",name_lst)


def humor_remove_base_key(info_dict,add_remove_key_lst=None):
    base_remove_key_lst = ["producer", "objects"]
    if add_remove_key_lst is not None:
        base_remove_key_lst.extend(add_remove_key_lst)
    info_dict = remove_key_if_exists(info_dict, base_remove_key_lst)
    return info_dict


#### 原样返回数据
def get_addtion_info_auto(info_dict,add_remove_key_lst:list=None):
    info_dict = humor_remove_base_key(info_dict,add_remove_key_lst)
    return info_dict

##### 老的数据获取addition info
def get_addtion_info_3d(info_dict,add_remove_key_lst:list=None):
    info_dict = humor_remove_base_key(info_dict, add_remove_key_lst)
    relative_images_data = []
    for cam_obj in info_dict["images"]:
        relative_images_data.append({
            "image_id": cam_obj["uid"],
            "imageUrl":cam_obj["image"],
            "image_json":cam_obj["http"],
            "imgHttp": cam_obj["http"],
            "camere_orientation":get_data_from_dict_by_name_lst(cam_obj,["image_orientation","camera_orientation",]),
        })

    if "point_cloud_uid" in info_dict:
        info_dict["point_cloud_id"] = info_dict["point_cloud_uid"]
        # del info_dict["point_cloud_uid"]
    info_dict["relative_images_data"] = relative_images_data

    return info_dict

# rs = requests.get("https://appen-pe.oss-cn-shanghai.aliyuncs.com/temp/humour-old-v1.json").json()
# print(json.dumps(get_addtion_info_3d(info_dict=rs)))


def get_addtion_info_2d(info_dict,cam_dict,add_remove_key_lst:list=None):
    relative_sensors_data = []
    relative_sensors_data.append({
        "point_cloud_id": get_data_from_dict_by_name_lst(info_dict,["point_cloud_id","point_cloud_uid"]),
        "point_cloud_url": info_dict["point_cloud_Url"],
        "point_cloud_json": info_dict["point_cloud_http"],
        "lidar_orientation":info_dict["lidar_orientation"],
    })
    for cam_obj in info_dict["images"]:
        relative_sensors_data.append({
            "image_id": cam_obj["uid"],
            "imageUrl":cam_obj["image"],
            "image_json":cam_obj["http"],
            "imgHttp": cam_obj["http"],
            "camere_orientation":get_data_from_dict_by_name_lst(cam_obj,["image_orientation","camera_orientation",]),
        })


    ###先去掉可能重复的字段,所有原来文件中去掉点云相关的字段
    if add_remove_key_lst is None:
        add_remove_key_lst = []
    info_dict = humor_remove_base_key(info_dict, ["point_cloud_uid","point_cloud_id","point_cloud_Url","point_cloud_http","timestamp", # 这个是点云的timestamp
                                                  "camera_type","camera_orientation","width","height",
                                                 "lidar_type","lidar_orientation",
                                                 "objects","relative_sensors_data"] + add_remove_key_lst)
    #### cam_dict处理
    cam_dict = humor_remove_base_key(cam_dict)
    if "image_id" not in cam_dict:
        cam_dict["image_id"] = cam_dict["uid"]
        del cam_dict["uid"]
    if "imgUrl" not in cam_dict:
        cam_dict["imgUrl"]  = cam_dict["image"]
        del cam_dict["image"]
    if "imgHttp" not in cam_dict:
        cam_dict["imgHttp"] = cam_dict["http"]
        del cam_dict["http"]
    ### 把剩余的字段
    info_dict = {**cam_dict,**info_dict}
    info_dict["relative_sensors_data"] = relative_sensors_data

    return info_dict



# rs = requests.get("https://appen-pe.oss-cn-shanghai.aliyuncs.com/temp/humour-old-v1.json").json()
# print(json.dumps(get_addtion_info_2d(info_dict=rs,cam_dict=rs["images"][0])))



#### 新的数据获取addtion info
def get_addtion_info_3d_new(info_dict,add_remove_key_lst:list=None):
    info_dict = humor_remove_base_key(info_dict,add_remove_key_lst)
    relative_images_data = []
    for image in info_dict["camera"]:
        data = {
            "image_id": image["uid"],
            "imgUrl": image["oss_path"],
            "imgHttp": image["http_path"],
            "camera_orientation": image["name"],
            "image_json": image["oss_path"]
        }
        relative_images_data.append(data)

    lidar_lst = info_dict["lidar"]
    for obj in lidar_lst:
        if obj["name"] == "center_128_lidar_scan_data":
            center_128_lidar_scan_data = obj
            break
    add_info = dict()
    # add_info["point_cloud_id"] = info_dict["lidar_merge"][0]["source"][0]
    # add_info["point_cloud_Url"] = info_dict["lidar_merge"][0]["oss_path_pcd_bin"]
    add_info["point_cloud_id"] = center_128_lidar_scan_data["uid"]
    add_info["point_cloud_Url"] = center_128_lidar_scan_data["oss_path_pcd_bin"]
    add_info["lidar_type"] = info_dict["trigger_name"]
    # add_info["lidar_orientation"] = info_dict["lidar_merge"][0]["name"]
    add_info["lidar_orientation"] = info_dict["trigger_name"]
    add_info["calibration_file"] = info_dict["hardware_config_path"]
    add_info["calibration_file_http"] = info_dict["hardware_config_http_path"]
    add_info["timestamp"]  = info_dict["stamp"]
    add_info["relative_images_data"] = relative_images_data


    info_dict = {**add_info,**info_dict}

    return info_dict

# rs = requests.get("https://appen-pe.oss-cn-shanghai.aliyuncs.com/temp/humor-json-new-v1.json").json()
# print(json.dumps(get_addtion_info_3d_new(info_dict=rs)))


def get_addtion_info_2d_new(info_dict,cam_dict,add_remove_key_lst:list=None):
    info_dict = humor_remove_base_key(info_dict,add_remove_key_lst)
    relative_sensors_data = []
    lidar_lst = info_dict["lidar"]
    for obj in lidar_lst:
        if obj["name"] == "center_128_lidar_scan_data":
            center_128_lidar_scan_data = obj
            break
    relative_sensors_data.append(
        {
            # "point_cloud_id":info_dict["lidar_merge"][0]["source"][0],
            # "point_cloud_url":info_dict["lidar_merge"][0]["oss_path_pcd_bin"],
            # "point_cloud_json":info_dict["lidar_merge"][0]["oss_path_pcd_txt"],
            "point_cloud_id":center_128_lidar_scan_data["uid"],
            "point_cloud_url":center_128_lidar_scan_data["oss_path_pcd_bin"],
            "point_cloud_json":center_128_lidar_scan_data["oss_path_pcd_txt"],
            "lidar_orientation":info_dict["trigger_name"],
        }
    )
    # print(relative_sensors_data)

    if add_remove_key_lst is None:
        add_remove_key_lst = []
    info_dict = humor_remove_base_key(info_dict, ["point_cloud_uid","point_cloud_id","point_cloud_Url","point_cloud_http","timestamp",# 这个是3d的 timestamp
                                                  "camera_type","camera_orientation","width","height",
                                                 "lidar_type","lidar_orientation",
                                                 "objects","relative_sensors_data"] + add_remove_key_lst)
    #### cam_dict处理
    cam_dict = humor_remove_base_key(cam_dict)
    if "image_id" not in cam_dict:
        cam_dict["image_id"] = cam_dict["uid"]
        del cam_dict["uid"]
    if "imgUrl" not in cam_dict:
        cam_dict["imgUrl"]  = cam_dict["oss_path"]
        del cam_dict["oss_path"]
    if "imgHttp" not in cam_dict:
        cam_dict["imgHttp"] = cam_dict["http_path"]
        cam_dict["camera_type"] = cam_dict["http_path"]
        del cam_dict["http_path"]
    if "camera_orientation" not in cam_dict:
        cam_dict["camera_orientation"] = cam_dict["name"]
        del cam_dict["name"]

    if "timestamp" not in cam_dict:
        cam_dict["timestamp"] = cam_dict["stamp"]
        del cam_dict["stamp"]

    info_dict = {**cam_dict,**info_dict}
    info_dict["relative_sensors_data"] = relative_sensors_data
    return info_dict


# rs = requests.get("https://appen-pe.oss-cn-shanghai.aliyuncs.com/temp/humor-json-new-v1.json").json()
# print(json.dumps(get_addtion_info_2d_new(info_dict=rs,cam_dict=rs["camera"][0])))
