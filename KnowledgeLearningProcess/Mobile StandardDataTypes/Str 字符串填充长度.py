# -*- coding: utf-8 -*-
"""
Author: Ethan Chai
Date: 2022/9/28 09:44
input: 
output: 
Short Description:
    - 原字符串左侧对齐， 右侧补零: str.ljust(width,'0')
    - 原字符串右侧对齐， 左侧补零:
        - str.rjust(width,'0')
        - str.zfill(width)
        - '%07d' % n
Change History:
"""

print('789'.ljust(32, '0'))  # '78900000000000000000000000000000'

print('798'.rjust(32, '0'))  # '00000000000000000000000000000798'

print('123'.zfill(32))  # '00000000000000000000000000000123'

print('%032d' % 89)  # '00000000000000000000000000000089'


