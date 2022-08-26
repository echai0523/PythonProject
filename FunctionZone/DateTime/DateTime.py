# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/24 16:40

input: 
output: 
Short Description: 

Change History:

"""
from datetime import datetime
import time


def main():
    print(datetime.fromtimestamp(1660803331))  # 2022-08-18 14:15:31  秒数转为时间类型
    print(datetime.now())  # 2022-06-28 21:19:40.276387
    print(datetime.now().date())  # 2022-06-28
    print(datetime.now().date().strftime("%Y"))  # 2022
    print(datetime.now().second)  # 21
    print(datetime.now().minute)  # 25
    print(datetime.now().hour)  # 21
    print(datetime.now().day)  # 28
    print(datetime.now().month)  # 6
    print(datetime.now().year)  # 2022
    print(datetime.now().strftime('%Y/%m/%d'))  # 2022/08/24
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))  # 2022-08-24 16:42:55


if __name__ == '__main__':
    main()
