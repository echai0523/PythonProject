# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/24 16:40

input: 
output: 
Short Description:
    - 知识点：
        - time.time()   时间戳
        - datetime.fromtimestamp() 秒数转为时间类型
        - strptime()   str转datatime
        - strftime()   格式化%Y %m %d %H %M %S
Change History:

"""
from datetime import datetime
import time


def main():
    print(time.time())  # 时间戳
    print(datetime.fromtimestamp(time.time()))  # 时间戳转为时间类型
    print(datetime.fromtimestamp(1660803331))  # 2022-08-18 14:15:31  秒数转为时间类型
    print(datetime.fromtimestamp(1642660786).strftime('%Y-%m-%d %H:%M:%S'))
    print(datetime.strptime("2022-10-12 14:40:15", '%Y-%m-%d %H:%M:%S').strftime("%Y"))  # str转datatime
    print(datetime.now())  # 2022-06-28 21:19:40.276387
    print(datetime.now().date())  # 2022-06-28
    print(datetime.now().date().strftime("%Y"))  # 2022
    print(datetime.now().second)  # 21
    print(datetime.now().minute)  # 25
    print(datetime.now().hour)  # 21
    print(datetime.now().day)  # 28
    print(datetime.now().month)  # 6
    print(datetime.now().year)  # 2022
    print(datetime.now().strftime('%Y%m%d_%H%M%S'))  # 格式化
    print(datetime.now().strftime('%Y/%m/%d'))  # 2022/08/24
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))  # 2022-08-24 16:42:55

    print(time.strftime("%H:%M:%S", time.gmtime(5555)))  # 秒数转换为时分秒
    seconds = 5555
    m, s = divmod(seconds, 60)  # divmod 返回商和余数
    h, m = divmod(m, 60)
    print("%02d:%02d:%02d" % (h, m, s))  # 秒数转换为时分秒


if __name__ == '__main__':
    # main()
    print(datetime.fromtimestamp(1642660786).strftime('%Y-%m-%d %H:%M:%S'))