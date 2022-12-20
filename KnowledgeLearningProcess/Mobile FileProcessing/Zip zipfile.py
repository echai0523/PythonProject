# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/12/2 10:29
input   : 
output  :   
Short Description:
zip文件格式是通用的文档压缩标准，在ziplib模块中，使用ZipFile类来操作zip文件，下面具体介绍一下：
    class zipfile.ZipFile(file[, mode[, compression[, allowZip64]]])
        创建一个ZipFile对象，表示一个zip文件。
        file: 文件的路径或类文件对象(file-like object)；
        mode: 打开zip文件的模式。
            默认值为'r'，表示读已经存在的zip文件，
            'w'表示新建一个zip文档或覆盖一个已经存在的zip文档，
            'a'表示将数据附加到一个现存的zip文档中。
        compression: 压缩格式，可选的压缩格式只有2个：ZIP_STORE;ZIP_DEFLATED。
            ZIP_STORE: 不压缩，默认。
            ZIP_DEFLATED: 压缩。
        allowZip64: True表示支持64位的压缩，一般而言，在所压缩的文件大于2G时，会用到这个选项；默认情况下，该值为False，因为Unix系统不支持。

    　　ZipFile还提供了如下常用的方法和属性：
            ZipFile.getinfo(name):  获取zip文档内指定文件的信息。
                返回一个zipfile.ZipInfo对象，它包括文件的详细信息。
            ZipFile.infolist()      获取zip文档内所有文件的信息
                返回一个zipfile.ZipInfo的列表。
            ZipFile.namelist()      获取zip文档内所有文件的名称列表。
            ZipFile.extract(member[, path[, pwd]])  将zip文档内的指定文件解压到当前目录。
                member: 指定要解压的文件名称或对应的ZipInfo对象；
                path: 指定了解析文件保存的文件夹；
                pwd: 解压密码。下面一个例子将保存在程序根目录下的txt.zip内的所有文件解压到D:/Work目录：
            ZipFile.extractall([path[, members[, password]]])    解压zip文档中的所有文件到当前目录。
                path: 解压缩目录。
                members: 默认值为zip文档内的所有文件名称列表，也可以自己设置，选择要解压的文件名称。
                password: 当zip文件有密码时需要该选项
            ZipFile.printdir()  将zip文档内的信息打印到控制台上。
            ZipFile.setpassword(pwd)    设置zip文档的密码。
            ZipFile.read(name[, pwd])   获取zip文档内指定文件的二进制数据。
                下面的例子演示了read()的使用，zip文档内包括一个txt.txt的文本文件，使用read()方法读取其二进制数据，然后保存到D:/txt.txt。
Change History:
"""
import zipfile, os


zip_file = "../../EthanFileData/Zip/zip_test.zip"

"""
# 判断文件是否为zip文件
if zipfile.is_zipfile(zip_file):
    # 创建一个ZipFile对象，表示一个zip文件
    ZipFile = zipfile.ZipFile(
        file=zip_file,  # 文件的路径或类文件对象(file-like object)
        mode="r",  # 打开zip文件的模式。默认值为'r'读已经存在的zip文件，'w'新建或覆盖zip文档，'a'现存zip文档追加数据。
        compression=zipfile.ZIP_STORED,  # 压缩格式，可选的压缩格式只有2个: ZIP_STORE(不压缩); ZIP_DEFLATED(压缩)。
        allowZip64=True,  # True支持64位的压缩，在所压缩的文件大于2G时使用True；默认情况下，该值为False，因为Unix系统不支持
        compresslevel=None
    )
    # zip中所有文件(带解压路径eg:['zip_test/', 'zip_test/lidar_label.json', '__MACOSX/zip_test/._lidar_label.json'])
    for name in ZipFile.namelist():
        # 排除 mac解压包、解压文件夹
        if name.startswith("__MACOSX/") or name.endswith('/'):
            #  打开压缩文档中的某个文件
            OpenFile = ZipFile.open(
                name=name,  # ZIP文件中的文件名的字符串，或ZipInfo对象。
                mode="r",
                pwd=None,   # 解密文件的密码(仅用于读取)
                force_zip64=False  # 写文件时，ZIP64格式，可以处理大(可能超过2G)的文件。
            )
            ZipFile.infolist()
            # 获取文件信息
            ZipInfo = ZipFile.getinfo(name)
            print('filename:', ZipInfo.filename)
            print('date_time:', ZipInfo.date_time)
            print('compress_type:', ZipInfo.compress_type)
            print('comment:', ZipInfo.comment)
            print('extra:', ZipInfo.extra)
            print('create_system:', ZipInfo.create_system)
            print('create_version:', ZipInfo.create_version)
            print('extract_version:', ZipInfo.extract_version)
            print('extract_version:', ZipInfo.reserved)
            print('flag_bits:', ZipInfo.flag_bits)
            print('volume:', ZipInfo.volume)
            print('internal_attr:', ZipInfo.internal_attr)
            print('external_attr:', ZipInfo.external_attr)
            print('header_offset:', ZipInfo.header_offset)
            print('CRC:', ZipInfo.CRC)
            print('compress_size:', ZipInfo.compress_size)
            print('file_size:', ZipInfo.file_size)
    # 关闭zip
    ZipFile.close()
"""
from peutils.transform.v1.base import get_session
from io import BytesIO


zip_url = "https://github.com/echai0523/PythonProject/raw/main/EthanFileData/Zip/63880a3f0b385136692fbf0e.zip"
s = get_session().get(zip_url).content
ZipFile = zipfile.ZipFile(
    file=BytesIO(s),  # 文件的路径或类文件对象(file-like object)
    mode="r",  # 打开zip文件的模式。默认值为'r'读已经存在的zip文件，'w'新建或覆盖zip文档，'a'现存zip文档追加数据。
    compression=zipfile.ZIP_STORED,  # 压缩格式，可选的压缩格式只有2个: ZIP_STORE(不压缩); ZIP_DEFLATED(压缩)。
    allowZip64=True,  # True支持64位的压缩，在所压缩的文件大于2G时使用True；默认情况下，该值为False，因为Unix系统不支持
    compresslevel=None
)
print(ZipFile.namelist())
for name in ZipFile.namelist():
    print(name)

    # if name.startswith("__MACOSX/") or name.endswith('/'):
    if not (name.endswith('/') or name.startswith("__MACOSX/")):
        # 编码问题参考：https://blog.csdn.net/qq_21076851/article/details/122752196
        name_decode = name.encode('cp437').decode('utf-8')
        foldername, filename = os.path.split(name_decode)
        os.makedirs(f"{os.path.basename(zip_url)[:-4]}/{foldername}", exist_ok=True)

        # 写文件操作
        data = ZipFile.read(name)
        (lambda f, d: (f.write(d), f.close()))(open(f"{os.path.basename(zip_url)[:-4]}/{foldername}/{filename}", 'wb'), data)

ZipFile.close()

# zipFile = zipfile.ZipFile(os.path.join(os.getcwd(), 'txt.zip'))
# for file in zipFile.namelist():
#     zipFile.extract(file, r'd:/Work')
# zipFile.close()
#
# zipFile = zipfile.ZipFile(os.path.join(os.getcwd(), 'txt.zip'))
# data = zipFile.read('txt.txt')
# (lambda f, d: (f.write(d), f.close()))(open(r'd:/txt.txt', 'wb'), data)  #一行语句就完成了写文件操作。仔细琢磨哦~_~
# zipFile.close()
