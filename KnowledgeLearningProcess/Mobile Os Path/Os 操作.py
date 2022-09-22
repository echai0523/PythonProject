# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/22 17:50

input: 
output: 
Short Description:
    - 知识点：
        - os.getcwd()       当前工作目录
        - os.chdir(path)    切换目录
        - os.mkdir(name, mode, dir_fd)        创建目录 创建一级目录
        - os.makedirs(name, mode=0o777, exist_ok=False)  创建目录 创建多层目录
            - name：目录名
            - mode：要为目录设置的权限数字模式，默认的模式为 0o777 (八进制)。
            - exist_ok：是否在目录存在时触发异常。如果exist_ok为False（默认值），则目录已存在的触发FileExistsError异常；如果exist_ok为True，则目录已存在不会触发FileExistsError异常。
        - os.close()        关闭文件
        - os.sep            根据你所处的平台，自动采用相应的分隔符号。
        - os.sep.join() 自动采用相应的分隔符号拼接路径
        - os.getmtime() 修改时间，给出自纪元以来的秒数
        - os.stat()         查看文件属性(给出自纪元以来的秒数)
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

Change History:

"""
import os
from datetime import datetime


def os_getcwd():
    """当前目录"""
    p1 = os.getcwd()
    print(p1)


def os_chdir():
    """切换目录"""
    os.chdir(r"C:\Users\echai\Downloads\process\660 humor物流小车2d单连续帧通用")
    p1 = os.getcwd()
    print(p1)


def os_stat():
    """获取文件属性"""
    file_attr = os.stat("filepath")
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


def main():
    # 当前目录
    os_getcwd()
    # 切换目录
    os_chdir()
    # 获取文件属性
    os_stat()


if __name__ == '__main__':
    main()
