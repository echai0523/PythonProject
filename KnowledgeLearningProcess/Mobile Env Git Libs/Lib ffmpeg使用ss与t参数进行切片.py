# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/11/17 15:51
input   : 
output  :   
Short Description:
    1. ffmpeg使用ss与t参数进行切片
        1.1 -ss   指定剪切开头部分
        1.2 -t    指定视频总长度
        1.3 -to   截止时间
        1.4 -output_ts_offset   指定输出start_time
    2. ffprobe使用show_format查看视频信息
        2.1 |grep start_time    查看视频开始时间
        2.2 |grep duration      查看视频持续时间
        2.3 ;                   多条命令同时查看多个视频
        2.4 格式:
            [FORMAT]
            filename=test-out/offset-120.mp4
            nb_streams=2
            nb_programs=0
            format_name=mov,mp4,m4a,3gp,3g2,mj2
            format_long_name=QuickTime / MOV
            start_time=119.952993
            duration=130.209000
            size=1221455
            bit_rate=75045
            probe_score=100
            TAG:major_brand=isom
            TAG:minor_version=512
            TAG:compatible_brands=isomiso2avc1mp41
            TAG:encoder=Lavf59.27.100
            [/FORMAT]

Change History:
"""
import os


def ffprobe_show_format(file, grep=None):
    if grep:
        os.system(f"ffprobe -v quiet -show_format {file} |grep {grep}")
    else:
        os.system(f"ffprobe -v quiet -show_format {file}")


video_file = '../../EthanFileData/AudioVideo/叶问4先行预告.mp4'
save_path = 'test-out/'
os.makedirs(save_path, exist_ok=True)

"""-ss指定剪切开头部分"""
# eg 从10s处开始: -ss 10
os.system(f'ffmpeg -ss 10 -i {video_file} -c copy {save_path + "10s-end.mp4"}')
# 查看起始时间(开始)与持续时间(长度)
# 原mp4: start_time=0.000000  duration=60.001000
ffprobe_show_format(file=video_file, grep="start_time")
ffprobe_show_format(file=video_file, grep="duration")
# 剪切后mp4: start_time=0.000000  duration=49.954000
ffprobe_show_format(file=save_path + "10s-end.mp4", grep="start_time")
ffprobe_show_format(file=save_path + "10s-end.mp4", grep="duration")

"""-t指定视频总长度"""
os.system(f'ffmpeg -i {video_file} -c copy -t 10 -copyts {save_path + "start-10s.mp4"}')
# 查看起始时间(开始)与持续时间(长度)
# 剪切后mp4: start_time=0.000000  duration=10.209000
ffprobe_show_format(file=save_path + "start-10s.mp4", grep="start_time")
ffprobe_show_format(file=save_path + "start-10s.mp4", grep="duration")

"""-output_ts_offset指定输出start_time"""
# 前面补120s的黑屏，从120s开始接10s剪切部分
os.system(f'ffmpeg -i {video_file} -c copy -t 10 -output_ts_offset 120 {save_path + "offset-120.mp4"}')
# 查看信息(Short Description > 2. > 2.4): start_time=119.952993  duration=130.209000
ffprobe_show_format(file=save_path + "offset-120.mp4")

"""学以致用"""
# 从10s开始剪切10s片段，对剪切片段前面补0s黑屏
os.system(f'ffmpeg -ss 10 -i {video_file} -c copy -t 10 -output_ts_offset 0 {save_path + "offset-0.mp4"}')



