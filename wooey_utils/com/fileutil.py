# -*- coding: UTF-8 -*-

'''
Author: Henry Wang
Date: 2021-05-25 14:14
Short Description:

Change History:

'''

from pathlib import Path
import os,sys
from functools import partial
from concurrent import futures



def list_current_file(path='.', type='all', suffix='', not_prefix=(('~', '.'))):
    '''
    列出当前目录下的文件或者文件夹
    :param path: 默认当前目录
    :param type: 可选 file,folder,all 默认all
    :param suffix: 对文件夹和文件后缀过滤
    :param not_prefix: 对文件夹和文件前缀过滤，默认不要隐藏文件和临时文件
    :return:文件或文件夹的集合
    '''
    p = Path(path)

    if type == 'all':
        return [x.resolve().as_posix() for x in p.iterdir()
                if x.name.endswith(suffix) and not x.name.startswith(not_prefix)]
    elif type == "file":
        return [x.resolve().as_posix() for x in p.iterdir() if x.is_file() and  x.name.endswith(suffix) and not x.name.startswith(not_prefix)]
    elif type == "folder":
        return [x.resolve().as_posix() for x in p.iterdir() if x.is_dir() and  x.name.endswith(suffix) and not x.name.startswith(not_prefix)]
    else:
        raise Exception(f"type: {type} not defined.")


def list_files_deep(path='.', suffix='', not_prefix=(('~', '.'))):
    '''
    :param path: 默认当前目录 '.'
    :param suffix: 文件后缀，单个或者元组
    :param not_prefix: 单个或者元组,默认去掉隐藏文件和临时文件
    :return: 文件全路径集合
    '''
    files = []
    all_files = list(Path(path).glob('**/*.*'))  # 过滤出来的是文件

    # # Henry Wang, 2021-01-28 14:01 Changed:将suffix转成小写
    if isinstance(suffix,str)==True:
        suffix = suffix.lower()
    elif isinstance(suffix,tuple) ==True:
        suffix = tuple([x.lower() for x in suffix])

    # Henry Wang, 2021-05-25 14:18 Changed:增加os.path.isfile的判断
    for filpath in all_files:
        if filpath.is_file() ==True and filpath.name.lower().endswith(suffix) and not filpath.name.startswith(not_prefix):
            files.append(filpath.resolve().as_posix())

    return files


def replace_path_and_create(filepath, old_dir, new_dir, add_path: list):
    old_dir = Path(old_dir)
    new_dir = Path(new_dir)
    filepath = Path(filepath)

    if old_dir.resolve().as_posix() in filepath.resolve().as_posix():
        new_fl = filepath.resolve().as_posix().replace(old_dir.resolve().as_posix(), new_dir.resolve().as_posix())
        if add_path != None:
            p = Path(new_fl).resolve()
            new_fl = p.parent.joinpath(*add_path, p.name).resolve().as_posix()
        return new_fl
    else:
        raise Exception(f"{old_dir} not in {new_dir}")


class Hanlde_Move_File_MULTI():
    def __init__(self, origin_path, out_path, process_func, in_suffix, out_suffix, add_path=None,default_workers=8):
        self.origin_path = origin_path
        self.out_path = out_path
        self.change_path = partial(replace_path_and_create, old_dir=origin_path, new_dir=out_path,
                                   add_path=add_path)  # 只要传filepath
        self.process_func = process_func
        self.in_suffix = in_suffix.strip()
        self.out_suffix = out_suffix.strip()
        self.add_path = add_path
        self.default_workers = default_workers

    def process_one(self,filename):
        try:
            out_change_path = self.change_path(filename)[:-len(self.in_suffix)] + self.out_suffix
            out_path_parent = Path(out_change_path).resolve().parent
            out_path_parent.mkdir(parents=True, exist_ok=True)  # 递归创建目录，如果已存在不报错
            self.process_func(filename, out_change_path)
        except Exception as e:
            print(f'filename  {filename} Error{e}')
            print(f'filename  {filename} Error{e}',file=sys.stderr)

    def main(self):
        print(f'handle {self.process_func.__name__.upper()} from: {self.origin_path} to: {self.out_path}')
        files = list_files_deep(self.origin_path, suffix=self.in_suffix)
        print(f'处理文件总数: {len(files)}')
        out_pre_file = list_files_deep(self.out_path, suffix=self.out_suffix)
        if len(out_pre_file) != 0:
            print(f'Warining: 目标文件夹，该类型文件存在 {out_pre_file} 个历史文件，请确认操作，无问题可忽略本提示')

        workers = min(self.default_workers, len(files))
        with futures.ThreadPoolExecutor(workers) as executor:
            res = executor.map(self.process_one, files)

        out_file = list_files_deep(self.out_path, suffix=self.out_suffix)
        print(f"输出文件总数: {len(out_file)}")
        if len(out_file)!=len(files):
            print(f"输入输出文件数量不一致，请确认，输入{len(files)}，输出{len(out_file)}")
            print(f"输入输出文件数量不一致，请确认，输入{len(files)}，输出{len(out_file)}",file=sys.stderr)

