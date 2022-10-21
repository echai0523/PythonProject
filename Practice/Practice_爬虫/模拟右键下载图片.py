# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/10/21 17:13
input   : 
output  :   
Short Description: 
Change History:
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui, pandas
from time import sleep


df = pandas.read_csv("../../EthanFileData/csv/image1019.csv")
driver = webdriver.Chrome('chromedriver.exe')

for _, row in df[:3].iterrows():
    url = row["image_url"]
    # url = 'https://image.lexica.art/md/de1b607f-0b24-4a8c-a55b-7f3b69d6a87b'
    driver.get(url)
    pic = driver.find_element(By.XPATH, '//html/body/img')  # 获取元素
    action = ActionChains(driver).move_to_element(pic)  # 移动到该元素
    action.context_click(pic)  # 右键点击该元素
    action.perform()  # 执行
    pyautogui.typewrite(['v', "down", "enter"])  # 敲击V 下移down 确认enter
    # 单击图片另存之后等1s敲回车
    sleep(3)
    pyautogui.typewrite(["enter"])
