# -*- coding: utf-8 -*-
"""
Author: Ethan Chai
Date: 2022/10/10 22:15
input:
output:
Short Description:
    - 无格式要求，只需要将平台数据转成labelme显示即可。
    - labelme框架结构
        {
            "version": "1.0.1",         # 设置手动输入
            "flags": {},                # 默认{}
            "shapes": [
                {
                    "label": "",        # 物体标签名
                    "line_color": [],   # 设置手动输入，默认None
                    "fill_color": [],   # 设置手动输入，默认None
                    "points": [],       # 点坐标
                    "shape_type": "",   # 框类型
                    "group_id": None,   # 默认None
                    "flags": {}         # 默认{}
                }
            ],
            "lineColor": [],            # 设置手动输入
            "fillColor": [],            # 设置手动输入
            "imagePath": "",            # 图片名
            "imageData": "",            # 设置手动输入是否需要生成图片字节数据，默认None
            "imageHeight": int,         # 图片高度
            "imageWidth": int           # 图片宽度
        }
Change History:
"""
from argparse import FileType
from peutils.transform.v1.base import get_session
from peutils.transform.v1.img_com.parser import ImgComParse, ImgComDataConfig
from peutils.transform.v1.task.executor import AbstractTask, CommonTaskV1
from peutils.wooeyutil import WooeyBaseZipHandlerFile
import sys, os, json, base64
from ast import literal_eval


class AfterParse(AbstractTask):
    def __init__(self, row, users_param=None):
        super().__init__(row, users_param)
        self.parse_obj = ImgComParse(row["annotation"], config=ImgComDataConfig())
        self.version = users_param['version']
        self.lineColor = self.color_parse(users_param['lineColor'])
        self.line_color = self.color_parse(users_param['line_color'])
        self.fillColor = self.color_parse(users_param['fillColor'])
        self.fill_color = self.color_parse(users_param['fill_color'])
        self.log.error_list.extend(self.parse_obj.check_frames_error())
        self.session = get_session()

    def check_row_on_a9(self) -> None:
        pass

    def check_row_addtional(self) -> None:
        pass

    def color_parse(self, color):
        # users_param转格式  str -> list/NoneType/···
        if color:
            return literal_eval(color)
        else:
            return None

    def get_img_base64(self, img_url):
        img_data = self.session.get(img_url).content
        if self.users_param['DownloadImage'] == '是':
            with open(os.path.basename(img_url), 'wb') as f:
                f.write(img_data)
        if self.users_param['imageData'] == '是':
            # Object of type bytes is not JSON serializable -> str(base64, encoding='utf-8')
            return str(base64.b64encode(img_data), encoding='utf-8')
        else:
            return None

    def process_label(self, a9_label):
        """
        把a9标注结果的单个框转成labelme的格式
        :param a9_label: # a9标注的单个object
        :return:
        """
        shape_type = a9_label.shapeType  # 框的类型
        polygon = a9_label.shape['points']  # 点坐标
        class_name = a9_label.instance.category  # 标签名
        polygon_dic = {
            "label": class_name,
            "line_color": self.line_color,
            "fill_color": self.fill_color,
            "points": [],
            "shape_type": shape_type,
            "group_id": None,
            "flags": {}
        }
        if shape_type == 'polygon':  # 多边形
            polygon_dic['points'] = [[p['x'], p['y']] for p in polygon]
            polygon_dic['shape_type'] = 'polygon'
        elif shape_type == 'dot':  # 点
            polygon_dic['points'] = [polygon['x'], polygon['y']]
            polygon_dic['shape_type'] = 'point'
        elif shape_type == 'rectangle':
            polygon_dic['shape_type'] = 'rectangle'
            polygon_dic['points'] = [[polygon[0]['x'], polygon[0]['y']], [polygon[2]['x'], polygon[2]['y']]]
        elif shape_type == 'line':
            polygon_dic['points'] = [[p['x'], p['y']] for p in polygon]
            if len(polygon) == 2:
                polygon_dic['shape_type'] = 'line'
            else:
                polygon_dic['shape_type'] = 'linestrip'
        else:
            print('ERROR,标注框类型为定义', file=sys.stderr)
        return polygon_dic

    def parse_row_func(self) -> None:
        for frame in self.parse_obj.frames_lst:
            img_url = frame.frameUrl
            img_name = os.path.basename(img_url)

            labelme_res_list = [self.process_label(item) for item in frame.frame_items]

            label_me_json = {
                "version": self.version,
                "flags": {},
                "shapes": labelme_res_list,
                "lineColor": self.lineColor,  # labelme json添加
                "fillColor": self.fillColor,  # labelme json添加
                "imagePath": img_name,
                "imageData": self.get_img_base64(img_url),
                "imageHeight": frame.imageHeight,
                "imageWidth": frame.imageWidth
            }

            with open(img_name.replace('.jpg', '.json'), mode='w', encoding='utf-8')as fw_json:
                json.dump(label_me_json, fw_json, ensure_ascii=False, indent=4)


# ct = CommonTaskV1(AfterParse, max_worker=1)
# ct.process_func(
#     "../../EthanFileData/csv/箱包后处理.csv",
#     version="3.4.5",
#     lineColor="[0, 255, 0, 128]",
#     fillColor="[255, 0, 0, 128]",
#     line_color="None",
#     fill_color="None",
#     imageData="否",
#     DownloadImage="是"
# )


if __name__ == '__main__':
    other_params = {
        "version": {
            "help": "输入版本号version",
            "type": str,
            "default": "3.4.5"
        },
        "lineColor": {
            "help": "输入外层lineColor, []内以英文逗号分割",
            "type": str,
            "default": "[0, 255, 0, 128]"
        },
        "fillColor": {
            "help": "输入外层fillColor, []内以英文逗号分割",
            "type": str,
            # "type": FileType('r'),
            "default": "[255, 0, 0, 128]"
        },
        "line_color": {
            "help": "输入内层line_color, []内以英文逗号分割",
            "type": str,
            "default": "None"
        },
        "fill_color": {
            "help": "输入内层fill_color, []内以英文逗号分割",
            "type": str,
            "default": "None"
        },
        "imageData": {
            "help": "是否写入ImageData,请注意：如果选择写入ImageData，生成的Json文件大小会很大。",
            "type": str,
            "default": "否",
            "choices": ["是", "否"]
        },
        "DownloadImage": {
            "help": "是否需要下载图片,请注意：图片保存位置与labelme json位置一致",
            "type": str,
            "default": "否",
            "choices": ["是", "否"]
        }
    }
    # labelme必须写入ImageData，取消选择框，写入ImageData
    h = WooeyBaseZipHandlerFile(
        project_desc="Labelme Json格式2d通用",
        need_process_suffix=".csv",
        process_func=CommonTaskV1(AfterParse, max_worker=1).process_func,
        other_params=other_params
    )
    sys.exit(h.main())
