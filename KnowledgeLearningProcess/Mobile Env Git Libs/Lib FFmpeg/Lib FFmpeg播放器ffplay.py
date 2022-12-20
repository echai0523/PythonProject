# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/11/23 14:47
input   : 
output  :   
Short Description:
    ffplay 不仅仅是 播放器，也是ffmpeg的codec引擎、format引擎、filter引擎工具，也可进行可视化的媒体参数分析。

    ffplay 常用命令
        ffplay --help

    ffplay 参数
        x: 强制设置视频显示窗口的宽
        y: 强制设置视频显示窗口的高
        s: 设置视频显示窗口的宽高
        fs: 强制全屏显示
        an: 屏蔽音频
        vn: 屏蔽视频
        sn: 屏蔽字幕
        ss: 根据设置的秒进行定位拖动
        t: 设置播放视频/音频的长度
        bytes: 设置定位拖动的策略, 不可拖动(0), 可拖动(1), 自动(-1)
        nodisp: 关闭图形化显示窗口
        f: 强制使用设置的格式进行解析
        window_title: 设置显示窗口的标题
        af: 设置音频的滤镜
        codec: 强制使用设置的codec进行解码
        autorotate: 自动旋转视频

        ast: 设置将要播放的音频流
        vst: 设置将要播放的视频流
        sst: 设置将要播放的字幕流
        stats: 输出播放状态
        fast: 非标准化规范的多媒体兼容优化
        sync: 音视频同步设置可根据音频时间、视频时间或者外部扩展时间进行参考
        autoexit: 播放完毕后自动退出ffplay, ffplay默认播放完毕不退出播放器
        exitkeydown: 当有键盘按键事件产生时退出ffplay
        exitmousedown: 当有鼠标按键事件产生时退出ffplay
        loop: 设置循环播放次数
        framedrop: 当CPU资源占用过高时, 自动丢帧
        infbuf: 设置无限极的播放器ffplay, 该项常见于实时流媒体播放场景
        vf: 视频滤镜设置
        acodec: 强制使用设置的音频编码器
        vcodec: 强制使用设置的视频编码器
        scodec: 强制使用设置的字幕编码器


Change History:
"""
import os


# 从第30s开始播放10s
os.system("ffplay -ss 30 -t 10 input.mp4")

# 播放时窗口标题为自定义标题“播放测试”
os.system("ffplay -window_title '播放测试' input.mp4")

# 打开网络直播流
os.system("ffplay -window_title '播放测试' rtmp://up.v.test.com/live/stream")

# 从第30s开始播放10s，播放完毕后自动退出ffplay，播放窗口标题“Hello”，为确认播放时长正确，可通过系统命令time查看命令运行时长
os.system("time ffplay -window_title 'Hello' -ss 30 -t 10 -autoexit input.mp4")

# 强制使用H.264解码器解码MPEG4视频会报错
os.system("ffplay -vcodec h264 output.mp4")

# 播放视频时加载字幕文件(.ass / .srt)，首先编写字幕文件
os.system("ffplay -window_title 'The Movie' -vf 'subtitles=input.srt' output.mp4")




