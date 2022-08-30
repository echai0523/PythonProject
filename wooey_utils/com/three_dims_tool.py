# -*- coding: UTF-8 -*-

'''
Author: Henry Wang
Date: 2021-05-13 12:10
Short Description:

Change History:

'''



'''
Author: Henry Wang
Date: 2021-03-12 17:21
Short Description:

Change History:


通用的生成manifest_json
# format='bin' # bin,bin.v2
'''
import json
import os
import oss2
from wooey_utils.com.config import *
from wooey_utils.com.oss_tool import OSS_API

import sys
'''
todo
- calibration暂时不支持
- 增加支持图片的自定义目录获取
'''

class GEN_Manifest():
    def __init__(self,bucket_name="projecteng"):
        self.bucket_name = bucket_name
        self.bucket = oss2.Bucket(oss2.Auth(OSS_AK, OSS_SK), 'https://oss-cn-shanghai.aliyuncs.com', self.bucket_name)
        self.oss_obj = OSS_API(bucket_name=self.bucket_name)

    # @staticmethod
    def get_oss_file_names(self,oss_path, suffix=None):
        # 只找当前文件夹下的文件
        file_paths = self.oss_obj.list_bucket_current(oss_path,list_type="file",suffix=suffix)
        return [os.path.basename(x) for x in file_paths]

    def get_oss_obj(self,oss_full_path):
        data = self.bucket.get_object(oss_full_path).read()
        return data

    def save_oss_data_by_path(self,oss_full_path, bytes_data):
        dir_path = os.path.dirname(oss_full_path)
        rs = self.bucket.put_object(oss_full_path, bytes_data)
        assert rs.status == 200, "文件上传失败"
        return f'https://{self.bucket_name}.oss-cn-shanghai.aliyuncs.com/{dir_path}'


    @staticmethod
    def join_oss_path(base_dir, *route_list):
        path = os.path.join(base_dir, *route_list)
        if path.endswith("/"):
            return path
        else:
            return path + '/'

    @staticmethod
    def cal_mean_xyz_from_bin(bin_data, group_len):
        # bin_v1是 4个一组
        # bin_v2是 5个一组
        # cal_mean_xyz_from_bin("/Users/hwang2/Downloads/1614562740500000.bin",4)
        import array
        import numpy as np
        # with open(bin_file,'rb') as fileobj:
        dataArray = array.array('f')  # 创建空数组
        dataArray.frombytes(bin_data)  # 加载数据
        assert len(dataArray) % group_len == 0, "点云组数量不匹配"
        mean_x = np.mean([x for idx, x in enumerate(dataArray) if idx % group_len == 0])
        mean_y = np.mean([x for idx, x in enumerate(dataArray) if idx % group_len == 1])
        mean_z = np.mean([x for idx, x in enumerate(dataArray) if idx % group_len == 2])
        # print(mean_x,mean_y,mean_z)
        # 根据下面的方法计算cameraInfo 和origins
        # result['cameraInfo'] = {
        #     "position": {
        #         "x": x,
        #         "y": y - 5,
        #         "z": z + 10
        #     },
        #     "lookAt": {
        #         "x": x,
        #         "y": y + 13,
        #         "z": z
        #     }
        # }
        # result["options"]["origins"] += [{"x": x, "y": y + 13, "z": z}]

        return mean_x, mean_y, mean_z

    def get_auto_mean_rs(self,format,bin_path, bin_file):
        if format == "bin":
            group_len = 4
        elif format == "bin.v2":
            group_len = 5
        else:
            raise Exception("未定义格式")

        bin_data = self.get_oss_obj(os.path.join(bin_path, bin_file))

        mean_x, mean_y, mean_z = self.cal_mean_xyz_from_bin(bin_data, group_len)
        # print(mean_x,mean_y,mean_z)

        # cameraInfo = {
        #         "position": {
        #             "x": mean_x,
        #             "y": mean_y - 5,
        #             "z": mean_z + 10
        #         },
        #         "lookAt": {
        #             "x": mean_x,
        #             "y": mean_y + 13,
        #             "z": mean_z
        #         }
        #     }
        # origins_list = [{"x": mean_x, "y": mean_y + 13, "z": mean_z}]

        cameraInfo = {
                "position": {
                    "x": mean_x,
                    "y": mean_y,
                    "z": mean_z + 10
                },
                "lookAt": {
                    "x": mean_x,
                    "y": mean_y,
                    "z": mean_z
                }
            }
        origins_list = [{"x": mean_x, "y": mean_y, "z": mean_z}]

        return cameraInfo,origins_list ## 后续如果每帧的origin不一样，那么需要遍历后生成，但是比较消耗性能

    def save_common_template(self,save_file_path, format, frames: dict, ground_remove: dict, images: list, cameraInfo=None,
                             origins_list=None, calibration=None,tag="2",lidarToWorld=None,use_radar=False,part_range_lst=None):

        if cameraInfo is None: cameraInfo = {}
        if origins_list is None: origins_list = [{"x": 0, "y": 0, "z": 0}]



        manifest_template = {
            "point": {
                "format": format
            },
            "tag": tag,  # 固定,一般情况下没有用。 但是有一个情况，比如数据改了 但是浏览器还缓存着上次的数据  可以修改下这个 tag 强制刷新下浏览器的缓存
            "frames": frames,
            "groundRemoved": ground_remove,
            "images": images,
            "cameraInfo": cameraInfo,
            "options": {
                "origins": origins_list
            }
        }

        ### 是否有radar
        if use_radar == True:
            manifest_template["options"]["radar"] = use_radar


        ### calibration暂时不支持。没有的时候不要加
        if calibration is not None:
            manifest_template["calibration"] = calibration

        if part_range_lst is not None:
            manifest_template["options"]["range"] = part_range_lst



        if lidarToWorld is not None:
            manifest_template["options"]["lidarToWorld"]=lidarToWorld

        url = self.save_oss_data_by_path(os.path.join(save_file_path, "manifest.json"),
                                    json.dumps(manifest_template, ensure_ascii=False).encode('utf-8'))
        return url


    def gen_mani_fest_main(self,oss_base_dir, bin_folder: list, ground_folder: list, image_folder: dict, format,
                           sort_func=None, max_frames=None, cameraInfo=None, origins_list=None, calibration=None,
                           auto_mean=False,tag="2",limit_bin_files=None,lidarToWorld=None,limit_image_folder=None,use_radar=False,json_folder="json",all_range_lst=None):

        bin_path = self.join_oss_path(oss_base_dir, *bin_folder)
        ground_path = self.join_oss_path(oss_base_dir, *ground_folder)

        if limit_bin_files is None:
            bin_files = sorted(self.get_oss_file_names(bin_path, suffix=f'.{format}'), key=sort_func)
            ground_files = sorted(self.get_oss_file_names(ground_path, suffix=f".{format}"), key=sort_func)

        else:
            bin_files = limit_bin_files
            ground_files = limit_bin_files

        # print(bin_files)

        image_list = []
        if image_folder is None:
            ### 有些场景只有点云，没有图片
            pass
        elif len(image_folder["image_has_dir"]) == 0:
            image_path = self.join_oss_path(oss_base_dir, *image_folder["base_image_dirs"])
            image_files = sorted(self.get_oss_file_names(image_path, suffix=image_folder["image_type"]), key=sort_func)
            image_list.append({"image_path": image_path, "camera":"camera", "image_files": image_files})
        elif isinstance(image_folder["image_has_dir"],list):
            for fd in image_folder["image_has_dir"]:
                image_path = self.join_oss_path(oss_base_dir, *image_folder["base_image_dirs"], fd)
                image_files = sorted(self.get_oss_file_names(image_path, suffix=image_folder["image_type"]),
                                     key=sort_func)
                image_list.append({"image_path": image_path, "camera": fd, "image_files": image_files})
        elif isinstance(image_folder["image_has_dir"],dict):
            ### 如果有传镜头限制，跟镜头限制的排序保持一致
            if limit_image_folder is None:
                for fd,img_lst in image_folder["image_has_dir"].items():
                    image_path = self.join_oss_path(oss_base_dir, *image_folder["base_image_dirs"], fd)
                    image_files = img_lst
                    image_list.append({"image_path": image_path, "camera": fd, "image_files": image_files})
            else:
                for camera in limit_image_folder:
                    image_path = self.join_oss_path(oss_base_dir, *image_folder["base_image_dirs"], camera)
                    image_list.append({"image_path": image_path, "camera": camera, "image_files": image_folder["image_has_dir"][camera]})
            ### 如果有传镜头限制，跟镜头限制的排序保持一致

        else:
            raise Exception("不支持的图像组类型")

        ### 检查数量
        # print(bin_files,ground_files,'kk')
        assert len(bin_files) == len(ground_files), f"点云数量和去地面数量不一致 {bin_files},{ground_files}"
        assert len(bin_files) != 0,"bin文件数量应不等于0"
        if image_folder is not None:
            for item in image_list:
                # print(item)
                # print(bin_files,item["image_files"])
                assert len(item["image_files"]) >= len(bin_files), f"点云数量和图片数量不一致{len(item['image_files'])}, {len(bin_files)}"
                if len(item["image_files"]) > len(bin_files):
                    print("注意图片数量比点云文件数量多，如果确认可忽略此问题","图片:",{len(item['image_files'])}, "点云:",{len(bin_files)},file=sys.stderr)
        ### 检查结束

        json_save_dir = oss_base_dir
        # 注意使用 rstrip为了防止最后一位造成的取basename不正确的问题!!!!
        total_frames = len(bin_files)
        if max_frames is None: max_frames = total_frames  # 全部生成在一个json中
        for i in range(0, total_frames, max_frames):
            start = i
            end = min(i + max_frames, total_frames)

            ## # Henry Wang, 2021-03-23 17:26 Changed:增加根据每组的第一帧计算平均数
            if auto_mean == True:
                bin_file = bin_files[start]# 取到没组的第一个帧
                cameraInfo,origins_list = self.get_auto_mean_rs(format,bin_path, bin_file)

                if cameraInfo is None: cameraInfo =cameraInfo
                if origins_list is None: origins_list=origins_list


            # 注意这里的写法，为了更直观，文件名start+1 !!!!! 注意索引切片还是原来的
            manifest_path = self.join_oss_path(json_save_dir, json_folder,
                                          f'{os.path.basename(oss_base_dir.rstrip("/"))}_{start + 1}_{end}')

            ## 切分数据，并保存
            frames = {"folder": os.path.relpath(bin_path, manifest_path), "data": bin_files[start:end]}
            ground_remove = {"folder": os.path.relpath(ground_path, manifest_path), "data": ground_files[start:end]}
            images = []
            for item in image_list:
                # print(item["image_path"])
                # image_type = item["image_path"].split("/")[-2]
                # bin_file = bin_files[start:end][0].split(".")[0]
                # images.append(
                #     {"folder": os.path.relpath(item["image_path"], manifest_path),
                #      "data":[image_all_dict[bin_file][image_type]] })
                images.append({"folder": os.path.relpath(item["image_path"], manifest_path), "camera":item["camera"],"data": item["image_files"][start:end]})



            ### 计算需要传递的calibration_dict
            if calibration is None:
                calibration_dict = None
            else:
                # image_lst = [{
                #     {
                #         "folder": "fake_folder"
                #         "data": "fake.json"
                #     }
                # }]
                calib_file_lst = []
                for i in range(start, end):
                    frame_items = []
                    for camera in limit_image_folder:
                        frame_items.append(calibration[camera][i])
                    calib_file_lst.append(frame_items)

                clib_json_name = os.path.join(f"/{self.bucket_name}/"+manifest_path, "calib.json")
                os.makedirs(os.path.dirname(clib_json_name), exist_ok=True)
                with open(clib_json_name, 'w', encoding='utf-8') as cf:
                    json.dump(calib_file_lst, cf)

                calibration_dict = {
                    "model": "pinhole",
                    "file": "calib.json",
                    "images": [
                        {
                            "folder": camera,
                            "data": "fake.json"
                        }
                        for camera in limit_image_folder
                    ],
                }
            ### 计算需要传递的calibration end

            #### 计算range
            part_range_lst = None if all_range_lst is None else all_range_lst[start:end]

            url = self.save_common_template(manifest_path, format=format, frames=frames, ground_remove=ground_remove,
                                       images=images, cameraInfo=cameraInfo, origins_list=origins_list,
                                       calibration=calibration_dict,tag=tag,lidarToWorld=lidarToWorld,use_radar=use_radar,part_range_lst=part_range_lst)
            yield url



