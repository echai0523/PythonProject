# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/12/7 17:26
input   : 
output  :   
Short Description:
    根据坐标截取小图
    0 · · · · · · · · · ·>x
    ·
    ·    (x,y)    (x1,y)
    ·     · · · · ·
    ·     ·       ·
    ·     ·  截取  ·
    ·     ·       ·
    ·     · · · · ·
    ·   (x,y1)   (x1,y1)
    ·
Change History:
"""
from PIL import Image
from io import BytesIO
import os, requests, cv2


def pil_image_matting(img_path, out_path, left_up, right_down):
    """
    支持url 和 本地路径，坐标值 int 或 float
    :param img_path: 原图片路径
    :param out_path: 截取后小图文件名
    :param left_up: 左上角xy(最小点) type-> tuple(,,,,)
    :param right_down: 右下角xy(最大点) type-> tuple(,,,,)
    :return:
    """
    min_x, min_y = left_up
    max_x, max_y = right_down
    if img_path.startswith('http'):
        img = Image.open(BytesIO(requests.get(img_path).content))  # .convert('L') 黑白
    else:
        img = Image.open(img_path)  # 本地路径

    # 左上xy,右下xy
    cropped = img.crop((min_x, min_y, max_x, max_y))
    cropped.save(out_path)


def cv2_image_matting(img_path, out_path, left_up, right_down):
    """
    仅支持本地路径，且坐标值必须为int型
    left_up, right_down都是矩形在图片的像素坐标位置，且坐标位置为int整型
    :param img_path: 原图片路径
    :param out_path: 截取后小图文件名
    :param left_up: 左上角xy(最小点), type-> tuple(int, int)
    :param right_down: 右下角xy(最大点), type-> tuple(int, int)
    :return:
    """
    min_x, min_y = left_up
    max_x, max_y = right_down

    img = cv2.imread(img_path)
    # 切片必须为int型
    # [纵min: 纵max, 横min, 横max]
    crop = img[int(min_y):int(max_y), int(min_x):int(max_x)]
    cv2.imwrite(out_path, crop)  # 输出


points = [
    [{'x': 1328.059055, 'y': 1110.833524}, {'x': 1741.203222, 'y': 1110.833524}, {'x': 1741.203222, 'y': 1474.037187},
     {'x': 1328.059055, 'y': 1474.037187}],
    [{'x': 1702.815035, 'y': 1136.72013}, {'x': 1857.161725, 'y': 1136.72013}, {'x': 1857.161725, 'y': 1300.968305},
     {'x': 1702.815035, 'y': 1300.968305}],
    [{'x': 1797.422224, 'y': 1142.102556}, {'x': 1883.560589, 'y': 1142.102556}, {'x': 1883.560589, 'y': 1228.898466},
     {'x': 1797.422224, 'y': 1228.898466}],
    [{'x': 1946.042498, 'y': 1156.909241}, {'x': 1969.717583, 'y': 1156.909241}, {'x': 1969.717583, 'y': 1180.165298},
     {'x': 1946.042498, 'y': 1180.165298}]
]
pth = "../../EthanFileData/Img/image_matting"
os.makedirs(pth, exist_ok=True)
for idx, point in enumerate(points):
    cv2_image_matting(
        img_path="../../EthanFileData/Img/ADAS_20221102-232058_242_0_1560158590915.jpeg",
        out_path=f"{pth}/cv2_{idx}.jpeg",
        left_up=[point[0]["x"], point[0]["y"]],
        right_down=[point[2]["x"], point[2]["y"]]
    )
    pil_image_matting(
        img_path="https://github.com/echai0523/PythonProject/blob/main/EthanFileData/Img/ADAS_20221102-232058_242_0_1560158590915.jpeg",
        out_path=f"{pth}/pil_{idx}.jpeg",
        left_up=[point[0]["x"], point[0]["y"]],
        right_down=[point[2]["x"], point[2]["y"]]
    )
