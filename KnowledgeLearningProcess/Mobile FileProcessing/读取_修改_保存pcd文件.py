# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/9/2 10:27

input: 

output: 

Short Description: 

Change History:
    
"""
import numpy as np
from peutils import pcd_py3


def main():
    # 读取pcd文件 "../../EthanFileData/1659430571904366.pcd" or "/projecteng/" + pcd_file
    point_pcd_result = pcd_py3.PointCloud.from_path(r"../../EthanFileData/1659430571904366.pcd")
    width = point_pcd_result.width
    points_count = point_pcd_result.points
    points_iter = ((p[0], p[1], p[2], p[3]) for p in point_pcd_result.pc_data)
    point_list = np.array(list(points_iter), dtype="float32")
    # pcd的头
    header_string = f"VERSION 0.7\nFIELDS x y z intensity \nSIZE 4 4 4 4\n" \
                    f"TYPE F F F F\nCOUNT 1 1 1 1\nWIDTH {width}\nHEIGHT 1\n" \
                    f"VIEWPOINT 0.0 0.0 0.0 1.0 0.0 0.0 0.0\nPOINTS {points_count}\nDATA ascii\n"
    # print(point_pcd_result)
    TopCenter_ego_matrix = np.array([[0.997457, 0.014383, 0.069803, 6.099690],
                                     [-0.014482, 0.999895, 0.000907, -0.060999],
                                     [-0.069782, -0.001916, 0.997560, 2.700000],
                                     [0.000000, 0.000000, 0.000000, 1.000000]])

    for pcd_index, point_pcd_row in enumerate(point_list):
        # print("row", point_pcd_row, np.dot(TopCenter_ego_matrix, point_pcd_row))
        p1, p2, p3, _ = point_pcd_row
        point_list[pcd_index] = np.dot(TopCenter_ego_matrix, np.array([p1, p2, p3, 1]))

    # 重写pcd文件 "../../EthanFileData/pcd_1.pcd"  out_pcd_path + pcd_name
    # print(point_list)
    # with open("../../EthanFileData/pcd_1.pcd", 'w') as writefile:
    #     writefile.write(header_string)
    #     for p in point_list:
    #         new_line = f'{p[0]} {p[1]} {p[2]} {p[3]}'
    #         writefile.write(f"{new_line.strip()}\n")


if __name__ == '__main__':
    main()
