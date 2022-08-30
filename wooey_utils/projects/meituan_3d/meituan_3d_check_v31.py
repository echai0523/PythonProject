# import perception_3d_label_pb2
from labeling_proto_v2 import perception_3d_label_pb2 as perception_3d_label_pb2_v2
from scipy.spatial.transform import Rotation as R
import numpy as np
import cv2
import sys
import os
import math
import json
import glob

CLS = str(
    "pedestrian,deformed_pedestrian,elderly_mobility_scooter,minibus,car,bigcar,engineering_vehicle,cyclist,motorlist,tricycle_rider,scooter,animal"
).split(",")
ALL_CLS = str(
    "pedestrian,deformed_pedestrian,elderly_mobility_scooter,minibus,car,bigcar,engineering_vehicle,cyclist,motorlist,tricycle_rider,cart,other_cart,tricycle,low_barrier,noise,cone_bucket,water_filled_barrier,anti_collision_bucket,warning_sign,construction_sign,other_unknown,construction_site,no_labeling_zone,scooter,animal,ground"
).split(",")
RIGID_CLS = str(
    "elderly_mobility_scooter,minibus,car,bigcar,engineering_vehicle").split(
    ",")
STATIC_CLS = str(
    "cone_bucket,water_filled_barrier,anti_collision_bucket,warning_sign,construction_sign,other_unknown"
).split(",")

MAX_TRACKING_DISAPPEAR_LEN = 10
IOU_THRESHOLD = 0.3
NOISE_BOX_MIN_Z = 2.5
MIN_MOTION_STATE_AGE = 3
MAX_TRACK_ANGLE_DIFF = 90
MIN_DYNAMIC_TRACK_POSITION_DIFF = 0.02
MAX_STATIC_TRACK_POSITION_STD_VAR = 0.2


def cal_iou_2d_rotate(box1, box2):
    area1 = box1[2] * box1[3]
    area2 = box2[2] * box2[3]

    rect1 = ((box1[0], box1[1]), (box1[2], box1[3]), box1[4] * 180 / np.pi)
    rect2 = ((box2[0], box2[1]), (box2[2], box2[3]), box2[4] * 180 / np.pi)

    inter_points = cv2.rotatedRectangleIntersection(rect1, rect2)[1]
    iou = 0.0
    if inter_points is not None:
        order_points = cv2.convexHull(inter_points, returnPoints=True)
        inter_area = cv2.contourArea(order_points)
        iou = inter_area * 1.0 / (area1 + area2 - inter_area + 1e-6)
    return iou


def get_bbox2d_from_bbox3d(bboxes_3d):
    bbox_2d = []
    for box_3d in bboxes_3d:
        x = box_3d.box3d_position.x
        y = box_3d.box3d_position.y
        w = box_3d.box3d_dimension.width
        l = box_3d.box3d_dimension.length
        theta = box_3d.heading
        bbox_2d.append(np.array([x, y, w, l, -theta]))
    return np.array(bbox_2d)


