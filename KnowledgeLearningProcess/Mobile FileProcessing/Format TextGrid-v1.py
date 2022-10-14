# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/10/14 13:50
input   : 
output  :   
Short Description:
    - 基本架构
        tg = textgrid.TextGrid(minTime=minTime, maxTime=maxTime)
        print('初始TextGrid文件信息：', tg.__dict__)

            # 开始时间，结束时间，文本
            tier_IntervalTier = textgrid.IntervalTier(name=name, minTime=minTime, maxTime=maxTime)
            tier_IntervalTier.add(start, end, text1)

            # 开始时间，文本
            tier_PointTier = textgrid.PointTier(name=name, minTime=minTime, maxTime=maxTime)
            tier_PointTier.add(start, text1)

        tg.tiers.append(tier_IntervalTier)
        tg.tiers.append(tier_PointTier)
        print('处理后TextGrid文件信息：', tg.__dict__)

        tg.write(path)

Change History:
"""
from peutils.transform.v1.base import get_session
from peutils.wooeyutil import WooeyBaseZipHandlerFile
import sys, os
import pandas as pd
from textgrid import textgrid

session = get_session()


def annotation_parse(annotation_json, statistics_json):
    # instances shapes categories
    instances = annotation_json["instances"]
    shapes = statistics_json["shapes"]
    categories = statistics_json["categories"]

    # 读取音频文件给定最大时长
    minTime = min([instance.get('start', 0) for instance in instances])  # 1.start字段最小值，一般为0
    maxTime = max([instance.get('end', 0) for instance in instances])    # 2.end字段最大值，代表整个音频的时长
    tg = textgrid.TextGrid(name="ooTextFile", minTime=minTime, maxTime=maxTime)
    # print('初始TextGrid文件信息：', tg.__dict__)

    # 通过statistics直接获取shapes, categories
    for shape, category in zip(shapes, categories):
        if shape == "segment":
            # shape type == segment 添加一层item[class=IntervalTier],name命名为category
            interval_tier = textgrid.IntervalTier(name=category, minTime=minTime, maxTime=maxTime)
            for instance in instances:
                if instance["shapeType"] == "segment":
                    interval_tier.add(instance.get("start"), instance.get("end"), instance.get("text"))
            tg.tiers.append(interval_tier)

        elif shape == "timing":
            # shape type == timing 添加一层item[class=PointTier],name命名为category
            point_tier = textgrid.PointTier(name=category, minTime=minTime, maxTime=maxTime)
            for instance in instances:
                if instance["shapeType"] == "timing":
                    point_tier.add(instance["start"], instance["text"])
            tg.tiers.append(point_tier)

    # print('处理后TextGrid文件信息：', tg.__dict__)

    return tg


def main(csv_path):
    df = pd.read_csv(csv_path)
    for _, row in df[:1].iterrows():
        # 解析标注数据
        annotation = session.get(row["annotation"]).json()
        statistics = session.get(annotation["statistics"]).json()
        tg = annotation_parse(annotation, statistics)
        # 写入TextGrid
        filename = os.path.basename(row['audio_url']).replace('.wav', '.TextGrid')  # 7.读取audio_url, 后缀大小写TextGrid
        tg.write(filename)


main("../../EthanFileData/csv/result_report_A5992-Li140535_2022-10-11T07_21_31.584310Z[UTC].csv")
if __name__ == '__main__':
    h = WooeyBaseZipHandlerFile(
        project_desc="A9数据转为TextGrid",
        need_process_suffix=".csv",
        process_func=main
    )
    sys.exit(h.main())
