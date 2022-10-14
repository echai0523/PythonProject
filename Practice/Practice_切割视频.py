# -*- coding: utf-8 -*-
"""
Author: Ethan Chai
Date: 2022/10/9 11:44
input:
output:
Short Description:
    - 获取视频文件播放时长
        - 方法一：VideoFileClip
            from moviepy.editor import VideoFileClip
            def get_duration_from_moviepy(url):
                clip = VideoFileClip(url)
                return clip.duration
        - 方法二：CV2  pip install opencv-python
            import cv2
            def get_duration_from_cv2(filename):
                cap = cv2.VideoCapture(filename)
                if cap.isOpened():
                rate = cap.get(5)
                frame_num =cap.get(7)
                duration = frame_num/rate
                return duration
                return -1
        - 方法三：FFmpeg  pip install ffmpy3
            import ffmpy3
            def get_duration_from_ffmpeg(url):
                tup_resp = ffmpy3.FFprobe(
                    inputs={url: None},
                    global_options=[
                        '-v', 'quiet',
                        '-print_format', 'json',
                        '-show_format', '-show_streams'
                    ]
                ).run(stdout=subprocess.PIPE)

                meta = json.loads(tup_resp[0].decode('utf-8'))
                return meta['format']['duration']

Change History:
"""
import glob

import cv2
from gooey import GooeyParser, Gooey
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from peutils.fileutil import list_current_file
from pydub import AudioSegment


def clip_video(source_file, target_file, start_time, stop_time):
    """
    利用moviepy进行视频剪切
    :param source_file: 原视频的路径，mp4格式
    :param target_file: 生成的目标视频路径，mp4格式
    :param start_time: 剪切的起始时间点（第start_time秒）
    :param stop_time: 剪切的结束时间点（第stop_time秒）
    :return:
    """
    validate_file(source_file)
    source_video = VideoFileClip(source_file)
    video = source_video.subclip(int(start_time), int(stop_time))  # 执行剪切操作
    video.write_videofile(target_file)  # 输出文件


def clip_audio(source_file, target_file, start_time, stop_time):
    """
    利用pydub进行音频剪切。pydub支持源文件为 mp4格式，因此这里的输入可以与视频剪切源文件一致
    :param source_file: 原视频的路径，mp4格式
    :param target_file: 生成的目标视频路径，mp4格式
    :param start_time: 剪切的起始时间点（第start_time秒）
    :param stop_time: 剪切的结束时间点（第stop_time秒）
    :return:
    """
    validate_file(source_file)
    audio = AudioSegment.from_file(source_file, "mp4")
    audio = audio[start_time * 1000: stop_time * 1000]
    audio_format = target_file[target_file.rindex(".") + 1:]
    audio.export(target_file, format=audio_format)


def combine_video_audio(video_file, audio_file, target_file, delete_tmp=False):
    """
    利用 ffmpeg将视频和音频进行合成
    :param video_file:
    :param audio_file:
    :param target_file:
    :param delete_tmp: 是否删除剪切过程生成的原视频/音频文件
    :return:
    """
    validate_file(video_file)
    validate_file(audio_file)
    # 注：需要先指定音频再指定视频，否则可能出现无声音的情况
    command = f"ffmpeg -y -i {audio_file} -i {video_file} -vcodec copy -acodec copy {target_file}"
    os.system(command)
    if delete_tmp:
        os.remove(video_file)
        os.remove(audio_file)


def clip_handle(source_file, target_file, start_time, stop_time, tmp_path=None, delete_tmp=False):
    """
    将一个视频文件按指定时间区间进行剪切
    :param source_file: 原视频文件
    :param target_file: 目标视频文件
    :param start_time: 剪切的起始时间点（第start_time秒）
    :param stop_time: 剪切的结束时间点（第stop_time秒）
    :param tmp_path: 剪切过程的文件存放位置
    :param delete_tmp: 是否删除剪切生成的文件
    :return:
    """
    # 设置临时文件名
    if tmp_path is None or not os.path.exists(tmp_path):
        # 如果没有指定临时文件路径，则默认与目标文件的位置相同
        # tmp_path = target_file[: target_file.rindex("/") + 1]
        tmp_path = target_file[: -len(os.path.basename(target_file))]
    # 切割视频名，不含后缀
    # target_file_name = target_file[target_file.rindex("/") + 1: target_file.rindex(".")]
    target_file_name = os.path.basename(target_file)[: -len('.mp4')]
    tmp_video = os.path.join(tmp_path, 'v' + target_file_name + ".mp4")
    tmp_audio = os.path.join(tmp_path, "a_" + target_file_name + ".mp4")

    # 执行文件剪切及合成
    clip_video(source_file, tmp_video, start_time, stop_time)
    clip_audio(source_file, tmp_audio, start_time, stop_time)
    combine_video_audio(tmp_video, tmp_audio, target_file, delete_tmp=True)


def validate_file(source_file):
    if not os.path.exists(source_file):
        raise FileNotFoundError("没有找到该文件：" + source_file)


def test_example():
    """
    测试例子
    :return:
    """
    root_path = '/Users/echai/Desktop/2085/'
    video_name = "big_buck_bunny.mp4"
    source_file = root_path + video_name  # '/Users/echai/Desktop/2085/687_1665283656.mp4'
    start_time = 15
    stop_time = 30

    # 设置目标文件名
    target_name = str(start_time) + "_" + str(stop_time)
    target_file = root_path + video_name.replace(".mp4", target_name + ".mp4")  # '/Users/echai/Desktop/2085/687_1665283656_5_6.mp4'
    # 处理主函数
    clip_handle(source_file, target_file, start_time, stop_time)


@Gooey(program_name='视频切分工具', show_preview_warning=False)
def main():
    parser = GooeyParser()
    parser.add_argument('root_path', metavar='目录', widget="DirChooser", help='请选择原文件目录')
    parser.add_argument('tmp_path', metavar='目录', widget="DirChooser", help='请选择生成文件目录')
    parser.add_argument('interval', widget="TextField", help='请选择间隔时间')
    args = parser.parse_args()

    root_path = args.root_path
    tmp_path = args.tmp_path
    interval = int(args.interval)

    # root_path = '../EthanFileData/mp4'
    # tmp_path = '../EthanFileData/mp4/out'
    # interval = 10

    os.makedirs(tmp_path, exist_ok=True)

    for source_file in list_current_file(root_path, type='file', suffix='.mp4'):
        print(source_file)
        video_name = os.path.basename(source_file)
        # 获取视频总时长
        clip = VideoFileClip(source_file)
        duration = clip.duration

        start_time = 0
        while start_time < duration - interval:
            stop_time = start_time + interval
            # 设置目标文件名 原路径/原名_起始时间_结束时间.mp4
            target_file = os.path.join(tmp_path, video_name.replace(".mp4", f"_{start_time}_{stop_time}.mp4"))
            # 处理主函数
            clip_handle(source_file, target_file, start_time, stop_time, tmp_path=tmp_path)
            start_time = stop_time
        else:
            # 设置目标文件名
            target_file = os.path.join(tmp_path, video_name.replace(".mp4", f"_{start_time}_{int(duration)}.mp4"))
            # 处理主函数
            clip_handle(source_file, target_file, start_time, duration, tmp_path=tmp_path)


if __name__ == "__main__":
    # test_example()
    main()

