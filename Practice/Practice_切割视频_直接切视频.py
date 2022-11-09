# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/10/28 15:51
input   : 
output  :   
Short Description:
    - OpenCV VideoCapture
        - cap = cv2.VideoCapture(0)
            - 参数0: 默认为笔记本的内置第一个摄像头，如果需要读取已有的视频则参数改为视频所在路径路径，例如：cap=cv2.VideoCapture('video.mp4')
        - cap.isOpened()
            - 判断视频对象是否成功读取，成功读取视频对象返回True。
    - OpenCV VideoCapture.get()参数详解
                param	                    define
        cv2.VideoCapture.get(0)	    视频文件的当前位置（播放）以毫秒为单位
        cv2.VideoCapture.get(1)	    基于以0开始的被捕获或解码的帧索引
        cv2.VideoCapture.get(2)	    视频文件的相对位置（播放）：0=电影开始，1=影片的结尾。
        cv2.VideoCapture.get(3)	    在视频流的帧的宽度
        cv2.VideoCapture.get(4)	    在视频流的帧的高度
        cv2.VideoCapture.get(5)	    帧速率
        cv2.VideoCapture.get(6)	    编解码的4字-字符代码
        cv2.VideoCapture.get(7)	    视频文件中的帧数
        cv2.VideoCapture.get(8)	    返回对象的格式
        cv2.VideoCapture.get(9)	    返回后端特定的值，该值指示当前捕获模式
        cv2.VideoCapture.get(10)	图像的亮度(仅适用于照相机)
        cv2.VideoCapture.get(11)	图像的对比度(仅适用于照相机)
        cv2.VideoCapture.get(12)	图像的饱和度(仅适用于照相机)
        cv2.VideoCapture.get(13)	色调图像(仅适用于照相机)
        cv2.VideoCapture.get(14)	图像增益(仅适用于照相机)（Gain在摄影中表示白平衡提升）
        cv2.VideoCapture.get(15)	曝光(仅适用于照相机)
        cv2.VideoCapture.get(16)	指示是否应将图像转换为RGB布尔标志
        cv2.VideoCapture.get(17)	× 暂时不支持
        cv2.VideoCapture.get(18)	立体摄像机的矫正标注（目前只有DC1394 v.2.x后端支持这个功能）

