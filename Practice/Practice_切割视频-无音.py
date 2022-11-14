# -*- coding: utf-8 -*-
"""
Author: Ethan Chai
Date: 2022/10/10 10:15
input: 
output: 
Short Description: 
Change History:
"""
import cv2
import os

from moviepy.video.io.VideoFileClip import VideoFileClip
from peutils.fileutil import list_current_file

file_path = '../EthanFileData/File audio video/'
out_path = '../EthanFileData/File audio video/out/'
time_set = 10  # 设置切割时间

os.makedirs(out_path, exist_ok=True)

for pth in list_current_file(file_path, type='file', suffix='.mp4'):
    # pth = os.path.join(file_path, name)
    print(pth)
    nm = os.path.basename(pth).split('.')[0]  # name = "**.mp4"
    cap = cv2.VideoCapture(pth)
    cap.isOpened()

    if cap.isOpened():  # 当成功打开视频时cap.isOpened()返回True,否则返回False
        # get方法参数按顺序对应下表（从0开始编号)
        rate = cap.get(5)  # 帧速率
        FrameNumber = int(cap.get(7))  # 视频文件的帧数
        print(FrameNumber)
        duration = FrameNumber / rate  # 帧速率/视频总帧数 是时间，除以60之后单位是分钟
        fps = int(rate)  # 每一段小视频帧数
        print(duration, fps)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        i = 0  # 第i帧
        while True:
            success, frame = cap.read()
            if success:
                i += 1
                # 1s是25帧，fps * 10是250帧即10s的总帧数
                if i % (fps * time_set) == 1:  # 10s保存一次视频
                    # i = 1，251, 501.......
                    videoWriter = cv2.VideoWriter(
                        os.path.join(out_path, f'{nm}_' + str(i // (fps * time_set) + 1) + '.mp4'),
                        cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'),
                        fps,
                        (int(width), int(height))
                    )
                    videoWriter.write(frame)

                else:
                    videoWriter.write(frame)
            else:
                print('end')
                break

    cap.release()

