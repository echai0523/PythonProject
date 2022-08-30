# -*- coding: UTF-8 -*-

'''
Author: Simon Wang
Date: 20210804
Short Description:

Change History:

'''


# from wooey_utils.common.config import get_protal_db

#
# def get_image_json_info_from_db(img_url):
#     db = get_protal_db()
#     rs = db.db_query(f'''select json_info from t_haomo_2d_json_info where imgurl='{img_url}';''')
#     assert len(rs) == 1, "根据imgUrl未找到json数据或者找到多条数据"
#     db.close()
#     return rs[0][0]
def ping_by_api():
    import requests
    try:
        r = requests.get('http://10.254.0.82/api/meta/info', timeout=5)
        return 0
    except Exception as e:
        return 404


def local_ip_if_linux():
    import platform
    if platform.system() == 'Linux':
        return '127.0.0.1'
    else:
        # 通过pin判断是否是走VPN
        num = ping_by_api()

        if num == 0:
            return '10.254.0.82'
        else:
            return '47.101.195.227'


def remove_key_if_exists(info_dict: dict, rm_list: list):
    for rm_name in rm_list:
        if rm_name in info_dict:
            del info_dict[rm_name]

    return info_dict
