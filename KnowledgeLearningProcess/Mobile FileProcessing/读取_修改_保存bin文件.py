# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/15 10:55

input:
    - .bin (链接: https://pan.baidu.com/s/1nINPYOxUUesFQM-XyP2VyQ?pwd=icpy)
output:
    - value
Short Description:
    - 知识点：
        - np.fromfile(path, dtype)
        - data.tofile(path)
    - 需求：
        - 读取bin文件
        - 修改bin文件
        - 保存bin文件
Change History:

"""
import numpy as np


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
    pass


if __name__ == '__main__':
    main()
