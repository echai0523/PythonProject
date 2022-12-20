# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/12/14 16:20
input   : 
output  :   
Short Description:
    1. 角度制弧度制互转
        参考: https://blog.csdn.net/weixin_41010198/article/details/126278336
    2. 角度区间转换
        参考: https://blog.csdn.net/gsgbgxp/article/details/117430052
Change History:
"""
from argparse import ArgumentParser, FileType
from peutils.textutil import gen_uuid
from peutils.fileutil import list_current_file
from peutils.transform.v1.img_com.parser import ImgComParse, ImgComDataConfig
from peutils.transform.v1.audio_seg.parser import AudioSegParse, AudioSegDataConfig
from peutils.transform.v1.lidar_box.parser import LidarBoxParse, LidarBoxDataConfig
from peutils.transform.v1.lidar_point.parser import LidarPointParse, LidarPointDataConfig
from peutils.transform.v1.lidar_box.pre_parser import LidarBoxPre
from peutils.transform.v1.base import get_session, Lidar3dObj, dict_adapter
from peutils.transform.v1.lidar_manifest.parser import LidarManifestParse, LidarManifestConfig
from peutils.transform.v1.task.executor import AbstractTask, CommonTaskV1
from wooey_utils.com.oss_tool import OSS_API
from peutils.wooeyutil import WooeyBaseZipHandlerFile
from urllib.parse import quote, unquote
from PIL import Image, ImageStat
from gooey import GooeyParser, Gooey
from ast import literal_eval
from collections import defaultdict
from itertools import groupby
from operator import itemgetter
from datetime import datetime
from io import BytesIO
import numpy as np
import pandas as pd
import math
from math import pi, sin, cos, atan2

du = -70
# 角度制转为弧度制
# r = du*pi/180
r = math.radians(du)  # 传入参数为角度制 180度=pi
print(r)  # 4.71238898038469

# 弧度制转为角度制
degree = math.degrees(r)  # 传入参数为弧度制
print(degree)  # 270.0

alpha = du * pi / 180  # 4.71238898038469
"""将角度转换到[−π, π]"""
# # 方法一 左闭右开 [180,180)
# alpha1 = alpha - 2*pi*np.floor((alpha+pi)/(2*pi))
# # 方法二 左闭右闭 [180,180]
# alpha2 = atan2(sin(alpha), cos(alpha))
# print(alpha1, alpha2)

