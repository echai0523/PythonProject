# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2023/1/5 18:01
input   : 
output  :   
Short Description:
    - 获取左下角坐标
        - get_left_down_point
Change History:
"""
import math


def get_left_down_point(points_list):
    # 最理想的左下角坐标(xmin, ymax) -> 最小x，最大y
    xmin, ymax = min([p[0] for p in points_list]), max([p[1] for p in points_list])
    distances = [math.sqrt((p[0] - xmin) ** 2 + (p[1] - ymax) ** 2) for p in points_list]  # 各顶点到理想点的距离
    sort_distances = distances.copy()
    sort_distances.sort()  # 从近到远重排距离
    # 距离理想点最近的两个点可为左下角坐标，取其索引值
    idx0, idx1 = distances.index(sort_distances[0]), distances.index(sort_distances[1])
    # y值大的为左下角坐标，因手滑会有0.+的偏差，所以int取整比较(避免矩形)
    # 以最下面的点为左下角坐标
    return points_list[idx0] if int(points_list[idx0][1]) >= int(points_list[idx1][1]) else points_list[idx1]
    # # 以最左边的点为左下角坐标
    # return points_list[idx0] if int(points_list[idx0][1]) <= int(points_list[idx1][1]) else points_list[idx1]


xy_points = [
    {
        "x": 2327.449518,
        "y": 776.850534
    },
    {
        "x": 2331.771575,
        "y": 782.799718
    },
    {
        "x": 2339.449581,
        "y": 782.850565
    },
    {
        "x": 2343.771637,
        "y": 777.15562
    },
    {
        "x": 2343.771637,
        "y": 767.036923
    },
    {
        "x": 2339.520769,
        "y": 760.84028
    },
    {
        "x": 2332.300392,
        "y": 760.636889
    },
    {
        "x": 2327.317316,
        "y": 766.891159
    },
    {
        "x": 2327.21562,
        "y": 776.399683
    }
]
left_down_point = get_left_down_point(points_list=[[p["x"], p["y"]] for p in xy_points])

