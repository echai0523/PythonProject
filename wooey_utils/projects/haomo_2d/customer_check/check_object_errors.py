#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import json
import argparse
from collections import OrderedDict
from tqdm.std import tqdm

haomo_classNames = ["car", "bus", "truck", "rider", "tricycle", "bicycle", "pedestrian", "other"]

vehicle = ["car", "bus", "truck"]
vru_3 = ["rider", "tricycle", "pedestrian"]
card_set = set()


def load_jsoninfos(data_path, ann_suffix=".json"):
    """
    Load imginfos from directory / json file
    """

    def load_from_dir():
        json_infos = []
        ind = 0
        for root, _, files in os.walk(data_path):
            for file in files:
                if file.endswith(".json"):
                    json_path = os.path.join(root, file)
                    json_infos.append(json_path)
        # print(json_infos)
        return json_infos

    if os.path.isdir(data_path):
        json_infos = load_from_dir()

    return json_infos


def parse_args():
    parser = argparse.ArgumentParser(description="Detection visualization")
    parser.add_argument("--data_path", help="Path to directory containing the annotated data", required=True)
    parser.add_argument("--error_file", default=None)
    return parser.parse_args()


class FormatCheck(object):
    def __init__(self, data_path, error_file) -> None:
        super().__init__()
        self.data_path = data_path
        self.error_file = error_file
        self.json_infos = load_jsoninfos(data_path)
        self.errors = OrderedDict()

    def check_key(self, key, json_cnt, type):
        value = json_cnt.get(key, None)
        # print(key, value)
        if value is not None:
            if not isinstance(value, type):
                if value == '' or value == ' ':
                    return f"Invalid Type and is empty str: {key}"
                if key == 'side_edge':
                    if isinstance(value, int):
                        return "Valid"
                return f"Invalid Type: {key}"
            elif json_cnt.get("className", None) == "bicycle":
                if value == {}:
                    return "Valid"
            elif value == {} or value == [] or value == ' ' or value == '' or value == None:
                if key == 'side_edge' or key == 'bottom_edge':
                    return "Valid"
                else:
                    return f"Invalid value is empty: {key}"
        else:
            return f"Missing: {key}"
        return "Valid"

    def check_range(self, key, json_cnt, type, range_list):
        value = json_cnt.get(key, None)
        if value is not None:
            if not isinstance(value, type):
                return f"Invalid Type: {key}"
            elif value not in range_list:
                return f"Invalid {key} out of range"
        else:
            # if key != "bicycle":
            return f"Missing: {key}"
        return "Valid"

    def check_bbox_point(self, key, json_cnt, type, img_width, img_height):
        value = json_cnt.get(key, None)
        if value is not None:
            if not isinstance(value, type):
                return f"Invalid Type: {key}"
            else:
                for i in range(len(value)):
                    if not isinstance(value[i], float) and not isinstance(value[i], int):
                        return f"Invalid value Type: {key}"
                    if key == 'bbox':
                        x, y, w, h = value
                        if (x < 0 or x > img_width) and (y < 0 or y > img_height) and (w <= 0 or w > img_width) and (
                                h <= 0 or h > img_height):
                            return f"Invalid bbox x, y, w or h"
                    else:
                        x, y = value
                        if (x < 0 or x > img_width) and (y < 0 or y > img_height):
                            return f"Invalid {key} x, y value"
        else:
            return f"Missing: {key}"
        return 'Valid'

    def update_errors(self, ret, json_path):
        if 'Valid' != ret and 'Normal' != ret:
            global card_set
            # dir_name = os.path.basename(os.path.dirname(json_path))
            dir_name = json_path  # zhang
            if ret not in self.errors:
                card_set = set()
                card_set.add(dir_name)
            else:
                self.errors[ret].add(dir_name)
            self.errors.setdefault(ret, card_set)

    def process(self):
        for idx in tqdm(range(len(self.json_infos)), ncols=100):
            json_path = self.json_infos[idx]
            with open(json_path, 'rb') as fjson:
                json_cnt = json.load(fjson)
            # producer
            ret = self.check_key('producer', json_cnt, str)
            self.update_errors(ret, json_path)

            # imgUrl
            ret = self.check_key('imgUrl', json_cnt, str)
            self.update_errors(ret, json_path)

            # imgHttp
            ret = self.check_key('imgHttp', json_cnt, str)
            self.update_errors(ret, json_path)

            # camera type
            ret = self.check_key('camera_type', json_cnt, str)
            self.update_errors(ret, json_path)

            # camera_orientation
            ret = self.check_key('camera_orientation', json_cnt, str)
            self.update_errors(ret, json_path)

            # width
            ret = self.check_key('width', json_cnt, int)
            self.update_errors(ret, json_path)

            # height
            ret = self.check_key('height', json_cnt, int)
            self.update_errors(ret, json_path)
            if ret == 'Valid':
                img_width = json_cnt['width']
                img_height = json_cnt['height']
            # else:
            #     img_no_w_h=Image.open(img_info['image'])
            #     img_width = img_no_w_h.size[0]
            #     img_height = img_no_w_h.size[1]

            # timestamp
            ret = self.check_key('timestamp', json_cnt, int)
            self.update_errors(ret, json_path)

            # objects
            ret = self.check_key('objects', json_cnt, list)
            self.update_errors(ret, json_path)

            if isinstance(json_cnt['objects'], list):
                for obj in json_cnt['objects']:
                    # id
                    ret = self.check_key('id', obj, int)
                    self.update_errors(ret, json_path)

                    # bbox
                    ret = self.check_bbox_point('bbox', obj, list, img_width, img_height)
                    self.update_errors(ret, json_path)

                    # className
                    ret = self.check_range('className', obj, str, haomo_classNames)
                    self.update_errors(ret, json_path)

                    if 'Valid' == ret:
                        # attributes
                        ret = self.check_key('attributes', obj, dict)
                        if obj['className'] == 'bicycle':  # 不判断自行车
                            if ret == "Missing: attributes":
                                ret = 'bicycle have no attributes, but it is normal'
                                # ret = 'Normal'
                            # elif ret == "Invalid value is empty: attributes":
                            #     ret = 'bicycle is empty, but it is normal'
                            #     # ret = 'Normal'
                        self.update_errors(ret, json_path)

                        if ret == 'Valid':
                            anno = obj['attributes']
                            if obj['className'] != "bicycle":
                                # occlusion
                                ret = self.check_range('occlusion', anno, int, [0, 1, 2])
                                self.update_errors(ret, json_path)
                                # truncation
                                ret = self.check_range('truncation', anno, int, [0, 1])
                                self.update_errors(ret, json_path)
                                # crowding
                                ret = self.check_range('crowding', anno, int, [0, 1, 2])
                                self.update_errors(ret, json_path)

                            if obj['className'] in vehicle:
                                # direction
                                ret = self.check_range('direction', anno, str,
                                                       ['left', 'right', 'front', 'behind', 'left_front', 'left_behind',
                                                        'right_front', 'right_behind'])
                                self.update_errors(ret, json_path)

                                # side_edge
                                ret_side_edge = self.check_key('side_edge', anno, float)
                                if ret_side_edge == "Missing: side_edge":
                                    ret_side_edge = "Normal"
                                self.update_errors(ret_side_edge, json_path)

                                # bottom_edge
                                ret_bottom_edge = self.check_key('bottom_edge', anno, dict)
                                if ret_bottom_edge == "Missing: bottom_edge":
                                    ret_bottom_edge = "Normal"
                                # elif 
                                self.update_errors(ret_bottom_edge, json_path)
                                if ret_bottom_edge == "Valid":
                                    bot = anno['bottom_edge']
                                    if bot != {}:
                                        # start_point
                                        ret = self.check_bbox_point('start_point', bot, list, img_width, img_height)
                                        self.update_errors(ret, json_path)

                                        # start_point_type
                                        ret = self.check_range('start_point_type', bot, str,
                                                               ['wheel_point', 'prediction_point'])
                                        self.update_errors(ret, json_path)

                                        # end_point
                                        ret = self.check_bbox_point('end_point', bot, list, img_width, img_height)
                                        self.update_errors(ret, json_path)

                                        # end_point_type
                                        ret = self.check_range('end_point_type', bot, str,
                                                               ['wheel_point', 'prediction_point'])
                                        self.update_errors(ret, json_path)

                            if obj['className'] in vru_3:
                                # onRoad
                                ret = self.check_range('onRoad', anno, int, [0, 1])
                                self.update_errors(ret, json_path)
                                if obj['className'] == 'pedestrian':
                                    # pose   standing\sitting\other
                                    ret = self.check_range('pose', anno, str, ['standing', 'sitting', 'other'])
                                    self.update_errors(ret, json_path)

    def dump(self):
        with open(self.error_file, 'w') as fjson:
            for err in self.errors.keys():
                self.errors[err] = list(self.errors[err])
            json.dump(self.errors, fjson, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', help='the path of json file or dir')
    parser.add_argument('--error_file', help='the path of error file')
    args = parser.parse_args()

    data_path = args.data_path
    error_file = args.error_file

    checker = FormatCheck(data_path, error_file)
    checker.process()
    checker.dump()