def check_anno_num(labeled_sequence, seq_result_dict, seq_error_dict):
    total_bbox = []
    each_frame_bbox = []
    each_frame_index = []
    class_count_dict = {}
    tracking_id_dict = {}
    tracking_id_index_dict = {}
    static_tracking_id_dict = {}
    static_lidar_to_world_dict = {}
    dynamic_tracking_id_dict = {}
    dynamic_lidar_to_world_dict = {}
    labeled_frames = labeled_sequence.frames
    for labeled_frame in labeled_frames:
        label = labeled_frame.label
        labeled_boxes = label.lidar_box3d
        for labeled_box in labeled_boxes:
            total_bbox.append(labeled_box)
        labeled_boxes = [
            labeled_box for labeled_box in labeled_boxes
            if perception_3d_label_pb2_v2.ClassName.Name(
                labeled_box.box3d_info.class_name) != "NOISE"
        ]
        each_frame_bbox.append(labeled_boxes)
        each_frame_index.append(label.sequence_index)
        labeled_frame_tracking_id = []
        for labeled_box in labeled_boxes:
            box_heading = labeled_box.heading
            if box_heading < -np.pi or box_heading >= np.pi:
                seq_result_dict["CriticalError"].append(
                    "box heading: box heading value beyond [-np.pi, np.pi) range, sequence_index: %d， tracking_id: %d"
                    %
                    (label.sequence_index, labeled_box.box3d_info.tracking_id))
                error_key = (str(label.sequence_index) + "_" +
                             str(labeled_box.box3d_info.tracking_id))
                seq_error_dict[error_key] = 1
            box_info = labeled_box.box3d_info
            box_tracking_id = box_info.tracking_id
            if (perception_3d_label_pb2_v2.ClassName.Name(
                    labeled_box.box3d_info.class_name) != "NOISE"):
                labeled_frame_tracking_id.append(box_tracking_id)
            # check class name
            box_cls_name = perception_3d_label_pb2_v2.ClassName.Name(
                box_info.class_name)
            if box_cls_name.lower() not in ALL_CLS:
                seq_result_dict["CriticalError"].append(
                    "box class name: box class name %s not in defined class, sequence_index: %d"
                    % (box_cls_name, label.sequence_index))
                error_key = (str(label.sequence_index) + "_" +
                             str(labeled_box.box3d_info.tracking_id))
                seq_error_dict[error_key] = 1
            if box_cls_name in class_count_dict.keys():
                class_count_dict[box_cls_name] += 1
            else:
                class_count_dict[box_cls_name] = 1
            # check tracking id
            if (box_cls_name.lower() in CLS
                    and box_cls_name.lower() != "deformed_pedestrian"):
                if box_tracking_id in tracking_id_dict:
                    tracking_id_dict[box_tracking_id].append(labeled_box)
                else:
                    tracking_id_dict[box_tracking_id] = [labeled_box]
                if box_tracking_id in tracking_id_index_dict:
                    tracking_id_index_dict[box_tracking_id].append(
                        label.sequence_index)
                else:
                    tracking_id_index_dict[box_tracking_id] = [
                        label.sequence_index
                    ]
                box_motion_state = perception_3d_label_pb2_v2.MotionState.Name(
                    box_info.box3d_attribute.motion_state)
                if box_motion_state == "STATIONARY":
                    if box_tracking_id in dynamic_tracking_id_dict:
                        if len(dynamic_tracking_id_dict[box_tracking_id]) < MIN_MOTION_STATE_AGE:
                            seq_result_dict["CriticalError"].append(
                                "motion state: box tracking id: %d, motion state STATIONARY after short MOVING for class :%s"
                                % (box_tracking_id, box_cls_name))
                        del dynamic_tracking_id_dict[box_tracking_id]
                        del dynamic_lidar_to_world_dict[box_tracking_id]
                    if box_tracking_id in static_tracking_id_dict:
                        static_tracking_id_dict[box_tracking_id].append(
                            labeled_box)
                        static_lidar_to_world_dict[box_tracking_id].append(
                            labeled_frame.data.lidar_to_world)
                    else:
                        static_tracking_id_dict[box_tracking_id] = [
                            labeled_box
                        ]
                        static_lidar_to_world_dict[box_tracking_id] = [
                            labeled_frame.data.lidar_to_world
                        ]
                elif box_motion_state == "MOVING":
                    if box_tracking_id in static_tracking_id_dict:
                        if len(static_tracking_id_dict[box_tracking_id]) < MIN_MOTION_STATE_AGE:
                            seq_result_dict["CriticalError"].append(
                                "motion state: box tracking id: %d, motion state MOVING after short STATIONARY for class :%s"
                                % (box_tracking_id, box_cls_name))
                        del static_tracking_id_dict[box_tracking_id]
                        del static_lidar_to_world_dict[box_tracking_id]
                    if box_tracking_id in dynamic_tracking_id_dict:
                        dynamic_tracking_id_dict[box_tracking_id].append(
                            labeled_box)
                        dynamic_lidar_to_world_dict[box_tracking_id].append(
                            labeled_frame.data.lidar_to_world)
                    else:
                        dynamic_tracking_id_dict[box_tracking_id] = [
                            labeled_box]
                        dynamic_lidar_to_world_dict[box_tracking_id] = [
                            labeled_frame.data.lidar_to_world
                        ]
        if len(set(labeled_frame_tracking_id)) != len(labeled_boxes):
            seq_result_dict["CriticalError"].append(
                "tracking id: same tracking id appear in same labeled frame, sequence_index: %d"
                % (label.sequence_index))
            error_key = (str(label.sequence_index) + "_" +
                         str(labeled_box.box3d_info.tracking_id))
            seq_error_dict[error_key] = 1
    if len(total_bbox) == 0:
        seq_result_dict["CriticalError"].append(
            "sequence labeled box num is equal to zero")
    return (total_bbox, each_frame_bbox, each_frame_index, class_count_dict,
            tracking_id_dict, tracking_id_index_dict, static_tracking_id_dict,
            seq_error_dict, static_lidar_to_world_dict, seq_result_dict,
            dynamic_tracking_id_dict, dynamic_lidar_to_world_dict)


