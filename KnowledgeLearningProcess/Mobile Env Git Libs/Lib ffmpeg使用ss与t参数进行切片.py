# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/11/17 15:51
input   : 
output  :   
Short Description:
    - ffmpeg使用ss与t参数进行切片
        -ss   指定剪切开头部分
        -t    指定视频总长度
        -to   截止时间
        -output_ts_offset   指定输出start_time
    - ffprobe使用show_format查看视频信息
        |grep start_time    查看视频开始时间
        |grep duration      查看视频持续时间
        ;                   多条命令同时查看多个视频
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
# 原mp4
ffprobe_show_format(file=video_file, grep="start_time")
ffprobe_show_format(file=video_file, grep="duration")
# 剪切后mp4
ffprobe_show_format(file=save_path + "10s-end.mp4", grep="start_time")
ffprobe_show_format(file=save_path + "10s-end.mp4", grep="duration")
# os.system(f'ffprobe -v quiet -show_format {video_file} |grep start_time; ffprobe -v quiet -show_format {save_path + "10s-end.mp4"}|grep start_time')
# os.system(f'ffprobe -v quiet -show_format {video_file} |grep duration; ffprobe -v quiet -show_format {save_path + "10s-end.mp4"}|grep duration')

"""-t指定视频总长度"""
os.system(f'ffmpeg -i {video_file} -c copy -t 10 -copyts {save_path + "start-10s.mp4"}')
# 查看起始时间(开始)与持续时间(长度)
# os.system(f'ffprobe -v quiet -show_format {video_file} |grep start_time; ffprobe -v quiet -show_format {save_path + "start-10s.mp4"}|grep start_time')
# 剪切后mp4
ffprobe_show_format(file=save_path + "start-10s.mp4", grep="start_time")
ffprobe_show_format(file=save_path + "start-10s.mp4", grep="duration")
# os.system(f'ffprobe -v quiet -show_format {video_file} |grep duration; ffprobe -v quiet -show_format {save_path + "start-10s.mp4"}|grep duration')

"""-output_ts_offset指定输出start_time"""
# 前面补120s的黑屏，从120s开始接10s剪切部分
os.system(f'ffmpeg -i {video_file} -c copy -t 10 -output_ts_offset 120 {save_path + "offset-120.mp4"}')
# 查看信息
# start_time=120.000000
# duration=130.008000
ffprobe_show_format(file=save_path + "offset-10.mp4")
# os.system(f'ffprobe -v quiet -show_format {save_path + "offset-10.mp4"}')

"""学以致用"""
# 从10s开始剪切10s片段，对剪切片段前面补0s黑屏
os.system(f'ffmpeg -ss 10 -i {video_file} -c copy -t 10 -output_ts_offset 0 {save_path + "offset-0.mp4"}')



