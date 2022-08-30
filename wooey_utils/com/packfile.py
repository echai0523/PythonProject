# -*- coding: UTF-8 -*-

'''
Author: Henry Wang
Date: 2021-10-09 16:05
Short Description:

Change History:

'''

import zipfile
import os

def packzipfilev1(outpath,rm_path,pack_name_list):
    # import zipfile
    # import os
    if rm_path.endswith("/")==False:
        rm_path = rm_path+"/"
    with zipfile.ZipFile(outpath, 'w',zipfile.ZIP_DEFLATED) as myzip:
        for fname in pack_name_list:
            # myzip.write(fname,os.path.basename(fname) )
            myzip.write(fname,arcname=fname.replace(rm_path,""))


# packzipfilev1("/Users/hwang2/Desktop/myres3.zip","/Users/hwang2/Desktop/",["/Users/hwang2/Desktop/result/haomo_2d_new/20210902_4597/images/1627614168018666/1627614168018666.json",
#                                             "/Users/hwang2/Desktop/result/haomo_2d_new/20210902_4597/images/1627614156019388/1627614156019388.json"])