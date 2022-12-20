# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/9/23 17:41

input:

output:d

Short Description:
    - 读取pcd文件
        point_pcd_result = pcd_py3.PointCloud.from_path(pcd_path)
        points_iter = (
            (p[0], p[1], p[2]) for p in point_pcd_result.pc_data
        )
        point_list = np.array(list(points_iter), dtype="float32")
    - pcd头部
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
    - 重写pcd文件
        with open(out_pcd_path, 'w') as writefile:
            writefile.write(header_string)
            writefile.write(points_str)
Change History:

"""
import numpy as np
from peutils import pcd_py3


def parse_point():
    """正常解析point，对point增值、换位等"""
    # 读取pcd文件
    point_pcd_result = pcd_py3.PointCloud.from_path("../../EthanFileData/Binary/000000.pcd")
    # pcd 点
    points_iter = (
        (p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12]) for p in point_pcd_result.pc_data
    )
    point_list = np.array(list(points_iter), dtype="float32")
    # 头部信息
    header_string = f"# .PCD v0.7 - Point Cloud Data file format\n" \
                    f"VERSION 0.7\n" \
                    f"FIELDS x y z _ intensity t reflectivity ring _ ambient _ range _\n" \
                    f"SIZE 4 4 4 1 4 4 2 1 1 2 1 4 1\n" \
                    f"TYPE F F F U F U U U U U U U U\n" \
                    f"COUNT 1 1 1 4 1 1 1 1 0 1 0 1 15\n" \
                    f"WIDTH {point_pcd_result.width}\n" \
                    f"HEIGHT {point_pcd_result.height}\n" \
                    f"VIEWPOINT 0.0 0.0 0.0 1.0 0.0 0.0 0.0\n" \
                    f"POINTS {point_pcd_result.points}\n" \
                    f"DATA binary\n"
    # 重写pcd文件
    with open("000000.pcd", 'w') as writefile:
        # 先固定写好头部
        writefile.write(header_string)
        # 对每个point处理
        for point_pcd_row in point_list:
            x, y, z, _1, intensity, t, reflectivity, ring, _2, ambient, _3, range_, _4 = point_pcd_row
            # (x,y)变成(y,-x)
            new_line = f'{y} {-x} {z} {_1} {intensity} {t} {reflectivity} {ring} {_2} {ambient} {_3} {range_} {_4}'
            writefile.write(f"{new_line.strip()}\n")


def eliminate_point():
    """剔除point的情况，pcd头部描述信息需要更新 宽/高/点云数量"""
    # 读取pcd文件
    point_pcd_result = pcd_py3.PointCloud.from_path("../../EthanFileData/Binary/1639623722.199605942.pcd")
    # pcd 点
    points_iter = (
        (p[0], p[1], p[2]) for p in point_pcd_result.pc_data
    )
    point_list = np.array(list(points_iter), dtype="float32")
    # 针对剔除points的情况，pcd头部描述信息需要更新 宽/高/点云数量
    # 用于头部描述，更新最新的宽/高/点云数量，继用原pcd的宽/高/点云数量会导致新pcd无法使用pcd_py3读取
    width = points = 0
    points_str = ""
    for row_pcd_point in point_list:
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
    with open("1639623722.199605942.pcd", 'w') as writefile:
        writefile.write(header_string)
        writefile.write(points_str)


if __name__ == '__main__':
    parse_point()
    eliminate_point()