if __name__=='__main__':
    from oneutils.fileutil import saveCsvData
    from oneutils.textutil import gen_uuid
    m_gen = GEN_Manifest()
    url_gen = m_gen.gen_mani_fest_main(
        oss_base_dir = "HWJ/2022_05_09_first/annotate/2022-01-20-14-02-36-afternoon_inv-1899/for_annotate/",
        bin_folder=["bin_v1"],
        ground_folder =["bin_v1"],
        image_folder={
            "base_image_dirs":["images"], # 多层路径拼接起来
            "image_has_dir":[],#{"temp":["2021-04-03_16-05-24-2.jpg" for x in range(46)]},#["front_wide_camera","left_fisheye_camera","rear_wide_camera","right_fisheye_camera"],# 不能有多层的情况.如果有直接放的图片就是[]
            "image_type":".png"
        },
        format="bin", # bin bin.v2
        sort_func = lambda i:i.split(".")[0],#i, #针对文件名的排序规则，不含路径int(i.split('.')[0])
        max_frames=100,
        cameraInfo=None,
        origins_list=None,#[{"x": 0, "y": 1, "z": 2}],
        calibration=None,
        auto_mean=False,
        tag="2",
        lidarToWorld=None,
        limit_image_folder=None,
        use_radar = False
    )

    saveCsvData(gen_uuid()+".csv",data=[[x] for x in url_gen],header=['base_url'])
