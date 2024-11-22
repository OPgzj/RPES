import cv2
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import os
from skimage.feature import graycomatrix, graycoprops
import colorsys
from skimage import color
'''
对进行了中值滤波的灰度图进行二值化
接着是形态学处理，得到去噪二值图
接着进行长宽面积提取、颜色提取
'''

def set_chinese():
    # 设置Matplotlib使用SimHei字体显示中文
    plt.rcParams['font.family'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def get_Mfilted(img, size=3):
    # 定义滤波器的尺寸
    simg=cv2.medianBlur(img, size)
    return simg

def get_Gfilted(img, size=3,sigma=0):
    # 定义滤波器的尺寸
    filter_size = (size,size)
    simg=cv2.GaussianBlur(img,filter_size, sigma)
    return simg

def get_gray(cvimg):
    return cv2.cvtColor(cvimg, cv2.COLOR_BGR2GRAY)

def get_rgb(cvimg):
    b,g,r = cv2.split(cvimg)
    return r, g, b

def get_hsv(cvimg):
    # 将BGR图像转换为HSV图像
    hsv_image = cv2.cvtColor(cvimg, cv2.COLOR_BGR2HSV)
    # 分离HSV通道
    h, s, v = cv2.split(hsv_image)
    return h, s, v

def get_channels(img:np.ndarray):
    imgs = [img]
    imgs.append(get_gray(img))
    imgs.extend(get_rgb(img))
    imgs.extend(get_hsv(img))
    return imgs

def get_thresh(img,threshold = 65):
    bimg = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)[1]
    return bimg


def morphological_processing(binary_image):
    # 定义结构元素
    kernel = [np.ones((5, 5), np.uint8), np.ones((7, 7), np.uint8)]
    # 定义椭圆形kernel
    ellipse_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    # 定义十字形kernel
    cross_kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))

    mimg = [binary_image]  # 0
    mimg.append(cv2.morphologyEx(mimg[-1], cv2.MORPH_OPEN, cross_kernel))  # 1
    mimg.append(cv2.morphologyEx(mimg[-1], cv2.MORPH_OPEN, kernel[1]))  # 2
    # 膨胀操作

    mimg.append(cv2.dilate(mimg[-1], kernel[0], iterations=1))  # 3
    mimg.append(cv2.dilate(mimg[-1], kernel[0], iterations=1))  # 4
    mimg.append(cv2.morphologyEx(mimg[-1], cv2.MORPH_CLOSE, ellipse_kernel))  # 5
    mimg.append(cv2.erode(mimg[-1], kernel[0], iterations=2))  # 6
    return mimg[-1]

# 直接从二值图像中获取连通域信息
def get_stats(binary_image):
    _, _, stats, _ = cv2.connectedComponentsWithStats(binary_image, connectivity=8, ltype=cv2.CV_32S)
    return stats

def draw_rectangle_with_label(image, stats):
    copy = image.copy()
    # 遍历每个连通域
    for i, stat in enumerate(stats):
        # 获取矩形的左上角和右下角坐标
        left = stat[0]
        top = stat[1]
        width = stat[2]
        height = stat[3]

        # 绘制矩形框
        rectangle_color = (0, 0, 255)  # 红色矩形框
        rect_thickness = 2  # 矩形框的厚度
        cv2.rectangle(copy, (left, top), (left + width, top + height), rectangle_color, rect_thickness)

        # 添加索引到矩形框中间
        font_face = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_color = (255, 255, 0)  # 白色文本
        cv2.putText(copy, str(i+1), (left, top), font_face, font_scale, font_color, 1)
    return copy

def get_mask(image,binary_image):
    mask = np.uint8(binary_image/255)  # 转换为真正的2值
    sum_pixels = np.sum(mask)
    # 使用 expand_dims 来增加 temp 的维度，使其与 imgs[0] 的维度匹配
    mask = np.expand_dims(mask, axis=2)
    masked = mask * image  # 此时只有前景
    return masked, sum_pixels

def get_RGB(masked, sum_pixels):
    # mask = np.uint8(binary_image/255)  # 转换为真正的2值
    #
    # # 使用 expand_dims 来增加 temp 的维度，使其与 imgs[0] 的维度匹配
    # mask = np.expand_dims(mask, axis=2)
    # masked = mask * image  # 此时只有前景
    b = int(np.sum(masked[:, :, 0]) / sum_pixels)
    g = int(np.sum(masked[:, :, 1]) / sum_pixels)
    r = int(np.sum(masked[:, :, 2]) / sum_pixels)
    color_list = [r, g, b]
    color = "{:02}{:02}{:02}".format(r, g, b)
    return [color, color_list]

