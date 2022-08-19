# -*- coding: UTF-8 -*-

# f0cf9a2c-4261-4297-bd91-78640b6cd613
import argparse
import json
import requests


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--body')
    return parser.parse_args()


def validate(result_json):
    validation_results = []

    for result in result_json['results']:
        main_id_count = []

        if len(result["items"]) != len(result["images"][0]["items"]):
            validation_results.append({
                "frameId": result["frameId"],
                "message": f"第{result['frameId'] + 1}帧：23D数据不对应，缺少数据",
                'blockSubmit': True
            })
        for item, img_item in zip(result["items"], result["images"][0]["items"]):
            # 2d属性
            labels = json.loads(img_item["labels"])

            if img_item["category"] != labels["ef-ontology"]:
                validation_results.append({
                    "frameId": result["frameId"],
                    "number": img_item["number"],
                    'category': img_item["category"],
                    'ef-ontology': labels["ef-ontology"],
                    "message": f"第{result['frameId']+1}帧-{img_item['category']}-{img_item['number']}：属性不同",
                    'blockSubmit': True
                })

            # 判断2d属性id是否重复
            main_id = labels["main_id"]
            sub_line_id = labels.get("sub_line_id", 0)
            if f"{main_id}-{sub_line_id}" in main_id_count:
                validation_results.append({
                    "frameId": result["frameId"],
                    "number": img_item["number"],
                    "message": f"第{result['frameId'] + 1}帧-{img_item['category']}-{img_item['number']}：车道线ID编号重复",
                    'blockSubmit': True
                })
            else:
                main_id_count.append(f"{main_id}-{sub_line_id}")
        # print(result["frameId"], main_id_count)
    return validation_results


def run():
    args = parse_args()
    annotation = json.loads(args.body)
    # import pandas as pd
    # df = pd.read_csv(r"C:\Users\echai\Downloads\process\1420 A9检查脚本\Result_2022-08-15T08_45_16.898381Z.csv")
    # annotation = df["annotation"][0]
    # annotation = "https://oss-prd.appen.com.cn:9001/tool-prod/d43faceb0f5c8d8e8c7cbaed97b3fff9/R.1660532037352.lidar.seg.dc4d9f0b-522c-47f9-b554-4225fde950ab.CNXa4gIQAg3d3d_2022-08-15T023945Z.15153.QA_RW.9647485d-402a-4380-b9a9-7d0b74ca73f2.df7bc80f421f46023187c55efd83ee1a.review.json"
    r = requests.get(annotation, timeout=8)
    if r.status_code == 200:
        json_result = r.json()
        data = validate(json_result)
        print(json.dumps(data, ensure_ascii=False))


run()
