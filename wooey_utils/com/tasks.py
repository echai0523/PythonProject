# -*- coding: UTF-8 -*-

'''
Author: Henry Wang
Date: 2021-09-02 14:09
Short Description:

Change History:

'''

import asyncio
import aiohttp
import uvloop
import os,sys
from argparse import ArgumentParser,FileType
import zipfile
import pandas as pd
import json
from peutils.textutil import gen_uuid
import os
from .oss_tool import OSS_API
from .packfile import packzipfilev1


from wooey_utils.com.base_tools import deco_execution_time
from wooey_utils.com.base_tools import list_files_deep
from peutils.fileutil import saveCsvData

from wooey_utils.com.oss_tool import OSS_STS_AUTH_Authorize


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

'''
输入 
    - 文件参数,单个csv 或者 压缩包
    - 其他参数
'''

import math
def gen_format_progress_seq(total,split_part=10):
    ###初始化
    total = total # 总的数量
    split_part = split_part # 分片数量
    every_part_num = math.ceil(total/split_part) # 总打印的分片数量

    finish = 0  # 当前完成的数量
    finish_part = 0 # 分配开始的进度数量
    # 分片数量，假如 总量是102，分片是10
    def update(step=1):
        nonlocal finish,finish_part
        finish += step # 每调用一次 加1
        if finish//every_part_num >finish_part and finish//every_part_num <=split_part:
            finish_part+=1 # 分片数量加 1
            print( "[",("*"*finish_part).ljust(split_part,"_") ,"]" )
        # 根据完成数量update进度
    return update


