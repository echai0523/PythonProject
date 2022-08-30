# -*- coding: UTF-8 -*-

'''
Author: Henry Wang
Date: 2021-05-05 11:17
Short Description:

Change History:

'''
import requests
import json
from minio import Minio
from datetime import timedelta
import time


TOKEN = "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDQyOTA1MTh9.smuFV5vJXtAypl74xofwuOnde_S-9Q-q55x3wiDLkg2bgUb0N_bxvkLfee3g64Ku"
FS_AGENT = "http://collect-fs-agent.cn-northwest-1.eb.amazonaws.com.cn/"


def appen_url_to_temp_url(appen_url):
    token = f"Bearer {TOKEN}"
    req_url = f"{FS_AGENT}secured-urls?path={appen_url.replace('appen://', '')}"  # http://collect-fs-agent.cn-northwest-1.eb.amazonaws.com.cn/secured-urls?path=
    url = requests.get(url=req_url, headers={"Authorization": token}).content.decode("utf-8")
    # print(url)
    return url


client = Minio(
    "collect-fs.appen.com.cn",
    secure=True,
    access_key="3IOSFODNN7EXAMPLE83G",
    secret_key="PxRfiCYEXAMPLJalrXUtnFEMI",
)

def appen_url_to_temp_with_expires(appen_url):
    if appen_url.startswith("appen://")==True:
        url = appen_url.replace("appen://","")
        bucket_name = url.split("/")[0]
        object_name = "/".join(url.split("/")[1:])
        return client.get_presigned_url("GET",bucket_name,object_name,expires=timedelta(days=3))
    else:
        return appen_url

# print(appen_url_to_temp_with_expires("appen://3565_Ake__UZB_UZB/Staging/AMR_DATA/Ake_Uzbek_UZB_UZB_UZB85078_20211210-040637/Ake_Uzbek_UZB_UZB_UZB85078_20211210-040637_0014_RDJYXX000008_01.wav"))

from argparse import ArgumentParser, FileType
import zipfile
import sys
import os
from peutils.fileutil import list_files_deep


class WooeyBaseZipFileiHander():
    '''
    project_desc: str
    need_process_suffix : str
    process_func function
    other_params a list like {"arganeme":{}} if name start with -- means option param
    {
        "arg1":{
            "help:"arg help", #not empty
            "type":int ,# not empty when it not choices.
            "default":'', #option
            "choices":['a','b','c'] #option

        },
        "--arg2":{}, option arg2
        ...
    }
    ##
    '''

    def __init__(self, project_desc, need_process_suffix, process_func, other_params=None):
        self.project_desc = project_desc
        self.need_process_suffix = need_process_suffix
        self.process_func = process_func
        self.other_params = other_params
        self.users_param = {}

    def main(self):
        parser = ArgumentParser(description=self.project_desc)
        parser.add_argument('inputfile', help='Upload your file can be sigle file or a zipfile include mutifiles',
                            type=FileType('r'))
        if self.other_params:
            for k, v in self.other_params.items():
                parser.add_argument(k, **v)

        args = parser.parse_args()
        filename = args.inputfile.name
        assert self.need_process_suffix.endswith(".zip") == False, "内容文件不能是zip格式"

        # add other param
        # users_param = {}
        if self.other_params:
            for k, v in self.other_params.items():
                # 移除非必须参数前面的-
                self.users_param[k] = getattr(args, k.lstrip("-"))

        if filename.endswith(self.need_process_suffix):
            self.process_func(filename, **self.users_param)

        elif filename.endswith(".zip"):
            print("ready to extract file")
            dir_name = os.path.dirname(filename)
            with zipfile.ZipFile(filename, 'r') as z:
                z.extractall(path=dir_name)
            print("extract finish... ready to process")
            # 解压完成后，读取文件
            files = list_files_deep(dir_name, suffix=self.need_process_suffix)
            print(f"发现待处理文件{len(files)}")

            for file in files:
                print(f"process file {file}")
                self.process_func(file, **self.users_param)
        else:
            raise Exception(f"file name suffix not endswith {self.need_process_suffix} or not zipfile")


def tp_parse(iter):
    iter = list(iter)
    assert len(iter) != 0
    if len(iter) == 1:
        if type(iter[0]) == str:
            return "('{}')".format(iter[0])
        if type(iter[0]) == int:
            return '({})'.format(iter[0])
    else:
        return tuple(iter)


def gen_uuid_seq():
    count = 0
    uuid_dict = dict()

    def new_uuid(uuid):
        nonlocal count
        nonlocal uuid_dict
        if uuid not in uuid_dict:
            count += 1
            uuid_dict[uuid] = count
        # print(uuid_dict,count)

        return uuid_dict[uuid]

    return new_uuid


### 默认从1开始
def gen_increase_seq(start=1):
    uuid_dict = dict()

    def new_uuid(uuid):
        nonlocal uuid_dict
        if uuid not in uuid_dict:
            uuid_dict[uuid] = start
        else:
            uuid_dict[uuid] = uuid_dict[uuid] + 1
        return uuid_dict[uuid]

    return new_uuid


def cal_bbox_by_polygon(polygon):
    ### 第一点和第三个点计算x,y,w,h
    bbox = [
        polygon[0]['x'],
        polygon[0]['y'],
        polygon[2]['x'] - polygon[0]['x'],
        polygon[2]['y'] - polygon[0]['y']
    ]
    assert all([x >= 0 for x in bbox]) == True, f"bbox四点坐标有错误{bbox}"
    return bbox


def get_name_without_suffix_from_path(path_like, ignore=True):
    # print(path_like)
    name = path_like.split("/")[-1]
    if ignore == False:
        assert name.count(".") == 1, "文件名存在多个.后缀或者没有.，请确认处理方式"
        name_without_suffix = name.split(".")[0]
    else:
        name_without_suffix = '.'.join(name.split(".")[:-1])
    return name_without_suffix


def save_json_by_url(data_dict):
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
    }
    json_dict = {"data": data_dict}
    json_rs = json.dumps(json_dict, ensure_ascii=False)
    rq = requests.post('https://pe.appen.com.cn/api/gen_json_url', headers=headers, data=json_rs.encode('utf-8'))
    return rq.json()["data"]["json_url"]


def download_by_url(download_url, folder, basename):
    try:
        out_file = os.path.join(folder, basename)
        rs = requests.get(download_url, stream=True)
        assert rs.status_code == 200, "请求失败"
        with open(out_file, 'wb') as f:
            for chunk in rs.iter_content(chunk_size=1024):
                f.write(chunk)
            f.flush()
        return 0  # 0代表成功

    except Exception as e:
        print('error', download_url, e, file=sys.stderr)
        return 1  # 1代表失败


def get_json_by_url(json_url):
    rs = requests.get(json_url)
    assert rs.status_code == 200, "请求不成功"
    return rs.json()


def deco_execution_time(func):
    def wrapper(*args, **kw):
        t_begin = time.time()
        res = func(*args, **kw)
        t_end = time.time()

        if t_end - t_begin < 60:
            print('%s executed in %s (s)' % (func.__name__, round(t_end - t_begin,2)) )
        elif t_end -t_begin <3600:
            print('%s executed in %s (min)' % (func.__name__, round((t_end - t_begin)/60, 2)))
        else:
            print('%s executed in %s (h)' % (func.__name__, round((t_end - t_begin) /3600, 2)))

        return res

    return wrapper

