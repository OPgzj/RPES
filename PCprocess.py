import cv2
import numpy as np
from matplotlib import pyplot as plt
import open3d as o3d
from PhenoEx import get_gray
import pandas as pd
import os
import sys

param1 = "calibration_results.npz"

# 生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_params(param_root):
    with np.load(param_root) as data:
        return (data['left_camera_matrix'],
                data['right_camera_matrix'],
                data['left_distortion_coefficients'],
                data['right_distortion_coefficients'],
                data['rotation_matrix'],
                data['translation_vector'],
                data['essential_matrix'],
                data['fundamental_matrix']
               )

def undistortion(Limg, Rimg):
    mtx_left, mtx_right, dist_left, dist_right, R, T, E, F = get_params(resource_path(os.path.join("res", param1)))
    image_size = (2448, 2048)

    # 计算投影矩阵
    R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(mtx_left, dist_left, mtx_right, dist_right,
                                                                      image_size, R, T)
    # 计算左右映射矩阵
    left_map1, left_map2 = cv2.initUndistortRectifyMap(mtx_left, dist_left, R1, P1, image_size, 5)
    right_map1, right_map2 = cv2.initUndistortRectifyMap(mtx_right, dist_right, R2, P2, image_size, 5)
    # 使用左右映射矩阵进行图像矫正
    left_rect = cv2.remap(Limg, left_map1, left_map2, cv2.INTER_LINEAR)
    right_rect = cv2.remap(Rimg, right_map1, right_map2, cv2.INTER_LINEAR)
    return left_rect, right_rect, Q

def process_disparity(disparity, scale = 4):
    size = (int(2448/scale),int(2048/scale))
    # 找到视差图中的最大视差值
    max_disparity = np.max(disparity)
    # 将视差图缩放到 0-255 并转换为 uint8
    disparity_scaled = (disparity.astype(np.float32) * 255 / max_disparity).astype(np.uint8)
    disparity_color = cv2.applyColorMap(disparity_scaled, cv2.COLORMAP_OCEAN)
    resized = cv2.resize(disparity_color, size)
    return resized

def get_disparity(Limg, Rimg):
    num = 44
    blockSize = 9
    minDisprt = 0  # 最小视差值(int类型)，通常情况下为0。此参数决定左图中的像素点在右图匹配搜索的起点。最小视差值越小，视差图右侧的黑色区域越大
    numDisprt = 16 * num  # 视差搜索范围，其值必须为16的整数倍且大于0。视差窗口越大，视差图左侧的黑色区域越大
    gray_L = get_gray(Limg)
    gray_R = get_gray(Rimg)
    stereo_sgbm = cv2.StereoSGBM_create(
        # minDisparity = minDisprt,
        numDisparities=numDisprt,
        blockSize=blockSize,  # SAD代价计算的窗口大小,大于1的奇数。默认为5,一般在5~21之间
        # P1=8 * 3 * blockSize **2 , # P1是相邻像素点视差增/减 1 时的惩罚系数；需要指出，在动态规划时，P1和P2都是常数。一般：P1=8*通道数*blockSize**2，P2=4*P1
        # P2=32 * 3* blockSize **2,  # P2是相邻像素点视差变化值大于1时的惩罚系数。P2必须大于P1。p2值越大，差异越平滑
        preFilterCap=20,  # 图像预处理参数，水平sobel预处理后，映射滤波器大小。默认为15
        uniquenessRatio=5,  # 代价是次低代价的(1+uniquenessRatio/100)倍时，最低代价对应的视差值才是该像素点的视差，通常为5~15.
        # speckleRange=255,  # 视差变化阈值，每个连接组件内的最大视差变化。如果你做斑点过滤，将参数设置为正值，它将被隐式乘以16.通常，1或2就足够好了
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY  # 指定了算法应该使用三路策略来进行匹配代价的计算
    )

    # 计算视差: 根据SGBM方法生成差异图
    disparity = stereo_sgbm.compute(gray_L, gray_R)

    disparity_color = process_disparity(disparity, scale=2)

    return disparity, disparity_color

