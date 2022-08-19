# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/8/18 21:57

input: 
output: 
Short Description: 
    - 需求：
        json数据一行显示，如何美观，层次显？少量json数据，可以通过文件工具快捷键进行格式化，那么有很多条json，每打开一个json就需要快捷键一次，很麻烦。
        制作一个gooey工具框架，内部编写功能脚本，实现JSON格式化工具，批量对JSON文件进行格式化。
        - 解析json文件夹
        - 利用json进行读取和写入
Change History:

"""
from gooey import Gooey, GooeyParser
import json
from peutils.fileutil import list_files_deep


def parse(json_list_path):
    # 解析json文件夹，方法可参考：FunctionZone/Os_Path/list_files_deep.py or https://www.cnblogs.com/icpy/p/16556531.html
    json_file_list = list_files_deep(json_list_path, suffix='.json')
    for file_path in json_file_list:
        with open(file_path, 'r', encoding='utf-8') as f:
            org_json = json.load(f)
        with open(file_path, 'w', encoding='utf-8') as wf:
            # indent格式化
            # ensure_ascii显示中文，不转码
            json.dump(org_json, wf, indent=4, ensure_ascii=False)


@Gooey(program_name='实现JSON格式化')
def main():
    parser = GooeyParser(description='JSON格式化')
    parser.add_argument('in_path', widget='DirChooser', metavar='选择输入目录', help='json文件夹')

    args = parser.parse_args()

    in_path = args.in_path
    parse(json_list_path=in_path)


if __name__ == '__main__':
    main()