def check_noise(labeled_sequence, seq_result_dict, seq_error_dict):
    for labeled_frame in labeled_sequence.frames:
        frame_index = labeled_frame.label.sequence_index
        labeled_boxes = labeled_frame.label.lidar_box3d
        noise_boxes = [
            labeled_box for labeled_box in labeled_boxes
            if perception_3d_label_pb2_v2.ClassName.Name(
                labeled_box.box3d_info.class_name) == "NOISE"
        ]
        if len(noise_boxes) > 0:
            # check noise box bottom z value
            for box in noise_boxes:
                box_bottom_z = box.box3d_position.z - box.box3d_dimension.height / 2.0
                if box_bottom_z > NOISE_BOX_MIN_Z:
                    seq_result_dict["CriticalError"].append(
                        "Noise: bottom z value > %.4f, sequence_index: %d" %
                        (NOISE_BOX_MIN_Z, frame_index))
                    error_key = (str(frame_index) + "_" + str(-1))
                    seq_error_dict[error_key] = 1
            # check iou
            bbox_2d = get_bbox2d_from_bbox3d(noise_boxes)
            for i in range(len(bbox_2d) - 1):
                for j in range(i + 1, len(bbox_2d)):
                    iou = cal_iou_2d_rotate(bbox_2d[i], bbox_2d[j])
                    if iou > IOU_THRESHOLD:
                        seq_result_dict["Error"].append(
                            "Noise: sequence_index %d, tracking_id %d, iou = %.4f > 0"
                            % (frame_index,
                               noise_boxes[i].box3d_info.tracking_id, iou))
                        error_key = (
                                str(frame_index) + "_" +
                                str(noise_boxes[j].box3d_info.tracking_id))
                        seq_error_dict[error_key] = 1
    return seq_result_dict, seq_error_dict


def check_track_disappear_len(tracking_id_dict, tracking_id_index_dict,
                              seq_result_dict, seq_error_dict):
    for key in tracking_id_dict.keys():
        seq_index_all = tracking_id_index_dict[key]
        if len(seq_index_all) > 2:
            margin_seq_index = seq_index_all[:-1]
            margin_seq_index.insert(0, 0)
            margin = max(
                (np.array(seq_index_all) - np.array(margin_seq_index))[1:])
            if margin > MAX_TRACKING_DISAPPEAR_LEN:
                seq_result_dict["Error"].append(
                    "check_track_disappear_len: tracking id %s max margin %d greater than %d"
                    % (key, margin, MAX_TRACKING_DISAPPEAR_LEN))
                margin_array = (np.array(seq_index_all) -
                                np.array(margin_seq_index))[1:]
                for i, array_i in enumerate(margin_array):
                    if array_i > MAX_TRACKING_DISAPPEAR_LEN:
                        for j in range(i, len(margin_array)):
                            error_key = str(seq_index_all[j]) + "_" + str(key)
                            seq_error_dict[error_key] = 1
                        break
    return seq_result_dict, seq_error_dict


def check_seq_stability(tracking_id_dict, tracking_id_index_dict,
                        seq_result_dict, seq_error_dict):
    for key, value in tracking_id_dict.items():
        seq_index_all = tracking_id_index_dict[key]
        box_dimension_dict = {
            "w": [],
            "h": [],
            "l": [],
        }
        cls = perception_3d_label_pb2_v2.ClassName.Name(
            value[0].box3d_info.class_name)
        if cls.lower() not in CLS or cls.lower() == "deformed_pedestrian":
            continue
        for bbox in value:
            box_dimension_dict["w"].append(bbox.box3d_dimension.width)
            box_dimension_dict["h"].append(bbox.box3d_dimension.height)
            box_dimension_dict["l"].append(bbox.box3d_dimension.length)
        for dimension, dimension_list in box_dimension_dict.items():
            if len(set(dimension_list)) > 1:
                seq_result_dict["Error"].append(
                    "check_seq_stability: tracking_id %d, %s dimension of the same object differs in frames"
                    % (bbox.box3d_info.tracking_id, dimension))
                error_key = str(seq_index_all[0]) + "_" + str(key)
                seq_error_dict[error_key] = 1
    return seq_result_dict, seq_error_dict


