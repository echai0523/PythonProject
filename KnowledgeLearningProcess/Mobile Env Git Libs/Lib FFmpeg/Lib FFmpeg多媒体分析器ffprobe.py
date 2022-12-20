# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/11/23 14:22
input   : 
output  :   
Short Description:
    ffprobe 常用命令
        ffprobe --help
            1) ffprobe -show_packets 数据包信息
            2) ffprobe -show_data    具体数据
                eg: ffprobe -show_data -show_packets input.flv 查看数据包内具体数据
            3) ffprobe -show_format  封装格式
                ffprobe -show_format input.mp4 |grep start_time    指定查看视频开始时间
                ffprobe -show_format input.mp4 |grep duration      指定查看视频持续时间
            4) ffprobe -show_frames  帧信息
            4) ffprobe -show_streams 流信息

        ffprobe -print_format/-of 格式化显示方式
            格式化输出信息，包含XML、INI、JSON、CSV、FLAT等
                eg: ffprobe -of xml -show_streams input.flv 以XML格式输出流信息
            select_streams 只查看音频(a)、视频(v)、字幕(s)的信息
                eg: ffprobe -show_frames -select_streams v -of xml input.flv 查看视频帧信息并以XML格式输出

Change History:
"""
import os


def ffprobe_show_streams(file):
    os.system(f"ffprobe -show_streams {file}")


def ffprobe_show_format(file, grep=None):
    if grep:
        os.system(f"ffprobe -v quiet -show_format {file} |grep {grep}")
    else:
        os.system(f"ffprobe -v quiet -show_format {file}")


video_file = '../../../EthanFileData/AudioVideo/叶问4先行预告.mp4'

# show_streams
ffprobe_show_streams(file=video_file)




