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
        - os.renames(old, new)      文件重命名(文件需要带绝对路径，同时可以实现剪切粘贴移动文件)
        - os.close()        关闭文件
        - os.sep            根据你所处的平台，自动采用相应的分隔符号。
            - python是跨平台的。在Windows上，文件的路径分隔符是'\'，在mac上是'/'。为了让代码在不同的平台上都能运行，那么路径应该写'\'还是'/'呢？
        - os.sep.join() 自动采用相应的分隔符号拼接路径
        - os.getmtime() 修改时间，给出自纪元以来的秒数
        - os.stat()         查看文件属性(给出自纪元以来的秒数)
            - st_mode   （保护位）
            - st_ino    （索引节点号）
            - st_dev    （设备）
            - st_nlink  （硬链接数）
            - st_uid    （所有者的用户ID）
            - st_gid    （所有者的组ID）
            - st_size   （文件大小，以字节为单位）
            - st_atime  （最新访问时间）
            - st_mtime  （最新内容修改时间）
            - st_ctime  （取决于平台；最新元数据更改的时间）在Unix上，或在Windows上创建的时间）

        - os.path.abspath(path) 	    返回绝对路径
        - os.path.basename(path)    	返回文件名
        - os.path.commonprefix(list)    返回list(多个路径)中，所有path共有的最长的路径
        - os.path.dirname(path) 	    返回文件路径(去除文件名的路径)
        - os.path.exists(path)  	    如果路径 path 存在，返回 True；如果路径 path 不存在，返回 False。
        - os.path.lexists   	        路径存在则返回True,路径损坏也返回True
        - os.path.expanduser(path)  	把path中包含的"~"和"~user"转换成用户目录
        - os.path.expandvars(path)  	根据环境变量的值替换path中包含的"$name"和"${name}"
        - os.path.getatime(path)    	返回最近访问时间（浮点型秒数）
        - os.path.getmtime(path)    	返回最近文件修改时间
        - os.path.getctime(path)    	返回文件 path 创建时间
        - os.path.getsize(path) 	    返回文件大小，如果文件不存在就返回错误
        - os.path.isabs(path)   	    判断是否为绝对路径
        - os.path.isfile(path)  	    判断路径是否为文件
        - os.path.isdir(path)   	    判断路径是否为目录
        - os.path.islink(path)  	    判断路径是否为链接
        - os.path.ismount(path) 	    判断路径是否为挂载点
        - os.path.join(path1[, path2[, ...]])   	把目录和文件名合成一个路径
        - os.path.normcase(path)    	转换path的大小写和斜杠
        - os.path.normpath(path)    	规范path字符串形式
        - os.path.realpath(path)    	返回path的真实路径
        - os.path.relpath(path[, start])    	    从start开始计算相对路径
        - os.path.samefile(path1, path2)    	    判断目录或文件是否相同
        - os.path.sameopenfile(fp1, fp2)    	    判断fp1和fp2是否指向同一文件
        - os.path.samestat(stat1, stat2)    	    判断stat tuple stat1和stat2是否指向同一个文件
        - os.path.split(path)   	    把路径分割成 dirname 和 basename，返回一个元组
        - os.path.splitdrive(path)  	一般用在 windows 下，返回驱动器名和路径组成的元组
        - os.path.splitext(path)    	分割路径，返回路径名和文件扩展名的元组
        - os.path.splitunc(path)    	把路径分割为加载点与文件
        - os.path.walk(path, visit, arg)    	    遍历path，进入每个目录都调用visit函数，visit函数必须有3个参数(arg, dirname, names)，dirname表示当前目录的目录名，names代表当前目录下的所有文件名，args则为walk的第三个参数
        - os.path.supports_unicode_filenames    	设置是否支持unicode路径名
Change History:

"""
import os
import time
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


def os_sep():
    sep = os.sep
    # 当前平台采用的分隔符号
    print(sep)
    # path_join = f'{sep}'.join(['a', 'b'])

    # path_join_win = os.sep.join([r"C:\Users\echai\PycharmProjects\PythonProject\FunctionZone", "Os_And_Csv"])
    # print(path_join_win)
    path_join_mac = os.sep.join([r"/Users/echai/PycharmProjects/PythonProject/FunctionZone", "Os_And_Csv"])
    print(path_join_mac)


def os_renames():
    from peutils.fileutil import list_current_file

    pth = r'/Users/PycharmProjects/SecretDocument/test'

    files = list_current_file(pth, type='file', suffix='.png')
    # 将1.png移动到SecretDocument下
    for file in files:
        # file = '/Users/PycharmProjects/SecretDocument/test/1.png'
        new = file.replace('test/', '')
        os.renames(file, new)

    # 1.png文件 重命名/转格式
    files = list_current_file(pth, type='file', suffix='.png')
    for file in files:
        # file = '/Users/PycharmProjects/SecretDocument/test/1.png'
        new = file.replace('.png', '.jpg')
        os.renames(file, new)


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


def os_path():
    file = '/root/test/runoob.Txt'  # 文件路径

    print("返回文件名: ", os.path.basename(file))  # 返回文件名
    print("返回目录路径: ", os.path.dirname(file))  # 返回目录路径 /root/test
    print("分割文件名与路径: ", os.path.split(file))  # 分割/root/test/runoob.txt文件名与路径 ('/root/test', 'runoob.Txt')
    print("分割文件夹名与路径: ", os.path.split(os.path.dirname(file)))  # 分割/root/test文件夹名与路径 ('/root', 'test')
    print("分割路径与文件后缀", os.path.splitext(file))  # 分割路径，返回路径名和文件扩展名的元组('/root/test/runoob', '.Txt')
    print("将目录和文件名合成一个路径: ", os.path.join('root', 'test', 'runoob.Txt'))  # 将目录和文件名合成一个路径

    print("输出最近访问时间: ", os.path.getatime(file))  # 输出最近访问时间
    print("输出文件创建时间: ", os.path.getctime(file))  # 输出文件创建时间
    print("输出最近修改时间: ", os.path.getmtime(file))  # 输出最近修改时间
    print("以struct_time形式输出最近修改时间: ", time.gmtime(os.path.getmtime(file)))  # 以struct_time形式输出最近修改时间
    print("输出文件大小: ", os.path.getsize(file))  # 输出文件大小（字节为单位）
    print("输出绝对路径: ", os.path.abspath(file))  # 输出绝对路径
    print("规范path字符串形式: ", os.path.normpath(file))  # 规范path字符串形式


def main():
    # # 当前目录
    # os_getcwd()
    # # 切换目录
    # os_chdir()
    # # 分隔符号
    os_sep()
    # 文件重命名/迁移
    # os_renames()
    # # 获取文件属性
    # os_stat()

    # 文件路径
    # os_path()


if __name__ == '__main__':
    main()