def check_box_collision(each_frame_bbox, each_frame_index, seq_result_dict,
                        seq_error_dict):
    for file_index in range(len(each_frame_bbox)):
        bbox_2d = []
        if len(each_frame_bbox[file_index]) > 0:
            bbox_2d = get_bbox2d_from_bbox3d(each_frame_bbox[file_index])
            for i in range(len(bbox_2d) - 1):
                for j in range(i + 1, len(bbox_2d)):
                    iou = cal_iou_2d_rotate(bbox_2d[i], bbox_2d[j])
                    if iou > IOU_THRESHOLD:
                        seq_result_dict["Error"].append(
                            "check_box_collision: sequence_index %d, tracking_id %d, iou = %.4f > 0"
                            % (each_frame_index[file_index],
                               each_frame_bbox[file_index]
                               [i].box3d_info.tracking_id, iou))
                        error_key = (str(each_frame_index[file_index]) + "_" +
                                     str(each_frame_bbox[file_index]
                                         [j].box3d_info.tracking_id))
                        seq_error_dict[error_key] = 1
    return seq_result_dict, seq_error_dict


def check_sequence_index_value(frames, seq_result_dict):
    all_sequence_index = []
    for frame in frames:
        all_sequence_index.append(frame.label.sequence_index)
    if len(set(all_sequence_index)) != len(frames):
        seq_result_dict["CriticalError"].append(
            "check_sequence_index_value: sequence_index value not assigned")
    return seq_result_dict


def local_to_world(box, lidar_to_world):
    quaternion = [
        lidar_to_world.quaternion.x,
        lidar_to_world.quaternion.y,
        lidar_to_world.quaternion.z,
        lidar_to_world.quaternion.w,
    ]
    rotation_matrix = R.from_quat(quaternion).as_matrix()
    box_center = np.array(
        [box.box3d_position.x, box.box3d_position.y, box.box3d_position.z])
    global_position = np.dot(rotation_matrix, box_center) + np.array([
        lidar_to_world.translation.x,
        lidar_to_world.translation.y,
        lidar_to_world.translation.z,
    ])
    return global_position[:2]


def check_global_position_diff(boxes, lidar_to_worlds, max_std_diff):
    global_positions = []
    for box, lidar_to_world in zip(boxes, lidar_to_worlds):
        global_positions.append(local_to_world(box, lidar_to_world))
    global_positions = np.array(global_positions)
    position_x = global_positions[:, 0]
    position_y = global_positions[:, 1]
    x_var = np.std(position_x)
    y_var = np.std(position_y)
    if x_var > max_std_diff or y_var > max_std_diff:
        return False
    return True


def check_static_box_stability(static_tracking_id_dict,
                               static_lidar_to_world_dict, seq_result_dict):
    for key, value in static_tracking_id_dict.items():
        lidar_to_world = static_lidar_to_world_dict[key]
        if len(value) > 1:
            flag = check_global_position_diff(value, lidar_to_world,
                                              MAX_STATIC_TRACK_POSITION_STD_VAR)
            if not flag:
                seq_result_dict["Error"].append(
                    "check_static_box_stability: tracking_id %d, static box location differ exceed the limit"
                    % key)
    return seq_result_dict


def check_global_position_moving(boxes, lidar_to_worlds, min_postion_diff):
    global_positions = []
    for box, lidar_to_world in zip(boxes, lidar_to_worlds):
        global_positions.append(local_to_world(box, lidar_to_world))
    global_positions = np.array(global_positions)
    position_x = global_positions[:, 0]
    position_y = global_positions[:, 1]
    for i in range(len(position_x) - 1):
        position_x_diff = abs(position_x[i + 1] - position_x[i])
        position_y_diff = abs(position_y[i + 1] - position_y[i])
        if position_x_diff < min_postion_diff and position_y_diff < min_postion_diff:
            return False
    return True


def check_dynamic_box_validity(dynamic_tracking_id_dict, dynamic_lidar_to_world_dict, seq_result_dict):
    for key, value in dynamic_tracking_id_dict.items():
        lidar_to_world = dynamic_lidar_to_world_dict[key]
        if len(value) > 1:
            flag = check_global_position_moving(value, lidar_to_world,
                                                MIN_DYNAMIC_TRACK_POSITION_DIFF)
            if not flag:
                seq_result_dict["Error"].append(
                    "check_dynamic_box_validity: tracking_id %d, dynamic box position diff is too small"
                    % key)
    return seq_result_dict


