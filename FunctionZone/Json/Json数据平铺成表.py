# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/19 17:51

input:
    - .json
output:
    - .xlsx or .csv
Short Description: 
    - 知识点：
        - pd.json_normalize() json数据展平
            - 参数
                - data：未解析的Json对象，也可以是Json列表对象
                - record_path：列表或字符串，如果Json对象中的嵌套列表未在此设置，则完成解析后会直接将其整个列表存储到一列中展示
                - meta：Json对象中的键，存在多层数据时也可以进行嵌套标记
                - meta_prefix：键的前缀
                - record_prefix：嵌套列表的前缀
                - errors：错误信息，可设置为ignore，表示如果key不存在则忽略错误，也可设置为raise，表示如果key不存在则报错进行提示。默认值为raise
                - sep：多层key之间的分隔符，默认值是.（一个点）
                - max_level：解析Json对象的最大层级数，适用于有多层嵌套的Json对象
Change History:

"""
import pandas as pd


def main():
    json_obj = {
        'school': 'ABC primary school',
        'location': 'London',
        'ranking': 2,
        'info': {
            'president': 'John Kasich',
            'contacts': {
                'email': {
                    'admission': 'admission@abc.com',
                    'general': 'info@abc.com'
                },
                'tel': '123456789',
            }
        }
    }
    df = pd.json_normalize(json_obj)
    # df.to_excel('Result_json_to_xlsx.xlsx', encoding='utf-8', index=False)
    print(df)


if __name__ == '__main__':
    main()
