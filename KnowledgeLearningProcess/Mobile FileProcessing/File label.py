# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/11/14 11:34
input   : 
output  :   
Short Description: 
Change History:
"""
import numpy as np
import os

# 读取label
arr = np.fromfile("../../EthanFileData/Binary/000000.label", dtype="uint32")

arr.tofile("000000.label")