def check_track_type_consistency(labeled_sequence, seq_result_dict):
    labeled_frames = labeled_sequence.frames
    tracking_dict = {}
    for labeled_frame in labeled_frames:
        labeled_boxes = labeled_frame.label.lidar_box3d
        for labeled_box in labeled_boxes:
            box_tracking_id = labeled_box.box3d_info.tracking_id
            if box_tracking_id in tracking_dict:
                tracking_dict[box_tracking_id].append(labeled_box)
            else:
                tracking_dict[box_tracking_id] = [labeled_box]
    for key, value in tracking_dict.items():
        track_class_list = []
        if len(value) > 2:
            for box in value:
                track_class_list.append(
                    perception_3d_label_pb2_v2.ClassName.Name(
                        box.box3d_info.class_name).lower())
        if len(set(track_class_list)) > 1 and set(track_class_list) != (
                "pedestrian", "deformed_pedestrian"):
            seq_result_dict["Error"].append(
                "check_track_type_consistency: tracking_id %d's type is not consistent in the whole track"
                % (key))
    return seq_result_dict


def check_attribute_is_movable_consistency(labeled_sequence, seq_result_dict):
    labeled_frames = labeled_sequence.frames
    tracking_dict = {}
    for labeled_frame in labeled_frames:
        labeled_boxes = labeled_frame.label.lidar_box3d
        labeled_boxes = [
            labeled_box for labeled_box in labeled_boxes
            if perception_3d_label_pb2_v2.ClassName.Name(
                labeled_box.box3d_info.class_name).lower() == "low_barrier"
        ]
        for labeled_box in labeled_boxes:
            box_tracking_id = labeled_box.box3d_info.tracking_id
            if box_tracking_id in tracking_dict:
                tracking_dict[box_tracking_id].append(labeled_box)
            else:
                tracking_dict[box_tracking_id] = [labeled_box]
    for key, value in tracking_dict.items():
        track_attribute_list = []
        if len(value) > 2:
            for box in value:
                track_attribute_list.append(
                    box.box3d_info.box3d_attribute.is_movable)
        if len(set(track_attribute_list)) > 1:
            seq_result_dict["Error"].append(
                "check_attribute_is_movable_consistency: tracking_id %d is_movable attribute not consistent in the whole track"
                % (key))
    return seq_result_dict


def check_sequence_length_consistency(labeled_sequence, seq_result_dict):
    labeled_frames = labeled_sequence.frames
    labeled_frames_length = len(labeled_frames)
    sequence_len = labeled_sequence.sequence_info.sequence_len
    if labeled_frames_length != sequence_len:
        seq_result_dict["Error"].append(
            "check_sequence_length_consistency: labeled_frames_length: %d, sequence_len: %d"
            % (labeled_frames_length, sequence_len))
    return seq_result_dict


