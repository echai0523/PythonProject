# -*- coding: UTF-8 -*-
"""
Author: Ethan Chai
Date: 2022/8/25 17:02

input:
output:

Short Description:
Change History:

"""
import re, os
from peutils.fileutil import list_current_file, list_files_deep


def main():
    org_path_list = list_current_file("FloW_IMG")
    for org_path in org_path_list:
        xml_org_path, image_org_path = list_current_file(org_path)
        xml_path_list = list_files_deep(xml_org_path)
        image_path_list = list_files_deep(image_org_path)

        for xml_path, image_path in zip(xml_path_list, image_path_list):
            with open(xml_path, 'r', encoding='utf-8') as rf:
                data = rf.read()
            try:
                xml_image_path = re.findall(r"<path>(.*)</path>", data)[0]
            except:
                xml_image_path = re.findall(r"<filename>(.*)</filename>", data)[0]

            xml_image_name = os.path.basename(xml_image_path)
            new_image = os.path.join("/".join(image_path.split("/")[:-1]), xml_image_name)
            os.rename(image_path, new_image)


if __name__ == "__main__":
    main()









