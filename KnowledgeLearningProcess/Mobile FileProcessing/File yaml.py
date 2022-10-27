# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/10/25 21:24
input   : 
output  :   
Short Description: 
Change History:
"""
import yaml


def save_dict_to_yaml(dict_value: dict, save_path: str):
    """dict保存为yaml"""
    with open(save_path, 'w') as file:
        file.write(yaml.dump(dict_value, allow_unicode=True))


def read_yaml_to_dict(yaml_path: str, ):
    with open(yaml_path) as file:
        dict_value = yaml.load(file.read(), Loader=yaml.FullLoader)
        return dict_value


if __name__ == '__main__':
    my_config_dict = {
        "mysql": {
            "host": "127.0.0.1",
            "tables": ["table_1", "table_2"],
        },
        "redis": {
            "host": "127.0.0.1",
            "db": 3,
        }
    }
    # 保存yaml
    save_dict_to_yaml(my_config_dict, "config.yaml")
    # 读取yaml
    config_value = read_yaml_to_dict("config.yaml")
    assert config_value == my_config_dict

