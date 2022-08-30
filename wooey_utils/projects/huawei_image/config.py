# -*- coding: UTF-8 -*-

'''
Author: Simon Wang
Date: 20210929
Short Description:

Change History:

'''
from wooey_utils.com.db_tool import Dbclass


def ping_by_api():
    import requests
    try:
        r = requests.get('http://10.254.0.82/api/meta/info', timeout=5)
        return 0
    except Exception as e:
        return 404


def local_ip_if_linux():
    import platform
    if platform.system() == 'Linux':
        return '127.0.0.1'
    else:
        # 通过pin判断是否是走VPN
        num = ping_by_api()

        if num == 0:
            return '10.254.0.82'
        else:
            return '47.101.195.227'


def get_protal_db():
    db_setting = {"host": local_ip_if_linux(), "port": 5432, "user": "postgres", "pwd": "appen_pe123"}
    db = Dbclass(db_setting, dbname="portal_db")
    return db
