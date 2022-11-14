# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/11/14 10:23
input   : 
output  :   
Short Description: 
Change History:
"""
from argparse import FileType
from peutils.textutil import gen_uuid
from peutils.fileutil import list_current_file
from peutils.transform.v1.img_com.parser import ImgComParse, ImgComDataConfig
from peutils.transform.v1.audio_seg.parser import AudioSegParse, AudioSegDataConfig
from peutils.transform.v1.lidar_box.parser import LidarBoxParse, LidarBoxDataConfig
from peutils.transform.v1.lidar_box.pre_parser import LidarBoxPre
from peutils.transform.v1.base import get_session, Lidar3dObj, dict_adapter
from peutils.transform.v1.lidar_manifest.parser import LidarManifestParse, LidarManifestConfig
from peutils.transform.v1.task.executor import AbstractTask, CommonTaskV1
from wooey_utils.com.oss_tool import OSS_API
from peutils.wooeyutil import WooeyBaseZipHandlerFile
from PIL import Image, ImageStat
from gooey import GooeyParser, Gooey
from ast import literal_eval
from collections import defaultdict
from itertools import groupby
from operator import itemgetter
from datetime import datetime
import numpy as np
import pandas as pd
import sys, os, json, requests, cv2


def tif_to_png(image_path, save_file_path):
    """
    :param image_path: *.tif image path
    :param save_file_path: *.png image path
    :return:
    """
    img = cv2.imread(image_path, 3)
    filename = os.path.basename(image_path).replace('tif', 'png')
    cv2.imwrite(os.path.join(save_file_path, filename), img)


if __name__ == '__main__':
    root_path = r'../../EthanFileData/Images'
    save_path = r'../../EthanFileData/Images/tif-png'
    os.makedirs(save_path, exist_ok=True)
    image_files = list_current_file(path=root_path, type='file', suffix='.tif')
    for image_file in image_files:
        tif_to_png(image_file, save_path)
