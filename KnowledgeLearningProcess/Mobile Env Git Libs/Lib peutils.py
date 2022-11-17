# -*- coding: UTF-8 -*-

# 音频
from peutils.transform.v1.audio_seg import parser

parser.AudioSegFrame.add_frame_obj()
# 文件
from peutils.fileutil import list_current_file
'''
列出当前目录下的文件或者文件夹
:param path: 默认当前目录
:param type: 可选 file,folder,all 默认all
:param suffix: 对文件夹和文件后缀过滤
:param not_prefix: 对文件夹和文件前缀过滤，默认不要隐藏文件和临时文件
:return:文件或文件夹的集合
'''
from peutils.fileutil import list_files_deep
'''
:param path: 默认当前目录 '.'
:param suffix: 文件后缀，单个或者元组
:param not_prefix: 单个或者元组,默认去掉隐藏文件和临时文件
:return: 文件全路径集合
'''
from peutils.fileutil import replace_path_and_create
"""echai 添加注释
修改文件路径并返回新的文件路径，不创建路径
:param filepath: 需要处理的文件路径或文件名
:param old_dir: 该文件的旧路径  # 脚本同路径 可写为 r''
:param new_dir: 该文件的新路径  # 文件同路径下的文件夹 r'xxx'
:param add_path: 为新文件路径添加路径，如文件上级添加一个t1文件夹：["t1"]，文件上级添加c2,c2上级再添加c1：["c1","c2"]。不需要添加可写[]。
:return: 新的文件路径
"""
'''
自定义方法，从A目录到B目录，找到对应后缀文件，循环并生成新的文件
'''
from peutils.fileutil import Hanlde_Move_File
'''
文件名相同的情况下检查文件对齐,不同后缀文件数量对齐,可以在相同文件夹，也可以在不同文件夹
'''
from peutils.fileutil import getCsvData
from peutils.fileutil import saveCsvData
from peutils.fileutil import getExcelData
from peutils.fileutil import saveExcelData


from peutils.datautil import unique   # 去重 # list unique、file unique、csv unique
from peutils.datautil import gen_uuid_seq  # 随机安排a b c d


from peutils.image_util import DrawMaskCls
'''
DrawMaskCls.get_image_meta()
DrawMaskCls.gen_mask_layer()
DrawMaskCls.transfer_color_code()
DrawMaskCls.getObjPoints()
DrawMaskCls.combine_mask_and_origin()
DrawMaskCls.main_result()
'''


from peutils.mailutil import SendEmail  # 发邮件


from peutils.pcd_py3 import parse_header
from peutils.pcd_py3 import write_header
from peutils.pcd_py3 import _metadata_is_consistent
from peutils.pcd_py3 import _build_dtype
from peutils.pcd_py3 import build_ascii_fmtstr
from peutils.pcd_py3 import parse_ascii_pc_data
from peutils.pcd_py3 import parse_binary_pc_data
from peutils.pcd_py3 import parse_binary_compressed_pc_data
from peutils.pcd_py3 import point_cloud_from_fileobj
from peutils.pcd_py3 import point_cloud_from_path
from peutils.pcd_py3 import point_cloud_from_buffer
from peutils.pcd_py3 import point_cloud_to_fileobj
from peutils.pcd_py3 import PointCloud
'''
PointCloud.get_metadata()
PointCloud.check_sanity()
PointCloud.from_path()
PointCloud.from_buffer()
'''


from peutils.textutil import gen_uuid  # 由伪随机数得到，有一定的重复概率， 返回值去掉了-
from peutils.textutil import md5_file  # md5文件解码
from peutils.textutil import gen_date_str  # 获取当前日期时间 并 设置格式
from peutils.textutil import strip_and_replace_blank  # 去掉前后空格，多个空格变成一个空格


from peutils.toolutil import remove_key_if_exists  # 删除”字典key中“存在”列表中的某数据“
from peutils.toolutil import get_name_without_suffix_from_path  # 去掉文件后缀


from peutils.wooeyutil import unzipfile  # 解压文件
from peutils.wooeyutil import packzipfile  # 指定输出路径和列表，打包路径
from peutils.wooeyutil import WooeyBaseZipHandlerFile
'''WooeyBaseZipHandlerFile.main()
支持单个压缩包文件中存放单种类型的文件(不支持zip种存放zip)
支持文件逐一处理
'''
from peutils.wooeyutil import WooeyBaseZipHandlerFileList
'''WooeyBaseZipHandlerFileList.main()
支持单个压缩包文件中存放单种类型的文件(不支持zip种存放zip)
文件批量读取后一起处理
'''


def main():
    pass


if __name__ == "__main__":
    main()