def get_pointclouds(disparity, Q, image, path):
    # 生成3D点云
    points = cv2.reprojectImageTo3D(disparity, Q)
    colors = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mask = disparity > disparity.min()
    output_points = points[mask]
    output_colors = colors[mask]
    output_mask = (output_colors[:, 0] >= 80) & (output_colors[:, 1] >= 80) & (output_colors[:, 2] >= 30)
    output_points = output_points[output_mask]
    output_colors = output_colors[output_mask]
    # 保留深度的部分
    depth_mask = output_points[:, 2] < 25
    output_points = output_points[depth_mask]
    output_colors = output_colors[depth_mask]

    # # X值裁剪
    # x_mask = output_points[:, 0] <= 4.5
    # output_points = output_points[x_mask]
    # output_colors = output_colors[x_mask]

    # Y值裁剪
    y_mask = output_points[:, 1] <= 6
    output_points = output_points[y_mask]
    output_colors = output_colors[y_mask]

    # Y值裁剪
    y_mask = output_points[:, 1] >= -4
    output_points = output_points[y_mask]
    output_colors = output_colors[y_mask]

    # 保存ply点云文件
    ply_path = path + ".ply"

    header = f"""ply
    format ascii 1.0
    element vertex {len(output_points)}
    property float x
    property float y
    property float z
    property uchar red
    property uchar green
    property uchar blue
    end_header
    """
    with open(ply_path, 'w') as f:
        f.write(header)
        for point, color in zip(output_points, output_colors):
            f.write(f"{point[0]} {point[1]} {point[2]} {color[0]} {color[1]} {color[2]}\n")
    # Save point cloud as PCD file
    ply = o3d.io.read_point_cloud(ply_path)
    pcd_path = path + ".pcd"
    o3d.io.write_point_cloud(pcd_path, ply)

def filter_pc(pcd):
    nb_neighbors = 25  # 邻域内点的数量
    std_ratio = 1  # 标准差阈值

    f_pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio, print_progress=False)
    return f_pcd

def downsampling(pcd):
    # 下采样
    downpcd = pcd.voxel_down_sample(voxel_size=0.05)
    return downpcd

def clustering(pcd):
    clst = np.array(pcd.cluster_dbscan(eps=0.12, min_points=10, print_progress=False))
    labels = clst.max()
    # 可视化聚类结果
    clst_colors = plt.get_cmap("tab20c")(clst / (labels if labels > 0 else 1))
    clst_colors[clst < 0] = 0  # 噪声为黑色
    clst_colors = clst_colors * 0.8  # 调整亮度以增加深度
    pcd.colors = o3d.utility.Vector3dVector(clst_colors[:, :3])
    return pcd, clst, labels

def get3dPheno(labels, clst, pcd, filepath):
    centers = []
    seeds_depth = []
    seeds_length = []
    seeds_width = []
    volumes = []

    for i in range(labels + 1):
        # 计算质心坐标
        index = np.where(clst == i)[0]
        cluster = pcd.select_by_index(index)
        center = cluster.get_center()
        centers.append(center)

        # 计算籽粒厚度
        depths = np.asarray(cluster.points)[:, 2]  # 提取所有点的深度值
        depth = (depths.max() - depths.min()) * 34  # 计算厚度
        seeds_depth.append(depth)

        # 计算籽粒长度
        lengths = np.asarray(cluster.points)[:, 1]  # 提取所有点的长度值
        length = (lengths.max() - lengths.min()) * 17  # 计算长度
        seeds_length.append(length)

        # 计算籽粒宽度
        widths = np.asarray(cluster.points)[:, 0]  # 提取所有点的宽度值
        width = (widths.max() - widths.min()) * 17  # 计算宽度
        seeds_width.append(width)

        # 三个方向的径长
        radius_x = length / 2
        radius_y = width / 2
        radius_z = depth / 2

        # 将籽粒近似为椭球计算体积
        volume = (4 / 3) * np.pi * radius_x * radius_y * radius_z  # 计算体积
        volumes.append(volume)

        # # 结果输出
        # print()
        # print("籽粒编号：", i + 1)
        # print("籽粒中心坐标：", center)
        # print("籽粒厚度：", "{:.3f}".format(depth), "mm")
        # print("籽粒长度：", "{:.3f}".format(length), "mm")
        # print("籽粒宽度：", "{:.3f}".format(width), "mm")
        # print("籽粒体积：", "{:.3f}".format(volume), "mm3")

    pheno = {
        "籽粒编号": list(range(labels+1)),
        "籽粒中心坐标": centers,
        "籽粒长度(mm)": seeds_length,
        "籽粒宽度(mm)": seeds_width,
        "籽粒厚度(mm)": seeds_depth,
        "籽粒体积(mm^3)": volumes
    }
    # 创建一个DataFrame
    pheno_df = pd.DataFrame(pheno)
    # 添加平均数据
    average_data = {
        "籽粒编号": "均值",
        "籽粒中心坐标": "",
        "籽粒长度(mm)": "{:.3f}".format(np.mean(seeds_length), ddof=1),
        "籽粒宽度(mm)": "{:.3f}".format(np.mean(seeds_width), ddof=1),
        "籽粒厚度(mm)": "{:.3f}".format(np.mean(seeds_depth), ddof=1),
        "籽粒体积(mm^3)": "{:.3f}".format(np.mean(volumes), ddof=1)
    }
    # print()
    # print("籽粒数量：", labels + 1)
    # print("平均厚度为：", "{:.3f}".format(np.mean(seeds_depth), ddof=1), "mm")
    # print("平均长度为：", "{:.3f}".format(np.mean(seeds_length), ddof=1), "mm")
    # print("平均宽度为：", "{:.3f}".format(np.mean(seeds_width), ddof=1), "mm")
    # print("平均体积为：", "{:.3f}".format(np.mean(volumes), ddof=1), "mm3")
    # 将平均数据作为一行添加到df中
    average_row = pd.DataFrame([average_data])
    df = pd.concat([pheno_df, average_row], ignore_index=True)

    # 将DataFrame写入CSV文件
    df.to_csv(filepath, index=False, encoding='utf-8-sig')

