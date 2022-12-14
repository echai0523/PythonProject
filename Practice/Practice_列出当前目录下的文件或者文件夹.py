# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/18 16:55

input: 
output: 
Short Description: 
     - 需求：
        - 列出当前目录下的文件或者文件夹
Change History:
    - 来源：https://github.com/yunsansheng/peutils
    - 安装：pip install peutils

"""
from pathlib import Path  # 使用pathlib替换os.path 兼容windows


def list_current_file(path='.', type='all', suffix='', not_prefix=(('~', '.'))):
    """
    列出当前目录下的文件或者文件夹
    :param path: 默认当前目录
    :param type: 可选 file,folder,all 默认all
    :param suffix: 对文件夹和文件后缀过滤
    :param not_prefix: 对文件夹和文件前缀过滤，默认不要隐藏文件和临时文件
    :return:文件或文件夹的集合
    """
    p = Path(path)

    if type == 'all':
        return [x.resolve().as_posix() for x in p.iterdir()
                if x.name.endswith(suffix) and not x.name.startswith(not_prefix)]
    elif type == "file":
        return [x.resolve().as_posix() for x in p.iterdir() if
                x.is_file() and x.name.endswith(suffix) and not x.name.startswith(not_prefix)]
    elif type == "folder":
        return [x.resolve().as_posix() for x in p.iterdir() if
                x.is_dir() and x.name.endswith(suffix) and not x.name.startswith(not_prefix)]
    else:
        raise Exception(f"type: {type} not defined.")


if __name__ == '__main__':
    list_current_file()