def check_sequence(labeled_sequence, seq_result_dict, seq_error_dict):
    # output version and sequence info
    sequence_info = labeled_sequence.sequence_info
    version_info = labeled_sequence.version_info

    seq_result_dict["Info"] = {}
    seq_result_dict["Info"]["Version"] = version_info.version
    seq_result_dict["Info"][
        "TimePeriod"] = perception_3d_label_pb2_v2.TimePeriod.Name(
        sequence_info.time_period)
    seq_result_dict["Info"]["Season"] = sequence_info.season
    seq_result_dict["Info"]["Weather"] = sequence_info.weather
    seq_result_dict["Info"]["Location"] = sequence_info.location
    seq_result_dict["Info"]["Time"] = sequence_info.time
    seq_result_dict["Info"]["SequenceLen"] = sequence_info.sequence_len
    seq_result_dict["Info"]["LabelPurpose"] = []
    for purpose in sequence_info.label_purpose:
        seq_result_dict["Info"]["LabelPurpose"].append(
            perception_3d_label_pb2_v2.LabelPurpose.Name(purpose))

    # check sequence index value
    seq_result_dict = check_sequence_index_value(labeled_sequence.frames,
                                                 seq_result_dict)

    # check anno num
    (total_bbox, each_frame_bbox, each_frame_index, class_count_dict,
     tracking_id_dict, tracking_id_index_dict, static_tracking_id_dict,
     seq_error_dict, static_lidar_to_world_dict,
     seq_result_dict,
     dynamic_tracking_id_dict, dynamic_lidar_to_world_dict) = check_anno_num(labeled_sequence, seq_result_dict,
                                                                             seq_error_dict)

    # check noise labeling
    seq_result_dict, seq_error_dict = check_noise(labeled_sequence,
                                                  seq_result_dict,
                                                  seq_error_dict)

    # check each frame box collision
    seq_result_dict, seq_error_dict = check_box_collision(
        each_frame_bbox, each_frame_index, seq_result_dict, seq_error_dict)

    # check tracking anno
    seq_result_dict, seq_error_dict = check_track_disappear_len(
        tracking_id_dict, tracking_id_index_dict, seq_result_dict,
        seq_error_dict)

    # check sequence stability
    seq_result_dict, seq_error_dict = check_seq_stability(
        tracking_id_dict, tracking_id_index_dict, seq_result_dict,
        seq_error_dict)

    # check static object stability
    seq_result_dict = check_static_box_stability(static_tracking_id_dict,
                                                 static_lidar_to_world_dict,
                                                 seq_result_dict)

    # check dynamic object validity
    seq_result_dict = check_dynamic_box_validity(dynamic_tracking_id_dict,
                                                 dynamic_lidar_to_world_dict,
                                                 seq_result_dict)

    # check track type consistency
    seq_result_dict = check_track_type_consistency(labeled_sequence,
                                                   seq_result_dict)

    # check low_barrier is_movable consistency
    seq_result_dict = check_attribute_is_movable_consistency(
        labeled_sequence, seq_result_dict)

    # check sequence length consistency
    seq_result_dict = check_sequence_length_consistency(
        labeled_sequence, seq_result_dict)

    return seq_result_dict, seq_error_dict, class_count_dict, total_bbox


def meituan_3d_check_main_func(labeled_data_dir, json_file):
    # assert (len(sys.argv) == 3
    #         ), "Must input labeled data dir and check result json file"
    # labeled_data_dir = sys.argv[1]
    # json_file = sys.argv[2]

    total_error_count = 0
    total_box_count = 0
    check_result_list = []
    for batch_dir in sorted(os.listdir(labeled_data_dir)):
        if batch_dir == ".DS_Store":
            continue
        batch_dir = os.path.join(labeled_data_dir, batch_dir)
        for record_dir in sorted(os.listdir(batch_dir)):
            if record_dir == ".DS_Store":
                continue
            record_dir = os.path.join(batch_dir, record_dir)
            for seq_task_dir in sorted(
                    os.listdir(os.path.join(record_dir, "pc_task"))):
                if seq_task_dir == ".DS_Store":
                    continue
                seq_task_dir = os.path.join(record_dir, "pc_task",
                                            seq_task_dir)
                seq_result_dict = {}
                seq_error_dict = {}

                seq_result_dict["Error"] = []
                seq_result_dict["CriticalError"] = []

                # basic result info
                seq_result_dict["BatchName"] = batch_dir.split("/")[-1]
                seq_result_dict["Record"] = record_dir.split("/")[-1]
                seq_result_dict["SeqTask"] = seq_task_dir.split("/")[-1]

                labeled_sequence_proto = glob.glob(
                    os.path.join(seq_task_dir, "*.proto"))[0]

                labeled_sequence = perception_3d_label_pb2_v2.LabeledSequence()
                with open(labeled_sequence_proto, "rb") as f:
                    labeled_sequence.ParseFromString(f.read())

                seq_result_dict, seq_error_dict, class_count_dict, total_bbox = check_sequence(
                    labeled_sequence, seq_result_dict, seq_error_dict)

                # output info
                seq_result_dict["Statistics"] = {}
                seq_result_dict["Statistics"][
                    "ClassDistribution"] = class_count_dict
                seq_result_dict["Statistics"]["LabeledBox"] = len(total_bbox)
                seq_result_dict["Statistics"]["ErrorBox"] = len(seq_error_dict)
                seq_result_dict["Statistics"]["ErrorRate"] = float(
                    len(seq_error_dict)) / len(total_bbox)

                total_error_count += len(seq_error_dict)
                total_box_count += len(total_bbox)
                check_result_list.append(seq_result_dict)

    check_result_dict = {}
    check_result_dict["CheckResult"] = check_result_list
    with open(json_file, 'w') as f:
        json.dump(check_result_dict, f, indent=4, sort_keys=True)