class PointCloudProcess:
    def __init__(self):
        self.L_img = None
        self.R_img = None
        self.pcd = None

    def preprocess(self):
        self.L_img, self.R_img, self.Q = undistortion(self.L_img, self.R_img)

    def get_disdep(self):
        self.dis, self.dis_color = get_disparity(self.L_img, self.R_img)

    def generate(self):
        # 生成3D点云
        points = cv2.reprojectImageTo3D(self.dis, self.Q)
        colors = cv2.cvtColor(self.L_img, cv2.COLOR_BGR2RGB)
        mask = self.dis > self.dis.min()
        output_points = points[mask]
        output_colors = colors[mask]
        output_mask = (output_colors[:, 0] >= 80) & (output_colors[:, 1] >= 80) & (output_colors[:, 2] >= 30)
        output_points = output_points[output_mask]
        output_colors = output_colors[output_mask]
        # 保留深度的部分
        depth_mask = output_points[:, 2] < 25
        output_points = output_points[depth_mask]
        output_colors = output_colors[depth_mask]
        # Y值裁剪
        y_mask = output_points[:, 1] <= 6
        output_points = output_points[y_mask]
        output_colors = output_colors[y_mask]
        # Y值裁剪
        y_mask = output_points[:, 1] >= -4
        output_points = output_points[y_mask]
        output_colors = output_colors[y_mask]/225.0

        self.pcd = o3d.geometry.PointCloud()
        self.pcd.points = o3d.utility.Vector3dVector(output_points)
        self.pcd.colors = o3d.utility.Vector3dVector(output_colors)

    def filter_pc(self):
        nb_neighbors = 25  # 邻域内点的数量
        std_ratio = 1  # 标准差阈值

        self.pcd, _ = self.pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio, print_progress=False)

    def downsampling(self):
        # 下采样
        self.pcd = self.pcd.voxel_down_sample(voxel_size=0.05)

    def display_pointcloud(self, pcd):
        # Visualize the point cloud
        o3d.visualization.draw_geometries([pcd])

    def save_pointcloud(self, path):
        # Save as PLY file
        ply_path = path + ".ply"
        o3d.io.write_point_cloud(ply_path, self.pcd)

        # Save as PCD file
        pcd_path = path + ".pcd"
        o3d.io.write_point_cloud(pcd_path, self.pcd)

    def get3dPheno(self):
        _,clst, labels = clustering(self.pcd)
        centers = []
        seeds_depth = []
        seeds_length = []
        seeds_width = []
        volumes = []

        for i in range(labels + 1):
            # 计算质心坐标
            index = np.where(clst == i)[0]
            cluster = self.pcd.select_by_index(index)
            center = cluster.get_center()
            centers.append(center)

            # 计算籽粒厚度
            depths = np.asarray(cluster.points)[:, 2]  # 提取所有点的深度值
            depth = (depths.max() - depths.min()) * 34  # 计算厚度
            seeds_depth.append(depth)

            # 计算籽粒长度
            lengths = np.asarray(cluster.points)[:, 1]  # 提取所有点的长度值
            length = (lengths.max() - lengths.min()) * 17  # 计算长度
            seeds_length.append(length)

            # 计算籽粒宽度
            widths = np.asarray(cluster.points)[:, 0]  # 提取所有点的宽度值
            width = (widths.max() - widths.min()) * 17  # 计算宽度
            seeds_width.append(width)

            # 三个方向的径长
            radius_x = length / 2
            radius_y = width / 2
            radius_z = depth / 2

            # 将籽粒近似为椭球计算体积
            volume = (4 / 3) * np.pi * radius_x * radius_y * radius_z  # 计算体积
            volumes.append(volume)

        return [labels+1, centers, seeds_length, seeds_width, seeds_depth,volumes]