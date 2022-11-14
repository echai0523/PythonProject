# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/10/19 17:57
input   : 
output  :   
Short Description: 
Change History:
"""
import os.path
import numpy as np
import open3d as o3d
from open3d import geometry
import warnings

pcd = o3d.geometry.PointCloud()
# print(np.asarray(pcd.points))

warnings.filterwarnings('ignore')

# kitti_path = "../EthanFileData/bin/1665739801.287219200_1.bin"
# l = np.fromfile(kitti_path, dtype=np.float32).reshape(-1, 5)[:, :3]
kitti_path = "../EthanFileData/File binary/1665739801.287219200_2.bin"
l = np.fromfile(kitti_path, dtype=np.float32).reshape(-1, 4)[:, :3]
ind = np.where(
    (l[:, 0] > -55) & (l[:, 0] < 55) &
    (l[:, 1] < 40) & (l[:, 1] > -40) &
    (l[:, 2] < 2) & (l[:, 2] > -3)
)
print(ind)
# crop_pcd = l[ind]
crop_pcd = l
pcd.points = o3d.utility.Vector3dVector(crop_pcd)
downpcd = pcd
# downpcd=pcd.voxel_down_sample(voxel_size=0.02)
# downpcd = pcd.voxel_down_sample(voxel_size=0.2)
downpoints = np.asarray(downpcd.points)
print('after down sampling, the shape is ', downpoints.shape)
o3d.visualization.draw_geometries([downpcd])