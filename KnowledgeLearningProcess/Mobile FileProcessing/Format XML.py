# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/12/8 11:24
input   : 
output  :   
Short Description:
    xmltodict.parse()把xml转为dict
    xmltodict.unparse()把dict转为xml
Change History:
"""
import xmltodict


def json_to_xml(json_str_parameter):
    """
    xmltodict.unparse()把dict转为xml
    @param json_str_parameter: python的字典对象
    @return: xml字符串
    """
    xml_data = xmltodict.unparse(json_str_parameter, pretty=1, encoding='utf-8')
    return xml_data


def xml_to_json(xml_str_parameter):
    """
    xmltodict.parse()把xml转为dict
    @param xml_str_parameter: xml
    @return: xml字符串
    """
    json_data = xmltodict.parse(xml_str_parameter, encoding='utf-8')
    return json_data


data = {
    "annotation": {
        "folder": "folder",  # 文件夹名
        "filename": "filename",  # 文件名
        "path": "frameUrl",  # 文件夹名+文件名, 事例为本地绝对路径
        "source": {
            "database": "UnKnown"  # 固定值: "UnKnown"
        },
        "size": {
            "width": 1024,  # 图宽
            "height": 1024,  # 图高
            "depth": 3,  # 图颜色深度
        },
        "segmented": 0,  # 固定值: 0
        "object": [
            {
                "name": "label",  # label type
                "pose": "Unspecified",  # 固定值
                "truncated": 0,  # 固定值
                "difficult": 0,  # 固定值
                "bndbox": {
                    "xmin": 50,
                    "ymin": 50,
                    "xmax": 100,
                    "ymax": 100
                }
            } for i in range(2)
        ]
    }
}
with open("to.xml", mode='w', encoding="utf-8") as fw:
    fw.write(json_to_xml(data))

with open("to.xml", mode='r', encoding="utf-8") as fr:
    result = xml_to_json(fr.read())
    print(result, type(result))

