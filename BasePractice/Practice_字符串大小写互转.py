# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/20 15:59

input: 
output: 
Short Description: 

Change History:

"""
in_put = input("Please enter your text：")
A_Z = [chr(A) for A in range(65, 91)]
a_z = [chr(a) for a in range(97, 123)]
out_put = str()
for i in in_put:
    if i in A_Z:
        out_put += chr(ord(i)+32)
    elif i in a_z:
        out_put += chr(ord(i) - 32)
print("New text: ", out_put)
