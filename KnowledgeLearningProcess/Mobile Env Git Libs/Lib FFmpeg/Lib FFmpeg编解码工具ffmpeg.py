# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/11/17 15:51
input   : 
output  :   
Short Description:
    ffmpeg 是 FFmpeg源代码编译后生成的一个可执行程序，其可以作为命令行工具使用。
    eg: "ffmpeg -i input.mp4 output.avi"  -> -i 参数 将input.mp4作为输入源输入，然后进行转码与转封装操作，输出到output.avi
        1) 获得输入源input.mp4
        2) 转码
        3) 输出文件output.avi
    eg: "ffmpeg -i input.mp4 -f output.dat" -> -f 参数 指定输出文件的容器格式。

    ffmpeg 主要工作流程(https://raw.githubusercontent.com/echai0523/ScreenshotFigureBed/main/image/202211231438740.png):
        1) 解封装
        2) 解码
        3) 编码
        4) 封装
        需经过6个步骤:
            1) 读取输入源
            2) 进行音视频的解封装
            3) 解码每一帧音视频数据
            4) 编码每一帧音视频数据
            5) 进行音视频的重新封装
            6) 输出到目标

    ffmpeg 常用命令
        ffmpeg --help        基础帮助信息
            1) ffmpeg --help long   高级帮助信息
            2) ffmpeg --help full   全部帮助信息
            3) ffmpeg -version      查看ffmpeg版本
            4) ffmpeg -formats      转码时无法解析或无法生成的视频文件，查看是否支持对应的视频文件
            5) ffmpeg -codecs       编/解码器支持
            6) ffmpeg -encoders     编码器支持
            7) ffmpeg -decoders     解码器支持
            8) ffmpeg -filters      滤镜支持
                # 了解具体某种demuxer、muxer、encoder、decoder、filter类型
                ) ffmpeg -h muxer=flv       FLV封装器支持
                ) ffmpeg -h demuxer=flv     FLV解封装器支持
                ) ffmpeg -h encoder=h264    H.264编码支持
                ) ffmpeg -h decoder=h264    H.264解码支持
                ) ffmpeg -h filter=colorkey colorkey滤镜支持

        ffmpeg 封装转换
            查看 ffmpeg --help full 全部帮助信息 > AVFormatContext 下参数均为封装转换可用参数

        ffmpeg 转码
            查看 ffmpeg --help full 全部帮助信息 > AVCodecContext 下参数均为编解码可用参数
            ffmpeg 基本转码原理 eg: ffmpeg -i input.rmvb -vcodec mpeg4 -b:v 200k -r 15 -an output.mp4
                1) .mp4: 转封装格式, RMVB -> MP4
                2) -vcodec mpeg4: 视频编码, RV40 -> MPEG4
                3) -b:v 200k: 视频码率, **kbit/s -> 200kbit/s。b设置音频与视频码率, b:v视频码率, b:a音频码率
                4) -r 15: 视频帧率, **fps -> 15fps
                5) -an: 转码后文件不含音频

    1. ffmpeg使用ss与t参数进行切片
        1) -ss   指定剪切开头部分
        2) -t    指定视频总长度
        3) -to   截止时间
        4) -output_ts_offset   指定输出start_time


Change History:
"""
import os


def ffprobe_show_format(file, grep=None):
    if grep:
        os.system(f"ffprobe -v quiet -show_format {file} |grep {grep}")
    else:
        os.system(f"ffprobe -v quiet -show_format {file}")


video_file = '../../../EthanFileData/AudioVideo/叶问4先行预告.mp4'
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



