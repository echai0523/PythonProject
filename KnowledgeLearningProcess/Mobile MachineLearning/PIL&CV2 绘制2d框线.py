# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/12/7 17:26
input   : 
output  :   
Short Description:
    根据坐标绘制2d框的四条线
    0 · · · · · · · · · ·>x
    ·
    ·    (x,y)    (x1,y)
    ·     · · · · ·
    ·     ·       ·
    ·     ·绘制4线 ·
    ·     ·       ·
    ·     · · · · ·
    ·   (x,y1)   (x1,y1)
    ·

    参考：https://blog.csdn.net/qq_17498785/article/details/104858251
Change History:
"""
from PIL import Image, ImageDraw
from io import BytesIO
import os, requests, cv2, shutil


def cv2_draw_box_line(image_path, left_up: tuple, right_down: tuple):
    """
    仅支持本地路径，且坐标值必须为int型
    left_up, right_down都是矩形在图片的像素坐标位置，且坐标位置为int整型
    :param image_path: 绘制框线后小图文件名
    :param left_up: 左上角xy(最小点), type-> tuple(int, int)
    :param right_down: 右下角xy(最大点), type-> tuple(int, int)
    :return:
    """
    image = cv2.imread(image_path)
    cv2.rectangle(image, left_up, right_down, (0, 255, 0), 2)
    cv2.imwrite(image_path, image)


def pil_draw_box_line(image_path, leftup_rightdown: tuple):
    """
    支持url 和 本地路径，坐标值 int 或 float
    leftup_rightdown都是矩形在图片的像素坐标位置
    :param image_path: 绘制框线后小图文件名
    :param leftup_rightdown: 左上角xy(最小点) and 右下角xy(最大点), type-> tuple(,,,,)
    :return:
    """
    if image_path.startswith('http'):
        img = Image.open(BytesIO(requests.get(image_path).content))
    else:
        img = Image.open(image_path)  # 打开图片

    a = ImageDraw.ImageDraw(img)  # 用a来表示右侧这段

    # fill填充eg:白色white，outline边框eg:黑色back，width边框粗细eg:1像素
    a.rectangle(leftup_rightdown, fill=None, outline="red", width=1)
    img.save(image_path)


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
cv2_img_path = "../../EthanFileData/Img/ADAS_20221102-232058_242_0_1560158590915.jpeg"
pil_img_path = "https://github.com/echai0523/PythonProject/blob/main/EthanFileData/Img/ADAS_20221102-232058_242_0_1560158590915.jpeg",

pth = "../../EthanFileData/Img/test"
out_path = f"{pth}/{os.path.basename(cv2_img_path)}"
os.makedirs(pth, exist_ok=True)

# 多框情况必须需要先复制图片备份，防止多框绘制将原图覆盖
shutil.copyfile(cv2_img_path, out_path)

for point in points:
    # cv2_draw_box_line(
    #     image_path=out_path,
    #     left_up=(int(point[0]["x"]), int(point[0]["y"])),
    #     right_down=(int(point[2]["x"]), int(point[2]["y"]))
    # )

    pil_draw_box_line(
        image_path=out_path,
        leftup_rightdown=(point[0]["x"], point[0]["y"], point[2]["x"], point[2]["y"])
    )
