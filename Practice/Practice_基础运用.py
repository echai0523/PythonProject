# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/11 10:53

input: 
output: 
Short Description: 

Change History:

"""
# 1

str_list = list()
while True:
    input_str = input("Please enter an item for your shopping list or end to print the list: ")
    if input_str == 'end':
        break
    str_list.append(input_str)

print("Shopping List:\n")
print("==============")
for i, s in enumerate(str_list):
    print(str(i+1), ")", s)

# Snickers
# Pizza
# Pepsi Max
# Ice-cream
# end

# 2
import time
import traceback

names = ["John", "Jane", "Peter", "Paul", "Michael", "Mary", "Robert", "Roland"]
print("Current list of name: ", names)

a_or_d = input("Enter A to add a name or D to delete a name: ")
if a_or_d == "A":
    tag = True
    while tag:
        # 添加
        new_name = input("Enter a new name: ")
        try:
            before_name = input("Enter the name you want to insert the new name before: ")
            names.insert(names.index(before_name), new_name)
            print("Updated list of names: ", names)
            tag = False
        except Exception:
            traceback.print_exc()
            time.sleep(0.5)
            continue
elif a_or_d == "D":
    # 删除
    tag = True
    while tag:
        try:
            delete_name = input("Enter a name to delete: ")
            names.remove(delete_name)
            print("Updated list of names: ", names)
            tag = False
        except Exception:
            traceback.print_exc()
            time.sleep(0.5)
            continue


# 3

SET = list()
sentence = input("Please enter a sentence: ")
for i in sentence.split():
    if i not in SET:
        SET.append(i)
result = ", ".join(SET[::-1])
print("Unique words: ", result)

# programming is fun
# i find that the harder i work the more luck i seem to have