Change History:
"""
from peutils.fileutil import list_current_file
from gooey import GooeyParser, Gooey
from ast import literal_eval
from time import strftime, gmtime
import os, cv2


def hms_s(hms):
    """
    时分秒转为秒
    @param hms: str型时分秒, eg: "00:01:30"
    @return: int型秒, eg: 90
    """
    h, m, s = hms.strip().split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def s_hms(seconds):
    """
    秒转为时分秒
    @param seconds: int型秒, eg: 30
    @return: str型时分秒, eg: "00:01:30"
    """
    return strftime("%H:%M:%S", gmtime(seconds))


def get_duration_from_cv2(filename):
    """
    @param filename: 视频文件
    @return: 视频总时长
    """
    cap = cv2.VideoCapture(filename)
    if cap.isOpened():
        rate = cap.get(5)   # 帧速率
        frame_num = cap.get(7)  # 视频文件中的帧数
        return frame_num / rate
    return -1


def split_video(video_file, start_time, interception_time, output_path):
    """
    @param video_file: 视频文件
    @param start_time: 开始时间
    @param interception_time: 截取时长
    @param output_path: 输出路径
    @return: 切割视频 并 进行视频段保存
    """
    # -t 间隔时间， -to 截止时间
    # ff = f'ffmpeg -i {video_file} -ss {start_time} -t {interception_time} -vcodec copy -acodec copy {output_path}'  # 开头会有1s黑屏
    # ff = f'ffmpeg -ss {start_time} -t {interception_time} -i {video_file} -vcodec copy -acodec copy {output_path}'  # -ss -t 放在 -i 前面 避免黑屏
    # ff = f'ffmpeg -ss {start_time} -t {interception_time} -accurate_seek -i {video_file} -vcodec copy -acodec copy {output_path}'    # -accurate_seek 剪切时间更加精确
    # ff = f'ffmpeg -ss {start_time} -t {interception_time} -accurate_seek -i {video_file} -vcodec copy -avoid_negative_ts 1 {output_path}'    # "avoid_negative_ts 1" 编码格式采用的copy, 下一片段会接上一片段最后1s
    ff = f'ffmpeg -ss {start_time} -t {interception_time} -accurate_seek -i {video_file} -vcodec copy -avoid_negative_ts 0 {output_path}'    # 编码格式采用的copy, 且无缝连接上一片段
    os.system(ff)


def interval_split(video_file, video_save_path, video_time, interval_time, video_type=".mp4"):
    """
    根据间隔切割视频
    @param video_file: 单挑视频文件
    @param video_save_path: 视频保存至目标文件夹路径
    @param video_time: 视频总时长
    @param interval_time: 间隔时间
    @param video_type: 视频类型
    @return:
    """
    video_name = os.path.basename(video_file)
    for start_time in range(0, int(video_time)+1, interval_time):
        stop_time = min(start_time + interval_time, video_time)
        # 设置目标文件名 原路径/原名_起始时间_结束时间.mp4
        target_file = os.path.join(video_save_path, video_name.replace(video_type, f"_{start_time}_{int(stop_time)}.mp4"))
        # 切割视频
        split_video(
            video_file=video_file,
            start_time=s_hms(start_time),
            interception_time=s_hms(interval_time),
            output_path=target_file
        )


def range_split(video_file, video_save_path, start, end, video_type=".mp4"):
    """
    指定起止区间切割视频
    @param video_file: 单挑视频文件
    @param video_save_path: 视频保存至目标文件夹路径
    @param start: 切割开始时间
    @param end: 切割结束时间
    @param video_type: 视频类型
    @return:
    """
    start_seconds = hms_s(start)
    end_seconds = hms_s(end)
    # 设置目标文件名 原路径/原名_起始时间_结束时间.mp4
    target_file = os.path.join(video_save_path, os.path.basename(video_file).replace(video_type, f"_{start_seconds}_{end_seconds}.mp4"))
    # 切割视频
    split_video(
        video_file=video_file,
        start_time=start,
        interception_time=s_hms(end_seconds - start_seconds),
        output_path=target_file
    )


@Gooey(program_name='视频切分工具')
def main():
    parser = GooeyParser(description=f"工具说明:\n\t1. 视频命名中带空格符均不处理")
    # 必选内容
    parser.add_argument(
        'video_original_path',
        metavar='原视频所在目录',
        widget="DirChooser",
        help='请选择原视频文件目录'
    )
    parser.add_argument(
        'video_save_path',
        metavar='生成视频存放目录',
        widget="DirChooser",
        help='请选择生成视频存放目录'
    )
    parser.add_argument(
        'input_time',
        metavar="输入时间",
        widget='TextField',
        default='10',
        help='间隔切割 eg: 以1分30秒切割(90) or (00:01:30)\n指定切割 必须是[开始时间,结束时间] eg: ["15", "30"] or ["00:00:00", "00:00:30"]'
    )
    # 可选内容
    parser.add_argument('-video_type', metavar='视频类型', widget="TextField", default='.mp4')

    args = parser.parse_args()

    video_original_path = args.video_original_path
    video_save_path = args.video_save_path
    os.makedirs(video_save_path, exist_ok=True)
    input_time = literal_eval(args.input_time) if all(s in args.input_time for s in ["[", "]"]) else args.input_time
    video_type = args.video_type

    # video_original_path = "../EthanFileData/mp4"
    # video_save_path = "outpath"
    # os.makedirs(video_save_path, exist_ok=True)
    # input_time = "10"
    # # input_time = "00:00:10"
    # # input_time = '["10", "30"]'
    # # input_time = '["00:00:15", "00:00:30"]'
    # video_type = '.mp4'
    # input_time = literal_eval(input_time) if all(s in input_time for s in ["[", "]"]) else input_time

    # 原始视频文件 -> list
    original_files = list_current_file(path=video_original_path, type="file", suffix=video_type)
    print("原始视频文件集视频条数：", len(original_files))

    for original_file in original_files:
        # 获取视频总时长
        video_total_time = get_duration_from_cv2(original_file)
        if video_total_time == -1:
            continue
        print(f"{os.path.basename(original_file)} 视频总时长: {video_total_time}")
        # 间隔切割
        if isinstance(input_time, str):
            # 转成秒
            if ":" in input_time:
                seconds = hms_s(input_time)
            else:
                seconds = int(input_time)

            interval_split(
                video_file=original_file,
                video_save_path=video_save_path,
                video_time=video_total_time,
                interval_time=seconds,
                video_type=video_type
            )

        # 指定切割
        if isinstance(input_time, list):
            start, end = input_time
            if ":" not in start:
                start = s_hms(int(start))
            if ":" in end:
                # 结束时间若大于视频总时长，则end==视频总时长
                end = end if hms_s(end) < video_total_time else s_hms(video_total_time)
            else:
                # 结束时间若大于视频总时长，则end==视频总时长
                end = s_hms(int(end)) if int(end) < video_total_time else s_hms(video_total_time)

            range_split(
                video_file=original_file,
                video_save_path=video_save_path,
                start=start,
                end=end,
                video_type=video_type
            )


if __name__ == '__main__':
    main()