class CommonDataParseV1():
    project_desc = None
    need_process_suffix = ".csv"
    other_params =dict()

    cols = ["Batch Num", "Record ID", "annotation"]
    parse_url = None

    ###以下参数一般不要改
    headers = {"Content-Type": "application/json"}
    async_task_nums = 10
    mode="save"
    save_way = "nas"
    pack_zip = False  # 只有save_way是oss的时候True才打包

    api_use_cache = False




    def __init__(self):
        self.temp_dir,self.work_dir = self.get_temp_dir_and_work_dir()
        self.args = self.get_parse_args()
        self.users_param = self.get_users_param(self.args)
        self.format_progress = lambda :None

    def get_temp_dir_and_work_dir(self):
        print("存储方式: ",self.save_way,"启用缓存: ",self.api_use_cache)

        if self.save_way =="nas":
            temp_dir = os.getcwd()
            resut_dir = os.path.join(temp_dir, "result")
            os.makedirs(resut_dir)
        elif self.save_way =="oss":
            # 随机在projecteng下生成一个文件
            temp_dir = os.path.join("/appen-delivery/process_rs/", gen_uuid())
            os.makedirs(temp_dir)  # 创建这个目录
            resut_dir = os.path.join(temp_dir, "result")
            if temp_dir.endswith("/") == False:
                temp_dir = temp_dir + "/"
        else:
            raise Exception("保存方式只能是nas或者oss")

        return temp_dir, resut_dir


    # @deco_execution_time
    def get_parse_args(self):
        if self.project_desc is None:
            raise NotImplementedError("please set the project_desc")
        parser = ArgumentParser(description=self.project_desc)
        parser.add_argument('inputfile', help='Upload your file can be sigle file or a zipfile include mutifiles',
                            type=FileType('r'))
        if self.other_params:
            for k,v in self.other_params.items():
                parser.add_argument(k,**v)
        args = parser.parse_args()

        return args

    # @deco_execution_time
    def get_users_param(self,args):
        users_param = dict()
        if self.other_params:
            for k,v in self.other_params.items():
                # 移除非必须参数前面的-
                users_param[k] = getattr(args,k.lstrip("-") )
        return users_param

    # @deco_execution_time
    def get_process_task_files(self,inputfilename):

        assert self.need_process_suffix.endswith(".zip")==False,"需要处理的独立文件不能是zip"
        if inputfilename.endswith(self.need_process_suffix):
            return [inputfilename]
        else:
            dir_name = os.path.dirname(inputfilename)
            with zipfile.ZipFile(inputfilename, 'r') as z:
                z.extractall(path=dir_name)
            # 解压完成后，读取文件
            files = list_files_deep(dir_name, suffix=self.need_process_suffix)
            print("发现需要处理文件:",len(files))
            return list(files)

    # 获取所有需要处理的任务，然后把任务加到任务池
    def get_all_tasks(self,taks_files):
        for file in taks_files:
            df = pd.read_csv(file,encoding='utf-8-sig')
            for _,row in df.iterrows():
                yield file, row,None # 最后一个是split_frame_idx

    async def request_data(self,session, url, data):
        async with session.post(url, json=data, headers=self.headers) as resp:
            # print(resp.status)
            rs = await resp.text()
            return resp.status, rs

    async def request_data_with_retry(self,session, url,data):
        tries = 3
        while tries > 0:
            try:
                return await self.request_data(session, url, data)
            except aiohttp.ClientResponseError:
                if tries <= 0:
                    raise Exception("请求错误超过3次")
            tries -= 1

    ### 执行单个异步任务，根据具体的业务覆盖这个方法
    async def process_func(self,file,task_row,split_frame_idx,semaphore):
        async with semaphore:
            # timeout=aiohttp.ClientTimeout(total=10*300)
            async with aiohttp.ClientSession() as session:
                payload = {
                    "file":file,
                    "data":{
                        "row_dict": task_row[self.cols].to_dict(),
                        "split_frame_idx": split_frame_idx,
                        "users_param":self.users_param
                    },
                    "mode":self.mode,
                    "save_dir":self.work_dir,
                    "use_cache":self.api_use_cache
                }
                statu,rs = await self.request_data_with_retry(session, url=self.parse_url, data=payload)

                ###打印进度
                self.format_progress()
                ##打印进度
                return file,task_row,statu,rs,split_frame_idx  # 文件名，原始行数据，以及API返回的结果

    # @deco_execution_time
    async def process_all_tasks(self,task_files):
        semaphore = asyncio.Semaphore(self.async_task_nums)
        task_list = []

        print("获取任务明细...")
        for file,task_row,split_frame_idx in self.get_all_tasks(task_files):
            task = asyncio.create_task(self.process_func(file,task_row,split_frame_idx,semaphore))
            task_list.append(task)
        print("总任务数量:",len(task_list))
        self.format_progress = gen_format_progress_seq(total=len(task_list),split_part=10)
        res = await asyncio.gather(*task_list)
        return res

    # @deco_execution_time
    def check_all_tasks_result(self):
        pass

    # @deco_execution_time
    def handler_tasks_result(self):
        pass

    @deco_execution_time
    def main_process(self):
        print("start ...")
        task_files = self.get_process_task_files(self.args.inputfile.name)
        # task_files = self.get_process_task_files("/Users/hwang2/Downloads/result_report_A4141-Li66571_2021-08-03T08_00_07.010205Z[UTC].csv")

        # 异步执行所有任务并拿到结果
        # print("ready to process taskfiles",task_files)
        res = asyncio.run(self.process_all_tasks(task_files))

        # 执行结果分析和处理 r如果有error 把错误写到csv文件中
        error_header = ["file", "record_id", "batch_num", 'http_code', "split_frame_idx", 'annotation', "errors"]
        error_lines = []

        for file, task_row, statu, rs, split_frame_idx in res:
            # print(file,task_row,statu,rs)
            record_id = task_row["Record ID"]
            batch_num = task_row["Batch Num"]
            # image_url = task_row.get("image_url")
            annotation = task_row.get("annotation")
            http_code = statu
            if statu != 200:
                errors = "网络或接口异常"
                error_lines.append([file, record_id, batch_num, http_code, split_frame_idx, annotation, errors])

            else:
                rs_dict = json.loads(rs)
                if rs_dict["code"] != 200:
                    errors = json.dumps(rs_dict["errors"], ensure_ascii=False)
                    error_lines.append([file, record_id, batch_num, http_code, split_frame_idx, annotation, errors])

        if len(error_lines) == 0:
            print("未发现异常")
        else:
            print(f"发现异常{len(error_lines)}，请检查输出文件中的异常明细", file=sys.stderr)
            saveCsvData(os.path.join(self.temp_dir, f"ERROR_{gen_uuid()}.csv"), error_lines, header=error_header)


    @deco_execution_time
    def main(self):
        self.main_process()

        if self.pack_zip ==True and self.save_way=='oss':
            print("压缩result文件夹到压缩包..",self.work_dir)
            oss_obj = OSS_API(bucket_name="appen-delivery")
            pack_name_list = oss_obj.list_bucket_files_deep(oss_path=self.work_dir.replace("/appen-delivery/",""),with_bucket_name=True)

            packzipfilev1(os.path.join(self.temp_dir,f"result_{gen_uuid()}.zip"),rm_path=self.temp_dir,pack_name_list=pack_name_list)
            print("压缩包生成完毕!")

        ## 生成oss授权码
        if self.save_way =="oss":
            oss_authorize = OSS_STS_AUTH_Authorize("oss:/"+self.temp_dir)
            oss_authorize.get_auth_str()
