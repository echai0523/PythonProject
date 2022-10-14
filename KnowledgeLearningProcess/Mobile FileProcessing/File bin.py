# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/15 10:55

input:
    - .bin
output:
    - value
Short Description:
    - 知识点：
        - np.fromfile(path, dtype)
        - data.tofile(path)
    - 需求：
        - bin文件补i
            - 读取指定oss路径下的bin文件
            - 数据reshape(-1, 3)转[[xyz][xyz]]补i
            - 符合转3的输出 正常处理文件file_name_list
            - 不符合的输出 异常文件error_file_name_list
Change History:

"""
import glob
import os
from argparse import ArgumentParser
import numpy


def parse_i():
    parser = ArgumentParser(description="1806 bin文件格式转换")
    parser.add_argument(
        'directory',
        help='bin文件夹oss路径, eg: oss://projecteng/0_ProjectData/upload_data/skd_f3405818f12343bfbeefa0ac418972d8',
        type=str
    )
    parser.add_argument(
        'dimension',
        help='提供的bin文件维度数',
        default='3',
        type=str
    )
    parser.add_argument(
        'method',
        help='处理方式: 补i取xyzi or 取xyzi',
        choices=['补i取xyzi', '取xyzi'],
        default='补i取xyzi',
        type=str
    )
    args = parser.parse_args()
    directory = args.directory
    dimension = int(args.dimension)
    method = args.method

    # directory = 'oss://projecteng/0_ProjectData/upload_data/skd_f3405818f12343bfbeefa0ac418972d8'
    directory = directory.split('oss:/')[1]
    # directory = /projecteng/0_ProjectData/upload_data/skd_f3405818f12343bfbeefa0ac418972d8

    """测试
    directory = '/Users/echai/Desktop/2061 bin通用脚本优化'
    dimension = 5
    method = '补i取xyzi'
    # """

    # 将directory右边切掉一个补copy文件夹
    new_directory = directory.rsplit('/', 1)[0] + '/copy'
    # new_directory = /projecteng/0_ProjectData/upload_data/copy
    os.makedirs(new_directory, exist_ok=True)

    # 存放正常处理的文件名
    file_name_list = []
    # 存放异常处理的文件名
    error_file_name_list = []
    # 指定路径下所有的bin文件
    for j in glob.glob(os.path.join(directory, '*.bin')):
        file_name = os.path.basename(j)
        data = numpy.fromfile(j, dtype="float32")
        try:
            if dimension == 3:
                assert method == '补i取xyzi', f"{dimension}维bin数据只支持: '补i取xyzi'"
            else:
                assert method in ['补i取xyzi', '取xyzi'], f"{dimension}维bin数据支持: '补i取xyzi' or '取xyzi'"

            new_data = data.reshape(-1, dimension)
            list1 = []

            for i in new_data:
                a = list(i)
                if method == '补i取xyzi':
                    a.insert(3, 0)  # 补i==0
                a = a[:4]  # 取xyzi, method设定不需要补i时直接切取xyzi
                list1.append(a)

            arr = numpy.array(list1, dtype="float32")
            # 保存补完后的bin至copy文件夹
            arr.tofile(os.path.join(new_directory, file_name))

            file_name_list.append(file_name)  # 记录正常文件名

        except Exception as e:
            print(e)
            error_file_name_list.append(file_name)  # 记录异常文件名
    print(f'发现并处理文件 {len(file_name_list)} 条：', file_name_list)
    print(f'发现异常文件 {len(error_file_name_list)} 条：', error_file_name_list)


def main():
    # 读取bin文件
    bin_path = "../../EthanFileData/1654516484442306304.bin"
    custom_single_line_bin_data = np.fromfile(bin_path, dtype=np.dtype("float32"))
    bin_result = custom_single_line_bin_data.reshape(-1, 4)
    # bin的shape [N点数, 4]
    bin_shape_0, bin_shape_1 = bin_result.shape
    print("shape -> ", bin_shape_0, bin_shape_1)
    # x, y, z, i = bin_result[22964]
    # print("22964 -> ", x, y, z, i)
    for index, _ in enumerate(bin_result):
        x, y, z, i = bin_result[index]
        print(index, "->", x, y, z, i)
        bin_result[bin_result] = x, y, z, i+1
    # 保存bin文件
    bin_result.tofile(bin_path)


if __name__ == '__main__':
    main()
    parse_i()
