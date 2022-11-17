# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/11/14 10:23
input   : 
output  :   
Short Description: 
Change History:
"""
from peutils.fileutil import list_current_file
import os, cv2


def tif_to_png(image_path, save_file_path):
    """
    :param image_path: *.tif image path
    :param save_file_path: *.png image path
    :return:
    """
    img = cv2.imread(image_path, 3)
    filename = os.path.basename(image_path).replace('tif', 'png')
    cv2.imwrite(os.path.join(save_file_path, filename), img)


def png_to_tig(image_path, save_file_path):
    """
    :param image_path: *.png image path
    :param save_file_path: *.tif image path
    :return:
    """
    img = cv2.imread(image_path, 3)
    filename = os.path.basename(image_path).replace('png', 'tif')
    cv2.imwrite(os.path.join(save_file_path, filename), img)


if __name__ == '__main__':
    root_path = r'../../EthanFileData/File img'
    save_png_path = r'../../EthanFileData/File img/tif-png'
    save_tif_path = r'../../EthanFileData/File img/png-tif'

    os.makedirs(save_png_path, exist_ok=True)
    image_files = list_current_file(path=root_path, type='file', suffix='.tif')
    for image_file in image_files:
        tif_to_png(image_file, save_png_path)

    os.makedirs(save_tif_path, exist_ok=True)
    image_files = list_current_file(path=save_png_path, type='file', suffix='.png')
    for image_file in image_files:
        png_to_tig(image_file, save_tif_path)
