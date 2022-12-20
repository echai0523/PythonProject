# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/12/14 15:53
input   : 
output  :   
Short Description:
    # 参考: https://blog.csdn.net/weixin_43229348/article/details/125986969
Change History:
"""
import numpy as np
import cv2

# 坐标转为矩阵
points = np.array([[3, 2], [5, 2], [5, 6], [6, 5], [4, 7], [2, 5], [3, 6]])
# 求外接最小面积矩形框
rect = cv2.minAreaRect(points)
print(rect)
# 中心点xy，旋转角第一个边为w，另一个为h，theta旋转角
(cx, cy), (w, h), theta = rect
print(cx, cy, w, h, theta)
# 矩形框4个焦点
box_points = cv2.boxPoints(rect)
# box = np.int0(box)  # 取整
print([{"x": p[0], "y": p[1]} for p in box_points])
