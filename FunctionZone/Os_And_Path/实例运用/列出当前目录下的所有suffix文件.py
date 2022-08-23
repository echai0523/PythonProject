# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/18 16:55

input:
output:
Short Description:
     - 需求：
        - 列出当前目录下的所有suffix文件
Change History:
    - 来源：https://github.com/yunsansheng/peutils
    - 安装：pip install peutils

"""
from pathlib import Path  # 使用pathlib替换os.path 兼容windows


def list_files_deep(path='.', suffix='', not_prefix=(('~', '.'))):
    """
    列出当前目录下的所有suffix文件
    :param path: 默认当前目录 '.'
    :param suffix: 文件后缀，单个或者元组
    :param not_prefix: 单个或者元组,默认去掉隐藏文件和临时文件
    :return: 文件全路径集合
    """
    files = []
    all_files = list(Path(path).glob('**/*.*'))  # 过滤出来的是文件

    # 将suffix转成小写
    if isinstance(suffix, str) == True:
        suffix = suffix.lower()
    elif isinstance(suffix, tuple) == True:
        suffix = tuple([x.lower() for x in suffix])

    # 增加os.path.isfile的判断
    for filpath in all_files:
        if filpath.is_file() == True and filpath.name.lower().endswith(suffix) and not filpath.name.startswith(
                not_prefix):
            files.append(filpath.resolve().as_posix())

    return files


if __name__ == '__main__':
    list_files_deep()
