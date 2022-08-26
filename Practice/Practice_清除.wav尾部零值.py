# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/6/9 11:41

输入: 
业务逻辑描述: 
输出: 

Change History:

"""

from gooey import Gooey, GooeyParser
from pydub import AudioSegment  # 处理wav音频
import struct  # 打包字节
from peutils.fileutil import list_files_deep  # 路径下所有文件
import os
import sys

"""
# 打开一个wav文件
audio = AudioSegment.from_wav("in/00000002.wav")
print(audio.frame_rate,  # 频率  48000  48K 或 48 Hz
      audio.sample_width,  # 宽度  4 bit
      audio.frame_count(),  # 长度  651392.0
      audio.duration_seconds,  # 查看音频时长 单位：s   13.570666666666666 s
      audio.channels,  # 通道  1 单音道 2 双音道
      # audio.raw_data  # 字节数据
      )
# struct.iter_unpack(format, buffer)根据 格式字符串format 以迭代方式从缓冲区 buffer 解包。每次迭代将产生一个如格式字符串所指定的元组。返回迭代器。
# 字节顺序：按原字节(@)按原字节(=)小端(<)大端(>)网络(!), sys.byteorder来检查你的系统字节顺序
print(sys.byteorder)  # little
# 格式字符：如4bit：int(i)unsigned int(I)long(l)unsigned long(L)float(f), audio.sample_width来判断bit大小
unpack = struct.iter_unpack("<l", audio.raw_data)  # 迭代器
lst = [x[0] for x in unpack]
print(len(lst))  # 651392
# 断言：解包的数据大小是否和音频长度相等。=
assert len(lst) == int(audio.frame_count()), "检查到解析数据量不正确，请检查字节数"
"""


def process_main(in_path, out_path):
    fls = list_files_deep(in_path, suffix=".wav")
    print(f"正在处理{len(fls)}条音频数据.")
    for i, fl in enumerate(fls):
        print(f"第 {i+1} 个音频 {fl}")
        audio = AudioSegment.from_wav(fl)
        # 查看末尾0：倒序遍历读取到第一个!=0的元素时终止遍历
        lst = [x[0] for x in struct.iter_unpack("<l", audio.raw_data)][::-1]
        print(lst)
        frame_nums = int(audio.frame_count())
        assert frame_nums == len(lst), "检查到解析数据量不正确，请检查字节数"
        # 统计 第一个非0前 0出现的次数 ：270736
        count = 0
        for j in lst:
            if j == 0:
                count += 1
            else:
                break
        # get_sample_slice(start, end)通过样本索引获取音频片段的一段。
        audio_new = audio.get_sample_slice(0, frame_nums - count)
        # export(path, format="文件后缀,默认wav")
        # os.path.join(path, filename) 路径拼接文件名  os.path.basename(file)获取file的文件名
        audio_new.export(os.path.join(out_path, os.path.basename(fl)), format="wav")
    print("处理成功")


@Gooey(required_cols=1, program_name="wav 清除尾部0值")
def main():
    # 参数部分
    parser = GooeyParser(description="")
    parser.add_argument("in_path", metavar="输入路径", help="音频输入路径", widget='DirChooser')
    parser.add_argument("out_path", metavar="输出路径", help="音频输出路径", widget='DirChooser')

    # 解析和执行
    args = parser.parse_args()
    process_main(args.in_path, args.out_path)


if __name__ == '__main__':
    main()
    pass
