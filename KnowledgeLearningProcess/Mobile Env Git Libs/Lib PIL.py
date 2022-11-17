# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/11/11 10:36
input   : 
output  :   
Short Description:
    - Image.open()
        - 读取本地img:
            - Image.open("../../EthanFileData/Img/11060.jpg")
        - 读取urlimg:
            - url = "http://www.bizhi360.com/meinv/11060.html"
            - Image.open(requests.get(url).content)
    - 获取图片亮度值的5种方式，返回值互不相同
        - get_image_light_mean()
        - get_image_light_rms()
        - get_image_light_mean_sqrt()
        - get_image_light_rms_sqrt()
        - get_image_light_gs()
Change History:
"""
from PIL import Image, ImageStat
import math, requests


def get_image_light_mean(dst_src):
    im = Image.open(dst_src).convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]


def get_image_light_rms(dst_src):
    im = Image.open(dst_src).convert('L')
    stat = ImageStat.Stat(im)
    return stat.rms[0]


def get_image_light_mean_sqrt(dst_src):
    im = Image.open(dst_src)
    stat = ImageStat.Stat(im)
    r, g, b = stat.mean
    return math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))


def get_image_light_rms_sqrt(dst_src):
    im = Image.open(dst_src)
    stat = ImageStat.Stat(im)
    r, g, b = stat.rms
    return math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))


def get_image_light_gs(dst_src):
    im = Image.open(dst_src)
    stat = ImageStat.Stat(im)
    gs = (math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))
          for r, g, b in im.getdata())
    return sum(gs) / stat.count[0]


