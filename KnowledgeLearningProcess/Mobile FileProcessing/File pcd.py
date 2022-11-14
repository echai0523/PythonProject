# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/9/23 17:41

input:

output:d

Short Description:
    - 读取pcd文件
        point_pcd_result = pcd_py3.PointCloud.from_path(pcd_path)
    - 针对剔除points的情况，pcd头部描述信息需要更新 宽/高/点云数量
        # 用于头部描述，更新最新的宽/高/点云数量，继用原pcd的宽/高/点云数量会导致新pcd无法使用pcd_py3读取
        width = points = 0
        points_str = ""
        for row_pcd_point in points_list:
            x, y, z = row_pcd_point
            # 剔除y<0的点
            if y >= 0:
                width += 1
                points += 1
                new_line = f'{x} {y} {z}'
                points_str += f"{new_line.strip()}\n"

        # pcd头部
        header_string = f"# .PCD v0.7 - Point Cloud Data file format\n" \
                        f"VERSION 0.7\n" \
                        f"FIELDS x y z\n" \
                        f"SIZE 4 4 4\n" \
                        f"TYPE F F F\n" \
                        f"COUNT 1 1 1\n" \
                        f"WIDTH {width}\n" \
                        f"HEIGHT 1\n" \
                        f"VIEWPOINT 0.0 0.0 0.0 1.0 0.0 0.0 0.0\n" \
                        f"POINTS {points}\n" \
                        f"DATA ascii\n"
        # 重写pcd文件
        out_pcd_path = "2021-06-26-15-46-29_c3_x1358_y504_z158_x1358_y504_z155_12.pcd"
        with open(out_pcd_path, 'w') as writefile:
            writefile.write(header_string)
            writefile.write(points_str)
Change History:

"""
import os
import sys
from argparse import ArgumentParser
from urllib.parse import quote
import numpy as np
from peutils import pcd_py3
from peutils.transform.v1.base import get_session
from wooey_utils.com.oss_tool import OSS_API, gen_uuid


class OSSAPI(OSS_API):
    def save_to_oss_url(self, bytes_data, oss_path=None, suffix_type=None, force=False):
        if oss_path is None:
            if suffix_type is None:
                raise Exception("路径不指定的情况，必须指定后缀类型")
            elif suffix_type.startswith(".") == False:
                raise Exception("后缀必须以.结尾")
            else:
                oss_path = f"upload_url/{gen_uuid()}/{gen_uuid()}{suffix_type}"

        # 检查文件是否已存在
        if force == False:
            if self.bucket.object_exists(oss_path) is True:
                print(f"文件{os.path.basename(oss_path)}已存在，现已被覆盖")

        # 写入文件
        rs = self.bucket.put_object(oss_path, bytes_data)
        if rs.status != 200:
            raise Exception("OSS数据写入失败")

        prefix_url = f"https://{self.bucket_name}.oss-cn-shanghai.aliyuncs.com/"
        url = prefix_url + quote(oss_path)
        og_url = prefix_url + oss_path

        return url, og_url


def main():
    assert in_oss_path.startswith("oss://") == True, "请输入以'oss://'开头的oss路径"
    # 去掉"oss://projecteng/"
    in_oss_path_del_bucket = in_oss_path.replace("oss://projecteng/", "")
    # pcd原文件夹路径
    pcd_oss_folder_path = in_oss_path_del_bucket + 'pcd/'
    # pcd处理后输出的文件夹路径
    out_pcd_oss_folder_path = in_oss_path_del_bucket + 'new_pcd/'
    os.makedirs(out_pcd_oss_folder_path, exist_ok=True)

    # pcd文件list
    pcd_file_list = oss_obj.list_bucket_current(pcd_oss_folder_path, list_type="file", suffix="pcd")
    for pcd_file in pcd_file_list:
        # pcd名
        pcd_name = os.path.basename(pcd_file)
        # 输入的pcd
        pcd_oss_path = "/projecteng/" + pcd_file
        # pcd_oss_path = "../../EthanFileData/1659430571904366.pcd"
        # 输出的pcd
        out_pcd_oss_path = "/projecteng/" + out_pcd_oss_folder_path + pcd_name
        # out_pcd_oss_path = "../../EthanFileData/out/1659430571904366.pcd"

        # 读取pcd文件
        point_pcd_result = pcd_py3.PointCloud.from_path(pcd_oss_path)
        # pcd 点
        points_iter = ((p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12]) for p in
                       point_pcd_result.pc_data)
        point_list = np.array(list(points_iter), dtype="float32")
        # pcd头部
        width = point_pcd_result.width
        height = point_pcd_result.height
        points_count = point_pcd_result.points
        # f"FIELDS x y z _ intensity t reflectivity ring _-a2d2d0f9-5644-4b98-8912-4ac9294b5433 ambient _-c4dbb4b6-6090-4c1b-b36b-2787d8faa554 range _-49363681-059b-49ad-8373-28a837b61b41\n" \
        header_string = f"# .PCD v0.7 - Point Cloud Data file format\n" \
                        f"VERSION 0.7\n" \
                        f"FIELDS x y z _ intensity t reflectivity ring _ ambient _ range _\n" \
                        f"SIZE 4 4 4 1 4 4 2 1 1 2 1 4 1\n" \
                        f"TYPE F F F U F U U U U U U U U\n" \
                        f"COUNT 1 1 1 4 1 1 1 1 0 1 0 1 15\n" \
                        f"WIDTH {width}\n" \
                        f"HEIGHT {height}\n" \
                        f"VIEWPOINT 0.0 0.0 0.0 1.0 0.0 0.0 0.0\n" \
                        f"POINTS {points_count}\n" \
                        f"DATA binary\n"
        # 重写pcd文件
        with open(out_pcd_oss_path, 'w') as writefile:
            # 先固定写好头部
            writefile.write(header_string)
            for point_pcd_row in point_list:
                x, y, z, _1, intensity, t, reflectivity, ring, _2, ambient, _3, range_, _4 = point_pcd_row
                if choose_str == "(x,y)->(y,-x)":
                    # 批次14：(x,y)变成(y,-x) oss中对应文件20220922
                    new_line = f'{y} {-x} {z} {_1} {intensity} {t} {reflectivity} {ring} {_2} {ambient} {_3} {range_} {_4}'
                elif choose_str == "(y,z)->(z,-y)":
                    # 批次15：(y,z)变成(z,-y), oss中对应文件202209222
                    new_line = f'{x} {z} {-y} {_1} {intensity} {t} {reflectivity} {ring} {_2} {ambient} {_3} {range_} {_4}'
                writefile.write(f"{new_line.strip()}\n")


if __name__ == '__main__':
    oss_obj = OSSAPI()
    session = get_session()
    oss_prefix = "https://projecteng.oss-cn-shanghai.aliyuncs.com/"

    # in_oss_path = "oss://projecteng/0_ProjectData/upload_data/313d_8ea8de08344c47cd9ea5782213c7d650/20220922/"
    parser = ArgumentParser(description="HJ智驾3d点云标注前处理")
    parser.add_argument(
        'in_oss_path',
        help='请输入oss路径, 框内路径为例子, 根据实际路径自行改写',
        default='oss://projecteng/0_ProjectData/upload_data/313d_8ea8de08344c47cd9ea5782213c7d650/20220922/',
        type=str
    )
    parser.add_argument(
        'choose_str',
        help='请选择转换方式, eg: 已有转换方式:1.(x,y)->(y,-x)2.(y,z)->(z,-y)',
        default='(x,y)->(y,-x)',
        type=str
    )
    args = parser.parse_args()
    # 输入路径->oss路径
    in_oss_path = args.in_oss_path
    choose_str = args.choose_str.replace(" ", "")
    assert choose_str == "(x,y)->(y,-x)" or choose_str == "(y,z)->(z,-y)", "请输入正确的转换方式，若超出已有转换方式，请联系PE添加。"
    sys.exit(main())
