# -*- coding: utf-8 -*-
"""
Author: Ethan Chai
Date: 2022/10/9 12:00
input: 
output: 
Short Description:
    - 安装
        - pip3 install moviepy
    - 入门：http://doc.moviepy.com.cn/index.html#document-2_MoviePy%E5%85%A5%E9%97%A8/index
    - error
        - ValueError: MoviePy couldn't find the codec associated with the filename. Provide the 'codec' parameter in write_videofile.
            - 使用codec参数手动放置编解码器
                扩展	        编解码器
                mp4	        libx264
                OGV	        自由女神
                网络管理器	libvpx
                奥格	        库沃尔比斯
                mp3	        pcm_s16le
                声波	        库沃尔比斯
                m4a	        libfdk_aac
Change History:
"""
from moviepy.editor import VideoFileClip, concatenate_videoclips, clips_array, vfx
from peutils.fileutil import list_current_file


def video_clip(mp4_pth, save_pth):
    """concatenate_videoclips连接操作"""
    # clip1 = VideoFileClip(mp4_pth+"/235_1668151574_0_10.mp4")
    # # .subclip(start, end) 剪辑时长
    # clip2 = VideoFileClip(mp4_pth+"/235_1668151574_10_20.mp4").subclip(5, 10)
    # clip3 = VideoFileClip(mp4_pth+"/235_1668151574_20_30.mp4")
    # final_clip = concatenate_videoclips([clip1, clip2, clip3])

    mp4_list = list_current_file(mp4_pth, type='file', suffix='mp4')
    clips = [VideoFileClip(clip) for clip in mp4_list]
    final_clip = concatenate_videoclips(clips)

    # 使用codec参数手动放置编解码器
    final_clip.write_videofile(save_pth, codec="libx264")

    """堆叠操作"""
    # clip1 = VideoFileClip("myvideo.mp4").margin(10)  # add 10px contour
    # clip2 = clip1.fx(vfx.mirror_x)
    # clip3 = clip1.fx(vfx.mirror_y)
    # clip4 = clip1.resize(0.60)  # downsize 60%
    # final_clip = clips_array([[clip1, clip2],
    #                           [clip3, clip4]])
    # final_clip.resize(width=480).write_videofile("my_stack.mp4")


video_clip(mp4_pth="input_folder_path", save_pth='save_mp4_file_path.mp4')