def get_RGB_mode(masked, binary_image):
    mask = np.uint8(binary_image/255)  # 转换为真正的二值
    # 过滤掉背景像素（即值为0的像素）
    pixels = masked[mask > 0]

    # 过滤掉极端值0和255
    # pixels = pixels[(pixels != 0) & (pixels != 255)]

    # 计算每个通道的众数
    b_mode = np.argmax(np.bincount(pixels[:, 0].flatten()))
    g_mode = np.argmax(np.bincount(pixels[:, 1].flatten()))
    r_mode = np.argmax(np.bincount(pixels[:, 2].flatten()))
    color_list = [r_mode, g_mode, b_mode]
    color = "{:02}{:02}{:02}".format(r_mode, g_mode, b_mode)
    return [color, color_list]

def rgb_to_hsv_lab(rgb):
    # 将RGB值标准化到0到1的范围
    r, g, b = [x / 255.0 for x in rgb]

    # 使用colorsys库将RGB转换为HSV
    hsv = colorsys.rgb_to_hsv(r, g, b)
    # 将HSV值中的色相（H）转换为0-360度范围
    hsv_output = (hsv[0] * 360, hsv[1], hsv[2])

    # 将RGB值转换为Lab颜色空间
    # 需要将RGB值扩展为三维数组，因为skimage函数期望输入是(height, width, 3)形状
    rgb_array = np.array([[[r, g, b]]])
    lab_output = color.rgb2lab(rgb_array)
    # 提取Lab值，并去掉数组的多余维度
    lab_output = tuple(lab_output[0, 0, :])

    return hsv_output, lab_output

def save_csv(data, mean_rgb, mode_rgb, glossiness, gdglcm_feature, filename):
    tran_rate = 18.8 / 170
    widths = data[:, 2] * tran_rate
    lengths = data[:, 3] * tran_rate
    areas = data[:, 4] * tran_rate * tran_rate
    # 创建一个字典，其中包含您的数据
    pheno = {
        "籽粒编号": list(range(1, 101)),
        "长度(mm)": lengths,
        "宽度(mm)": widths,
        "投影面积(mm^2)": areas
    }
    rgb_dict = {
        "平均RGB值": mean_rgb,
        "主要RGB值": mode_rgb,
        "光泽度": glossiness,
        "对比度": gdglcm_feature[0],
        "不相似度": gdglcm_feature[1],
        "同质性": gdglcm_feature[2],
        "能量": gdglcm_feature[3],
        "相关性": gdglcm_feature[4],
        "角二阶矩": gdglcm_feature[5],
        "纹理复杂度": gdglcm_feature[6]
                }
    # 创建一个DataFrame
    pheno_df = pd.DataFrame(pheno)
    color_df = pd.DataFrame(rgb_dict)

    # 将DataFrame保存到CSV文件
    # print(f"将数据保存至{filename}")
    pheno_df.to_csv(filename + "_pheno.csv", index=False)
    color_df.to_csv(filename + "_color.csv", index=False)


def colorImage(color):
    # 设置图像的大小
    width, height = 200, 200

    # 创建一个全1的数组，形状为(高度, 宽度, 3通道)
    # 数组的类型设置为uint8，因为图像的像素值通常在这个范围内
    image_array = np.ones((height, width, 3), dtype=np.uint8)

    # 将颜色值乘以数组，以设置每个像素的颜色
    color_uint8 = np.array([color[2], color[1], color[0]], dtype=np.uint8)
    # 注意：如果color元组中的值超过255，则需要对其进行缩放或剪辑
    image_array *= color_uint8
    return image_array


def show2images(img1: np.ndarray, img2: np.ndarray, title1='image1', title2='image2'):
    set_chinese()
    # 创建一个图形和子图
    fig, axs = plt.subplots(1, 2, figsize=(15, 15))
    axs = axs.flatten()
    # 在子图上显示图片
    image_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    axs[0].imshow(image_pil, cmap='gray', vmin=0, vmax=255)
    axs[0].axis('off')  # 不显示坐标轴
    axs[0].set_title(title1)  # 设置标题
    # 在子图上显示图片
    image_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    axs[1].imshow(image_pil, cmap='gray', vmin=0, vmax=255)
    axs[1].axis('off')  # 不显示坐标轴
    axs[1].set_title(title2)  # 设置标题

    # 调整子图间距
    plt.tight_layout()

    # 显示图形
    plt.show()

