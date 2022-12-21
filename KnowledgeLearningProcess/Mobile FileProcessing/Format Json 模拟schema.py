# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/10/20 09:35
input   : 
output  :   
Short Description:
    1.固定的数组数量
        3*3数组例子: Tuple[Tuple[float,float,float],Tuple[float,float,float],Tuple[float,float,float]]
    2. 枚举
        class SensorEnum(str, Enum):
            pear = 'pear'
            banana = 'banana'
            CAMERA_FRONT_MAIN = "CAMERA_FRONT_MAIN"


        class xxx(baseModel):
            sensor: SensorEnum

    3. 多中类型的支持，比如允许None和int
        class Base_Labels_Frames_Timestamp(BaseModel):
            timestamp: Union[int, None]

    4. 针对字段的值增加自定义的 validator
        class Base_Labels_Frames_Timestamp(BaseModel):
            timestamp: Union[int, None]
            sensor: SensorEnum

            @validator('timestamp')
            def timestamp_must_rule(cls,v):
                if v <100:
                    raise ValueError("must larger than 100")

    5. 针对列表下的每一个字段去做检查
        # 如果不写each_item 那么v 就是整个list,如果写了 就是list中某个值，可以少写一层循环
        class Base(BaseModel):

            mylist: List[Base_Mylist]
            @validator('mylist', each_item=True)
            def check_squares(cls, v):
                assert v.x > 8 and v.y> 8,f"{v} is not valid"
                return v

    6. 如果没有特定的格式，可以用Any
        比如
            timestamp: Any
            my_lit: List[Any]
            my_dict : Dict[Any]


    安装:
        pydantic==1.9.1

    使用注意点:
        1. 根结点不支持数组，如果是数组，可以自己改下JsonSchema
        2. 如果是列表中的字典key不一样，是按最多的来生成的，需要自己手动去改一下哪些是可选参数，比如 str 改成 Optional[str]
        3. 数组或嵌套数组是取最里层的第一个元素来判断类型的，如果不一样的情况需要定制
        4. 如果str类型是固定的取值范围，可以自己加枚举

Change History:
"""
from pydantic import BaseModel, Field, ValidationError, validator
from typing import List, Set, Optional, Dict, Tuple, Any, Union
from enum import Enum, unique
import json
from collections import defaultdict
import sys


class SchemaParseV1(object):

    def __init__(self, data):
        self.data = data
        if isinstance(data, dict) is False:
            raise Exception("最外层必须是字典结构")
        self.cls_dict = defaultdict(dict)

    @staticmethod
    def str_type(tp):
        if tp is None:
            return "Any"
        if type(tp) == int:
            return "int"
        if type(tp) == float:
            return "float"
        elif type(tp) == str:
            return "str"
        elif type(tp) == dict:
            return "dict"
        elif type(tp) ==bool:
            return "bool"
        else:
            raise Exception("未知类型", tp)

    @staticmethod
    def combine_name(concat_name, filed_name):
        if concat_name == "":
            return filed_name.capitalize()
        else:
            return concat_name + "_" + filed_name.capitalize()

    @staticmethod
    def list_parser(lst: list):
        """
        1. 返回list层级
        2. 返回第一个元素，如果有嵌套返回最里层的第一个元素
        """
        assert isinstance(lst, list) is True, "必须传入数组"
        # 深度
        deep = 0
        l = lst
        first = None
        while isinstance(l, list) is True:
            deep += 1
            first = l[0]
            l = first
        return deep, first

    def parse_data_unit(self, un, field_name, concat_name):
        if isinstance(un,bool):
            return "bool"
        elif isinstance(un, float):
            return "float"
        elif isinstance(un, int):
            return "int"
        elif isinstance(un, str):
            return "str"
        elif isinstance(un, list):
            cls_name = self.combine_name(concat_name, field_name)

            if len(un) == 0:
                return "List[Any]"
            else:
                # 遍历一遍，对于内部嵌套数组的这种，可以把key补充完整
                for iun in un:
                    _ = self.parse_data_unit(iun, field_name=field_name, concat_name=concat_name)

                # 取第一个，嵌套就是里层第一个元素去返回类型
                deep, first = self.list_parser(un)
                dtype = self.parse_data_unit(first, field_name=field_name, concat_name=concat_name)
                return "List[" * deep + dtype + "]" * deep

        elif isinstance(un, dict):
            cls_name = self.combine_name(concat_name, field_name)
            for k, vun in un.items():
                field_name = k
                dtype = self.parse_data_unit(vun, field_name=field_name, concat_name=cls_name)
                self.cls_dict[cls_name][field_name] = dtype
            # 这里是整个dict的类型的最终返回值
            return cls_name

        elif un is None:
            return "Any"
        else:
            raise Exception("异常的解析结构类型")

    def parse_dict_func(self):
        cls_name = "Base"
        for k, v in self.data.items():
            # 递归的时候返回，当前这个对象的类型
            field_name = k
            # 递归数据
            dtype = self.parse_data_unit(v, field_name=field_name, concat_name="Base")
            self.cls_dict[cls_name][field_name] = dtype

        # 打印类的数据
        print("""from pydantic import BaseModel, Field, ValidationError
from typing import * 
from enum import Enum, unique
import json
from collections import defaultdict
        """)
        # 短的名称放在最后
        cls_list = sorted(list(self.cls_dict.keys()), key=lambda name: len(name), reverse=True)
        for name in cls_list:
            cls_name = name
            cls_d = self.cls_dict[name]
            cls_text = f"class {cls_name}(BaseModel):\n"
            for k, v in cls_d.items():
                cls_text += f"    {k}: {v}\n"
            print(cls_text)


if __name__ == "__main__":
    # json_path = "../../EthanFileData/Json/jg.json"
    json_path = "../../EthanFileData/Json/cr_f60.json"
    # json_path = "../../EthanFileData/Json/cr_f120.json"
    with open(json_path, 'r') as fr:
        data = json.load(fr)
        sc = SchemaParseV1(data=data)
        sc.parse_dict_func()
