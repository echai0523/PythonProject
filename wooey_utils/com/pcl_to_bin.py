# -*- coding: UTF-8 -*-

'''
Author: Henry Wang
Date: 2021-08-10 13:22
Short Description:

Change History:

'''
import asyncio
import aiohttp
import uvloop
import time
from wooey_utils.com.oss_tool import OSS_API
from wooey_utils.com.config import *
from wooey_utils.com.base_tools import get_name_without_suffix_from_path
import os
import sys
import json

# 设置事件循环为uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


headers = {"Content-Type":"application/json"}
semaphore = asyncio.Semaphore(10)

async def request_data(session,url,data):
    async with session.post(url,json=data,headers=headers) as resp:
        print(resp.status)
        rs = await resp.text()
        # await asyncio.sleep(1)
        return data, resp.status, rs

async def request_data_with_retry(session,url,data):
    tries = 3
    while tries > 0:
        try:
            return await request_data(session, url, data)
        except aiohttp.ClientResponseError:
            if tries <= 0:
                raise Exception("请求错误超过3次")
        tries -= 1

async def process_one(path_pair):
    # url = f"http://192.168.0.75/pcl-to-bin"
    # url = "http://192.168.0.118:30100"
    url = f"{PROCESS_API_HOST}/pcl-to-bin"
    data = {
        "in_fname":path_pair[0],
        "out_fname":path_pair[1],
        "use_cache":True
    }
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            rs = await request_data_with_retry(session,url=url,data=data)
            return rs


def process_by_sub_path(bucket_name,oss_obj,sub_batch_path_list:list,addition_og,addition_out):
    # if sub_batch_path.endswith("/") ==False:
    #     sub_batch_path =sub_batch_path +"/"
    # sub_name = sub_batch_path.split("/")[-2] # -1是空，所以取-2

    path_pairs = []
    for sub_batch_path in sub_batch_path_list:
        files = oss_obj.list_bucket_files_deep(oss_path=os.path.join(sub_batch_path, *addition_og), suffix='.pcd',
                                               with_bucket_name=True)
        path_pairs.extend([(x,
                   os.path.join(f'/{bucket_name}', sub_batch_path, *addition_out,
                                get_name_without_suffix_from_path(x) + ".bin")
                   ) for x in files])
    #
    # path_pairs = [(x,
    #                os.path.join(f'/{bucket_name}', sub_batch_path, *addition_out,
    #                             get_name_without_suffix_from_path(x) + ".bin")
    #                ) for x in files]
    # path_pairs = [("/projecteng/haomo/test/HDR000_20210121101710-1611195638500934-1611195643705539/point_cloud/pcd/four_lidar/1611195638499741.pcd","/projecteng/test/temp/1611195638499741.bin"),
    #       ("/projecteng/haomo/test/HDR000_20210121101710-1611195638500934-1611195643705539/point_cloud/pcd/four_lidar/1611195638499741.pcd","/projecteng/test/temp/1611195638499742.bin")]
    print("find files", len(path_pairs),"start", time.time())

    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(process_one(path_pair)) for path_pair in path_pairs]

    tasks = asyncio.gather(*tasks)
    res = loop.run_until_complete(tasks)
    loop.close()
    ## 分别是 data,http_code和返回的json字符串
    ## http code不等于200的。或者数据中的code不是200
    erros = [x for x in res if x[1] != 200 or json.loads(x[2])["code"] != 200]
    if len(erros) != 0:
        print("发现错误条数，请查阅错误的文件", len(erros), file=sys.stderr)
        with open(f"errors_data.log", 'a') as fw:
            for er in erros:
                fw.write(json.dumps(er[0], ensure_ascii=False) + "\n")
    else:
        for sub_batch_path in sub_batch_path_list:
            bins = oss_obj.list_bucket_files_deep(oss_path=os.path.join(sub_batch_path, *addition_out), suffix='.bin',
                                           with_bucket_name=True)
            pcls = oss_obj.list_bucket_files_deep(oss_path=os.path.join(sub_batch_path, *addition_og), suffix='.pcd',
                                           with_bucket_name=True)
            if len(pcls)==len(bins):
                print(f"{sub_batch_path}数据转换成功 {len(bins)}")
            else:
                print(f"{sub_batch_path}发现转换数量不一致",len(pcls),len(bins),file=sys.stderr)



def main_process(batch_path,has_multi,addition_og,addition_out):
    assert batch_path.startswith("/")==True,"路径必须以/开头"
    bucket_name = batch_path.split("/")[1]
    oss_obj = OSS_API(bucket_name=bucket_name)

    if has_multi =='false': # 没有子文件夹需要解析
        batch_path_without_bucket_name = "/".join(batch_path.split("/")[2:])
        print("处理路径:",batch_path_without_bucket_name)
        batch_path_without_bucket_name_list = [batch_path_without_bucket_name]
        process_by_sub_path(bucket_name,oss_obj,batch_path_without_bucket_name_list,addition_og,addition_out)

    elif has_multi =='true': # 有子文件需要解析
        batch_path_without_bucket_name = "/".join(batch_path.split("/")[2:])
        folders= oss_obj.list_bucket_current(batch_path_without_bucket_name,list_type="folder")
        print("发现组内处理路径",folders)
        batch_path_without_bucket_name_list =[]
        for folder in folders:
            batch_path_without_bucket_name_list.append(folder)

        process_by_sub_path(bucket_name,oss_obj,batch_path_without_bucket_name_list,addition_og,addition_out)

if __name__ =="__main__":
    main_process(
        batch_path = "/projecteng/haomo_3d/segmentation/test/gp1",
        has_multi = "false", # true或者 false
        addition_og = ["point_cloud","pcd"],
        addition_out =  ["point_cloud","bin_v1"]
    )