def save2images(img1: np.ndarray, img2: np.ndarray,photo_path, title1='image1', title2='image2', name='temp'):
    set_chinese()
    # 创建一个图形和子图
    fig, axs = plt.subplots(1, 2, figsize=(15, 15))
    axs = axs.flatten()
    # 在子图上显示图片
    image_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    axs[0].imshow(image_pil, cmap='gray', vmin=0, vmax=255)
    axs[0].axis('off')  # 不显示坐标轴
    axs[0].set_title(title1)  # 设置标题
    # 在子图上显示图片
    image_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    axs[1].imshow(image_pil, cmap='gray', vmin=0, vmax=255)
    axs[1].axis('off')  # 不显示坐标轴
    axs[1].set_title(title2)  # 设置标题

    # 调整子图间距
    plt.tight_layout()

    plt.savefig(os.path.join(photo_path, name + '.svg'))
    # 显示图形
    plt.show()

def mor_open(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def subctract_mask(grayimg, mask):
    shape = mask.shape
    temp = np.zeros(shape)

    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            if mask[i, j] > 0:
                temp[i, j] = 0
            else:
                temp[i, j] = grayimg[i, j]
    return np.uint8(temp)


# 计算灰度差值共生矩阵
def get_gdglcm_feature(img):
    # 转换为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 计算灰度差值共生矩阵
    gdglcm = graycomatrix(gray, [1], [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4], levels=256, symmetric=True,
                          normed=True)
    # 计算统计量特征
    contrast = graycoprops(gdglcm, 'contrast').mean() / 256 / 256
    dissimilarity = graycoprops(gdglcm, 'dissimilarity').mean() / 256
    homogeneity = graycoprops(gdglcm, 'homogeneity').mean()
    energy = graycoprops(gdglcm, 'energy').mean()
    correlation = graycoprops(gdglcm, 'correlation').mean()
    asm = graycoprops(gdglcm, 'ASM').mean()
    texture_complexity = ( contrast + 1 - homogeneity + energy + asm) / 4
    # 返回特征向量
    return [contrast, dissimilarity, homogeneity, correlation, asm, energy, texture_complexity]

def get_glossiness(masked):
    gray = Image.fromarray(masked).convert('L')  # 转换为灰度图像
    window_size = 10
    var = np.array(gray).astype(float)
    mean = cv2.blur(var, (window_size, window_size))
    sqr_mean = cv2.blur(var ** 2, (window_size, window_size))
    var = sqr_mean - mean ** 2
    var = var[var > 0]
    if len(var) == 0:
        mean_var = 0
        max_var = 0
    else:
        mean_var = np.mean(var)
        max_var = np.percentile(var, 95)
    if max_var == 0:
        glossiness = 0
    else:
        glossiness = 1 - np.sqrt(mean_var / max_var)
    return glossiness


'''
先是preprocess
之后getbino
最后提取表型
'''
class phenoExtractor:
    def __init__(self):
        self.seed_type = 0  # 0为水稻，1为大豆
        self.img = None  # 左图

    def preprocess(self):
        self.img = get_Mfilted(self.img)
        self.gray_img = get_Mfilted(self.gray_img)
        if self.seed_type == 0:  # 消除镜面反射
            self.gray_img = self.remove_reflection()

    def remove_reflection(self):
        bch = get_rgb(self.img)[2]
        binary = cv2.threshold(bch, 70, 255, cv2.THRESH_BINARY)[1]
        mask = mor_open(binary)

        result = subctract_mask(self.gray_img, mask)
        return result

    def get_binary(self):
        bimg = get_Mfilted(self.gray_img)
        thresholds = [130, 50]  # 小麦和大豆的参数不同，阈值大的是水稻
        r_img = get_thresh(bimg, threshold=thresholds[self.seed_type])  # 二值化
        r_img = morphological_processing(r_img)
        return r_img

    def phenoext(self, binary):
        stats = get_stats(binary)[1:]
        mor_img = binary.copy()
        masked, sum_pixels = get_mask(self.img, mor_img)
        mean_rgb = get_RGB(masked, sum_pixels)
        mean_hsv, mean_Lab = rgb_to_hsv_lab(mean_rgb[1])
        mode_rgb = get_RGB_mode(masked, mor_img)
        mode_hsv, mode_Lab = rgb_to_hsv_lab(mode_rgb[1])
        result_img = draw_rectangle_with_label(self.img, stats)
        # 计算光泽度
        glossiness = get_glossiness(masked)
        # 纹理复杂度计算
        gdglcm_feature = get_gdglcm_feature(masked)  # 计算GDGLCM特征

        statics = [stats, mean_rgb, mean_hsv, mean_Lab, mode_rgb, mode_hsv, mode_Lab, glossiness, gdglcm_feature]
        return result_img,statics

    def forward(self):
        self.gray_img = get_gray(self.img)
        self.preprocess()
        binary = self.get_binary()
        result = self.phenoext(binary)
        return result

