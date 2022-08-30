# -*- coding: UTF-8 -*-

'''
Author: Henry Wang
Date: 2021-05-13 11:56
Short Description:

Change History:

'''
import platform

OSS_AK = 'LTAI4GGpV2FB3UcvEJBjhAu7'
OSS_SK = 'zbRKd60LpBQTWOu5fD59tpy1B7sziE'
OSS_REGION = "http://oss-cn-shanghai.aliyuncs.com"



if platform.system() =='Linux':
    RDS_DATA_DB_HOST ="pgm-uf67awed7a872oi4168220.pg.rds.aliyuncs.com" # 内网
    PROCESS_API_HOST = 'http://192.168.0.181'  # process api 内网IP
    AMR_API_HOST = 'http://192.168.0.75'  # 走内网gateway

else:
    RDS_DATA_DB_HOST = "pgm-uf67awed7a872oi4mo.pg.rds.aliyuncs.com"  # 外网地址
    PROCESS_API_HOST = 'http://101.133.150.181:9090' # process api公网IP 注意80端口只对vpc和公司IP开放
    AMR_API_HOST = 'http://47.103.159.230' #走公网gateway  注意80端口只对vpc和公司IP开放

PROCESS_API_SLB_HOST ="https://process-api.appen.com.cn"


RDS_DATA_DB_NAME = 'data_db'
RDS_DATA_DB_PORT = '5432'
RDS_DATA_DB_USER = 'postgres'
RDS_DATA_DB_PSW = 'F2V7IwitDtXampru'


OLD_DB_HOST = "47.101.195.227"
OLD_DB_PORT = '5432'
OLD_DB_USER = 'postgres'
OLD_DB_PSW = 'appen_pe123'
OLD_DB_NAME = 'portal_db'


REDIS_HOST = "r-uf64lhk3mvdj47kepj.redis.rds.aliyuncs.com" # 内网地址 data_cache
REDIS_PORT = "6379"


MQ_HSOT = "192.168.0.173"  # 内网地址
MQ_PORT = 5672
MQ_USER = 'guest'
MQ_PWD = 'guestpe123'