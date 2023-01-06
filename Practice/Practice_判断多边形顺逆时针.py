# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2023/1/5 18:00
input   : 
output  :   
Short Description:
    - 判断多边形顺逆时针
        - calculate_polygon_area()
Change History:
"""


def calculate_polygon_area(points_list):
    n = len(points_list)
    d = 0
    for i in range(n - 1):
        d += -0.5 * (points_list[i + 1][1] + points_list[i][1]) * (points_list[i + 1][0] - points_list[i][0])
    d += -0.5 * (points_list[0][1] + points_list[n - 1][1]) * (points_list[0][0] - points_list[n - 1][0])

    order = "顺时针" if d > 0 else "逆时针"
    return order


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
res = calculate_polygon_area(points_list=[[p["x"], p["y"]] for p in xy_points])






