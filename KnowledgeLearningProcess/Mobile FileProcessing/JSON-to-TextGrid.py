#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/24 17:14

input:
output:

Short Description:
    - 如何优雅的使用Python读取TextGrid文件：https://blog.csdn.net/shaopengfei/article/details/108631858
    - 生成textgrid文件：https://www.cnblogs.com/yunhgu/p/15179565.html
    - textgrid 库调研小结：https://blog.csdn.net/duxin_csdn/article/details/88966295
        - 添加分割线：貌似类似add方法，具体与实操为主，mark为text(好像只是最后一个intervals的text，其他text设为空)
            - interval1 = textgrid.Interval(minTime=0, maxTime=2, mark="s")
            - interval2 = textgrid.Interval(minTime=1, maxTime=2, mark="asdfas")
            - interval3 = textgrid.Interval(minTime=1, maxTime=2, mark="asdfas")
            - tier_1.addInterval(interval1)
            - tier_2.addInterval(interval2)
            - tier_3.addInterval(interval3)
Change History:

"""

import textgrid
import requests
import pandas as pd


def dispose_json(data):
    # 排除不存在的数据
    exclude = lambda x: x if x else ""

    # json提取中results
    results = data['results'][0]

    # 读取音频文件给定最大时长
    minTime = results[0]['start']  # 第一段的开始
    maxTime = results[-1]['end']  # 最后一段的结束
    tg = textgrid.TextGrid(minTime=minTime, maxTime=maxTime)
    print('初始TextGrid文件信息：', tg.__dict__)

    # 添加一层item[1],name命名为 层
    tier_1 = textgrid.IntervalTier(name="category", minTime=minTime, maxTime=maxTime)
    # 添加一层item[2],name命名为 层
    tier_2 = textgrid.IntervalTier(name="transcript", minTime=minTime, maxTime=maxTime)
    # 添加一层item[3],name命名为 层
    tier_3 = textgrid.IntervalTier(name="attribute", minTime=minTime, maxTime=maxTime)

    for result in results:
        # 每层每个片段start时间
        start = result['start']
        # 每层每个片段end时间
        end = result['end']
        # 提取text
        content = result['content'][0]
        attributes = content['attributes']
        # item[1].text
        text1 = content['attributes']['Category']
        # item[2].text
        text2 = content['text']
        # item[3].text
        language = exclude(attributes.get('Language'))
        gender = exclude(attributes.get('Gender'))
        role = exclude(content.get('role'))
        age = exclude(attributes.get('Age'))
        emotion = exclude(attributes.get('Emotion'))
        unclear_or_not = exclude(attributes.get('Unclear_or_not'))
        tts = exclude(attributes.get('TTS'))
        text3 = ""
        if text1 != 'NOISE' or 'ACCOMPANY' or 'EOVRLAP':
            text_list = [language, gender, role, age, emotion, unclear_or_not, tts]
            text3 = ' '.join(text_list)

        # add添加每个intervals的起止时间start、end内容text
        tier_1.add(start, end, text1)
        tier_2.add(start, end, text2)
        tier_3.add(start, end, text3)

    # 添加到tg对象中
    tg.tiers.append(tier_1)
    tg.tiers.append(tier_2)
    tg.tiers.append(tier_3)

    print('处理后TextGrid文件信息：', tg.__dict__)
    return tg


def main():
    # 读取csv文件 获取annotation、audio_url
    file_path = r'B-英文ASR试标导出.csv'  # 文件路径
    df = pd.read_csv(file_path)
    json_files = df.annotation
    audio_urls = df.audio_url
    for file, url in zip(json_files, audio_urls):
        json_data = requests.get(file).json()
        tg = dispose_json(json_data)
        # 写入保存TextGrid文件
        filename = url.split('/')[-1].split('.')[0]
        tg.write(f"{filename}.TextGrid")
        print(f'{filename}.TextGrid文件已生成！')


if __name__ == '__main__':
    main()
