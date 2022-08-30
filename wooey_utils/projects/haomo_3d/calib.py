import json
from typing import List, Dict

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from scipy.spatial.transform import Rotation as R
from scipy import linalg
import numpy as np

# 标定文件   VS    JSON
# front_middle_camera   VS   front_middle_camera
# rear_middle_camera    VS   rear_middle_camera
# front_left_camera         VS   lf_wide_camera
# rear_left_camera          VS   lr_wide_camera
# front_right_camera       VS   rf_wide_camera
# rear_right_camera        VS   rr_wide_camera

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=10))
s.mount('https://', HTTPAdapter(max_retries=10))


def generate_a9_calibration(
        cam_name: str,
        cam_cx: float,
        cam_cy: float,
        cam_fx: float,
        cam_fy: float,
        cam_attitude: List[float],
        cam_translation: List[float],
        lidar_name: str,
        lidar_attitude: List[float],
        lidar_translation: List[float],
        after_process_calibration_data: List[Dict]
):
    """
        attitude有四个值，按x,y,z,w顺序传入
        translation有三个值，按x,y,z顺序传入
    """
    tail_cam_column = np.array(cam_translation)
    tail_lidar_column = np.array(lidar_translation)
    tail_row = np.array([0.0, 0.0, 0.0, 1.0])

    cam_rot = R.from_quat(cam_attitude).as_matrix()
    cam_rot = np.row_stack(
        (
            np.column_stack((cam_rot, tail_cam_column)),
            tail_row
        )
    )

    lidar_rot = R.from_quat(lidar_attitude).as_matrix()
    lidar_rot = np.row_stack(
        (
            np.column_stack((lidar_rot, tail_lidar_column)),
            tail_row
        )
    )

    cam_rot_inv = linalg.inv(cam_rot)
    lidar_rot_inv = linalg.inv(lidar_rot)

    calibration_data = {
        "p": [
            [
                cam_fx, 0.0, cam_cx, 0.0
            ],
            [
                0.0, cam_fy, cam_cy, 0.0
            ],
            [
                0.0, 0.0, 1.0, 0.0
            ]
        ],
        "r": [
            [
                1, 0, 0, 0
            ],
            [
                0, 1, 0, 0
            ],
            [
                0, 0, 1, 0
            ],
            [
                0, 0, 0, 1
            ]
        ],
        "t": []
    }

    mapping_data = [[is_camera_left, is_camera_invert, is_lidar_invert] for is_camera_left in range(2) for
                    is_camera_invert in range(2)
                    for is_lidar_invert in range(2)]

    for single_mapping in mapping_data:
        is_camera_left, is_camera_invert, is_lidar_invert = single_mapping[0], single_mapping[1], single_mapping[2]

        if is_camera_invert == 0:
            camera_data = cam_rot
        if is_camera_invert == 1:
            camera_data = cam_rot_inv

        if is_lidar_invert == 0:
            lidar_data = lidar_rot
        if is_lidar_invert == 1:
            lidar_data = lidar_rot_inv

        if is_camera_left == 0:
            calibration_data["t"] = np.dot(lidar_data, camera_data).tolist()  # noqa
        else:
            calibration_data["t"] = np.dot(camera_data, lidar_data).tolist()  # noqa

        after_process_calibration_data.append({
            "camera_name": cam_name,
            "lidar_name": lidar_name,
            "is_camera_left": is_camera_left,
            "is_camera_invert": is_camera_invert,
            "is_lidar_invert": is_lidar_invert,
            "calibration_json": json.dumps(calibration_data),
        })


def get_json_result(url):
    resp = s.get(url)
    if resp.status_code == 200:
        return resp.json()
    else:
        raise Exception(f"{url}下载失败，请检查")


