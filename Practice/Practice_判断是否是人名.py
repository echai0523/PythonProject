# -*- coding: UTF-8 -*-

import re
import json
from uuid import uuid4
from collections import defaultdict
import jieba.posseg as pseg


def isname(single_word_string):
    """
    判断是否是人名
    :param single_word_string: 待判断的str
    :return: bool值
    """
    pair_word_list = pseg.lcut(single_word_string)
    for eve_word, cixing in pair_word_list:
        if cixing == "nr":
            return True
    return False


def parse_result(result):
    """
    解析数据 -> json
    :param result: 待处理的数据
    :return: json
    """
    title_list = ['总经理', '副总裁', '第一副总裁', '副总裁助理', '首席执行官', '首席运营官', '首席财务官', '首席信息官', '首席技术官', '人力资源总监', '运营总监', '市场总监',
                  '运作经理', '生产经理', '产品经理', '业务部经理', '艺术总监', '商务总监', '内容总监', '开发总监', '政府关系', '人事总监', '知识总监', '工会主席', '市场总监', '首席谈判代表', '公关总监',
                  '质控总监', '研究总监', '销售总监', '客户总监', '销售负责人']
    default = defaultdict(list)
    Data = {}

    data = result['result'][0]['data']
    for d in data:
        text = d['text']
        fax = re.match(r'([\d]{4}-[\d]{8})', text)
        call = re.match(r'C([\d]{4}-[\d]{8})', text)
        tel1 = re.findall(r'.*([\d]{11})', text)
        tel2 = re.findall(r'.*([\d]{2}\+[\d]{11})', text)
        tel3 = re.findall(r'86([\d]{11})', text)
        if fax:
            default['Fax'].append(fax.group(1))
        elif call:
            default['OfficePhoneNumbers'].append(call.group(1))
        elif tel1:
            default['CellPhoneNumbers'].append(tel1[0])
        elif tel2:
            default['CellPhoneNumbers'].append(tel2[0])
        elif tel3:
            default['CellPhoneNumbers'].append(tel3[0])
        elif '@' in text:
            default['Emails'].append(text)

        elif '市' in text:
            default['Addresses'].append(text)
        elif '公司' in text:
            default['Companies'].append(text)
        elif isname(text):
            default['Name'] = text
        if text:
            for title in title_list:
                if title in text:
                    default['Titles'] = title
                continue

    for k, v in default.items():
        Data[k] = v
    after_data = json.dumps({
        "RequestId": str(uuid4()),
        "Data": Data
    }, ensure_ascii=False)

    # 最终结果
    return after_data


if __name__ == '__main__':
    # result = {'result': [{'save_path': '', 'data': [{'text': '深圳市南山区海天一路赛西科技大厦1707室', 'confidence': 0.9513640403747559, 'text_box_position': [[303.0, 221.0], [357.0, 222.0], [352.0, 970.0], [297.0, 970.0]]}, {'text': 'www.htcctech.com', 'confidence': 0.9851363897323608, 'text_box_position': [[374.0, 225.0], [425.0, 226.0], [413.0, 658.0], [362.0, 657.0]]}, {'text': 'libo@htcctech.com', 'confidence': 0.9048331379890442, 'text_box_position': [[443.0, 226.0], [497.0, 228.0], [483.0, 662.0], [429.0, 660.0]]}, {'text': '口+8618038183498', 'confidence': 0.8758825659751892, 'text_box_position': [[513.0, 234.0], [562.0, 235.0], [554.0, 644.0], [505.0, 643.0]]}, {'text': '深圳红途科技有限公司', 'confidence': 0.8968387842178345, 'text_box_position': [[584.0, 232.0], [635.0, 233.0], [629.0, 727.0], [578.0, 727.0]]}, {'text': '红途科技', 'confidence': 0.9969583749771118, 'text_box_position': [[795.0, 375.0], [860.0, 377.0], [851.0, 611.0], [786.0, 608.0]]}, {'text': '销售负责人', 'confidence': 0.977143406867981, 'text_box_position': [[749.0, 1112.0], [794.0, 1112.0], [794.0, 1303.0], [749.0, 1303.0]]}, {'text': '李波', 'confidence': 0.9986451864242554, 'text_box_position': [[807.0, 1128.0], [888.0, 1128.0], [888.0, 1308.0], [807.0, 1308.0]]}]}]}
    # print(parse_result(result))
    pass




