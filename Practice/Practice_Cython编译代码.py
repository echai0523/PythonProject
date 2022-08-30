# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/26 10:18

input: 

output: 

Short Description: 
    - 先将脚本编译为.c，然后再编译为.pyd
        - by\test.py待编译的脚本
            -
                def test(a):
                print("Hello World!", a)
        - by\setup.py编译脚本
            -
                from distutils.core import setup
                from Cython.Build import cythonize
                from Cython.Distutils import build_ext

                setup(ext_modules=cythonize("a.py"))
        - by路径下进入终端输入命令
            - python setup.py build_ext
                生成的by\build\lib.win-amd64-cpython-37\a.cp37-win_amd64.pyd为编译后的pyd文件，可以直接调用使用
Change History:
    
"""