def clib_main(json_file_path,ft_lidar_name,ft_is_camera_left,ft_is_camera_invert,ft_is_lidar_invert,camera_map,calib_field_name):
    AFTER_PROCESS_CALIBRATION_DATA = []
    with open(json_file_path, mode="r", encoding="utf-8") as f:

        json_obj = json.load(f)

        calibration_json_obj = get_json_result(json_obj[calib_field_name])

        ## 如果有 MIDDLE_LIDAR 用MIDDLE_LIDAR,否则用 FRONT_LIADAR
        og_lidars_list = calibration_json_obj["sensor_config"]["lidar_param"]

        has_middle = False if len([x for x in og_lidars_list if x["name"] == 'MIDDLE_LIDAR']) == 0 else True

        if has_middle == False:
            out_lidars_list = og_lidars_list
        else:
            out_lidars_list = []
            for og_lidar in og_lidars_list:

                if og_lidar["name"] == "FRONT_LIDAR":
                    pass  # 不写入
                elif og_lidar["name"] == "MIDDLE_LIDAR":
                    og_lidar["name"] = "FRONT_LIDAR"
                    out_lidars_list.append(og_lidar)

        # print(out_lidars_list)
        calibration_json_obj["sensor_config"]["lidar_param"] = out_lidars_list
        # print(json.dumps(calibration_json_obj))


        sensor_config = calibration_json_obj["sensor_config"]
        cam_param, lidar_param = sensor_config["cam_param"], sensor_config["lidar_param"]

        lidar_param_dict = [
            {**single_lidar_param["pose"], "name": single_lidar_param["name"]} for single_lidar_param in lidar_param
        ]

        cam_df = pd.DataFrame(cam_param)
        lidar_df = pd.DataFrame(lidar_param_dict)

        for cam_name, cam_cx, cam_cy, cam_fx, cam_fy, cam_pose in zip(
                cam_df["name"],
                cam_df["cx"],
                cam_df["cy"],
                cam_df["fx"],
                cam_df["fy"],
                cam_df["pose"]
        ):
            if cam_pose is np.nan:
                continue

            cam_attitude, cam_translation = cam_pose["attitude"], cam_pose["translation"]

            cam_attitude = [
                cam_attitude.get("x", 0.0),
                cam_attitude.get("y", 0.0),
                cam_attitude.get("z", 0.0),
                cam_attitude.get("w", 0.0)
            ]

            cam_translation = [
                cam_translation.get("x", 0.0),
                cam_translation.get("y", 0.0),
                cam_translation.get("z", 0.0)
            ]

            for lidar_name, lidar_attitude, lidar_translation in zip(
                    lidar_df["name"],
                    lidar_df["attitude"],
                    lidar_df["translation"]
            ):
                lidar_attitude = [
                    lidar_attitude.get("x", 0.0),
                    lidar_attitude.get("y", 0.0),
                    lidar_attitude.get("z", 0.0),
                    lidar_attitude.get("w", 0.0)
                ]

                lidar_translation = [
                    lidar_translation.get("x", 0.0),
                    lidar_translation.get("y", 0.0),
                    lidar_translation.get("z", 0.0)
                ]

                generate_a9_calibration(
                    cam_name,
                    cam_cx,
                    cam_cy,
                    cam_fx,
                    cam_fy,
                    cam_attitude,
                    cam_translation,
                    lidar_name,
                    lidar_attitude,
                    lidar_translation,
                    AFTER_PROCESS_CALIBRATION_DATA
                )

    df = pd.DataFrame(AFTER_PROCESS_CALIBRATION_DATA)
    # df.to_csv("calibration.csv", encoding="utf-8-sig", index=False)
    # print(df.head())
    # print(set(df["camera_name"]))
    # print(df.columns,df.dtypes)
    # print(set(df["lidar_name"]))
    # print(df)

    # pre_filter_df = filter_df.drop_duplicates('camera_name', keep='first')
    # print(set(df["lidar_name"]))


    filter_df = df[
              (df["lidar_name"]== ft_lidar_name) &
              (df["is_camera_left"] == ft_is_camera_left ) &
              (df["is_camera_invert"] == ft_is_camera_invert)&
              (df["is_lidar_invert"] == ft_is_lidar_invert) &
              (df["camera_name"].isin(set(camera_map.keys())))
          ]
    filter_df = filter_df.drop_duplicates('camera_name', keep='first')

    # print(filter_df)
    assert len(filter_df) == len(set(camera_map.keys())),f"{json_file_path} 数量不对等"


    return filter_df

    # pd.DataFrame(AFTER_PROCESS_CALIBRATION_DATA).to_csv("calibration.csv", encoding="utf-8-sig", index=False)  # noqa


if __name__ == "__main__":
    CAMERA_MAP = {
        "front_left_camera": "lf_wide_camera",
        "front_right_camera": "rf_wide_camera"
    }
    # from peutils.fileutil import list_files_deep
    # files = list_files_deep("/Users/hwang2/Desktop/1229-10-test",".json")
    # for fl in files:
    #     filter_df = clib_main(fl,
    #                           "FRONT_LIDAR",
    #                           0, 0, 1, CAMERA_MAP)
        # for _, row in filter_df.iterrows():
        #     pass



    filter_df = clib_main("/Users/hwang2/Downloads/61d97293910d7200e762c544/61d97293910d7200e762c544/1638580949275133.json",
              "FRONT_LIDAR",
              1,1,0,CAMERA_MAP,"calibration_file_http")
    print(filter_df)
    for _,row in filter_df.iterrows():
        # print(row["camera_name"])
        # print(row["camera_name"],row["lidar_name"],row["is_camera_left"],row["is_camera_invert"],row["is_lidar_invert"])
        # print(row["calibration_json"])
        print("====")



    # from peutils.fileutil import list_files_deep
    # from peutils.textutil import  gen_uuid
    # files = list_files_deep("/Users/hwang2/Documents/wooey_rs/e9f3e35c23b74483af2811aef7ecb49f/task_result/test2",suffix=".json")
    #
    # from collections import defaultdict
    # import os
    # map_dict = defaultdict(list)
    # CAMERA_MAP =  {
    #             "front_left_camera":"lf_wide_camera",
    #             "front_right_camera":"rf_wide_camera"
    #         }
    #
    #
    #
    # single_json_dir ="/Users/hwang2/Documents/wooey_rs/e9f3e35c23b74483af2811aef7ecb49f/task_result/uuid"
    #
    # download_task = []
    #
    # for fl in files:
    #     df = clib_main(
    #         # "/Users/hwang2/Documents/wooey_rs/e9f3e35c23b74483af2811aef7ecb49f/task_result/test1/61c98e39194d07b7bc17ce34/1638317628075147.json",
    #         fl,
    #         lidar_name = "FRONT_LIDAR",
    #         is_camera_left=0,
    #         is_camera_invert=0,
    #         is_lidar_invert=1,
    #         camera_map = CAMERA_MAP
    #     )
    #     print(df)
    #     for _,row in df.iterrows():
    #         camera_name = row["camera_name"]  # calib中对应的名称
    #         img_cam_name = CAMERA_MAP[camera_name] # 图像对应的名称
    #
    #         json_name = gen_uuid() + ".json"
    #         out_json_name = os.path.join(single_json_dir,)
    #
    #         download_task.append({
    #             "full_path":  os.path.join(single_json_dir,json_name),
    #             "json_data":row["calibration_json"]
    #         })
    #
    #         map_dict[img_cam_name].append({
    #             "folder": "../../../calibration/FDUUI",
    #             "data": json_name
    #         })
    #
    #     print(download_task)
    #     print(dict(map_dict))
