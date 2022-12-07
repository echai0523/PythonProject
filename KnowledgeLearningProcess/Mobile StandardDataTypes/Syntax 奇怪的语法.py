# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/12/5 14:54
input   : 
output  :   
Short Description: 
Change History:
"""
import os


data = "奇怪的语法"
(lambda f, d: (f.write(d), f.close()))(open(os.path.basename("Syntax.txt"), 'w'), data)

