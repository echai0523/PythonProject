# -*- coding: utf-8 -*-


"""
Author  :Jon
Date    :20210624
Manage  :
Project :
CID     :
PID     :
Detail  :

 

Change History:
"""

import requests


class ERROR_MSG_LOG():
    def __init__(self):
        self.error_list = []

    def create_error(self, error_msg):
        self.error_list.append(f"ERROR:{error_msg}")


class SINGEL_ROW_PROCESS():
    def __init__(self, json_url, row_dict):
        self.json_row_data = requests.get(json_url).json()

        self.log = ERROR_MSG_LOG()  # 这行数据的所有错误

    def get_group_maps(self):
        group_dict = dict()
        for item in self.json_row_data['json'][0]["groups"]:
            group_dict[item["id"]] = item
        return group_dict

    def check_row_func(self):
        json_data = self.json_row_data
        print(json_data)
        results_list = json_data['results'][0]
        for idx, res in enumerate(results_list):
            # 检查角色是否为空
            role = res['attributes']
            if role and role.get('speaker', None):
                """数据正确"""
            else:
                """数据错误"""
                self.log.create_error(f"{idx + 1} 角色为空！")
            content_text: str = res['content'][0]['text']
            if content_text:
                if content_text.endswith('。') or content_text.endswith('？') or content_text.endswith('！'):
                    pass
                else:
                    self.log.create_error(f"{idx + 1} 结尾不为。？！")

            else:
                self.log.create_error(f"{idx + 1} 文本为空！")

        return self.log.error_list


if __name__ == '__main__':
    h = SINGEL_ROW_PROCESS(
        "https://oss-prd.appen.com.cn:9001/tool-prod/c3a89dee-cb79-454c-89ce-087a85b5a7a6/c3a89dee-cb79-454c-89ce-087a85b5a7a6.CIGGUBAC_2021-06-17T063346Z.1.result.json")
    error_rs = h.check_row_func()
    print(error_rs)
    # # json_rs = h.parse_row_func()
    # print(json.dumps(json_rs,ensure_ascii=False))
