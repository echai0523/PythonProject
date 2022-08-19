# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/18 15:31

input:

output: 
Short Description: 
    - 知识点：
        - os.getmtime() 修改时间，给出自纪元以来的秒数
        - os.stat() 给出自纪元以来的秒数
            - st_mode（保护位）
            - st_ino（索引节点号）
            - st_dev（设备）
            - st_nlink（硬链接数）
            - st_uid（所有者的用户ID）
            - st_gid（所有者的组ID）
            - st_size（文件大小，以字节为单位）
            - st_atime（最新访问时间）
            - st_mtime （最新内容修改时间）
            - st_ctime （取决于平台；最新元数据更改的时间）在Unix上，或在Windows上创建的时间）
        - datetime.fromtimestamp() 秒数转为时间类型
    - 需求：
        读取文件修改时间、保存时间、访问时间，按行写入csv或txt
Change History:

"""
import os
from datetime import datetime
import pandas as pd


def main():
    file_attr = os.stat(filepath)
    # os.stat_result(st_mode=33206, st_ino=16044073672860753, st_dev=716125111, st_nlink=1, st_uid=0, st_gid=0, st_size=411, st_atime=1660807956, st_mtime=1660803331, st_ctime=1660803210)
    print(file_attr)
    # 访问时间
    atime = datetime.fromtimestamp(file_attr.st_atime)
    print(atime)  # 2022-08-18 15:32:36.271877
    # 修改时间
    mtime = datetime.fromtimestamp(file_attr.st_mtime)
    print(mtime)  # 2022-08-18 14:15:31.282147
    # 创建时间
    ctime = datetime.fromtimestamp(file_attr.st_ctime)
    print(ctime)  # 2022-08-18 14:13:30.340448

    df = pd.DataFrame()


if __name__ == '__main__':
    filepath = 'filepath.txt'
    main()
