import pandas as pd
import os
import sys
import numpy as np

class phenoDatum:
    def __init__(self):
        self.type = None  # 0为二维，1为三维

    def update(self, result):
        if self.type == 0:  # 二维表型
            self.avg_weight = result[0]
            stats = result[1][0]
            # 换算
            tran_rate = 18.8 / 170
            self.widths = stats[:, 2] * tran_rate
            self.lengths = stats[:, 3] * tran_rate
            self.areas = stats[:, 4] * tran_rate * tran_rate

            self.mean_rgb = result[1][1]
            self.mean_hsv = result[1][2]
            self.mean_Lab = result[1][3]
            self.mode_rgb = result[1][4]
            self.mode_hsv = result[1][5]
            self.mode_Lab = result[1][6]
            self.glossiness = result[1][7]
            self.gdglcm_feature = result[1][8]
            self.mean_length = round(np.mean(self.lengths), 3)
            self.mean_width = round(np.mean(self.widths), 3)
            self.mean_area = round(np.mean(self.areas), 3)

        elif self.type == 1: # 三维表型
            self.labels = result[0]
            self.centers = result[1]
            self.lengths = result[2]
            self.widths = result[3]
            self.depths = result[4]
            self.volumes = result[5]
            self.mean_length = round(np.mean(self.lengths), 3)
            self.mean_width = round(np.mean(self.widths), 3)
            self.mean_depth = round(np.mean(self.depths), 3)
            self.mean_vol = round(np.mean(self.volumes), 3)

    def save(self,filename):
        if self.type == 0: # 二维表型
            # 创建一个字典，其中包含您的数据
            detail = {
                "籽粒编号": list(range(1, len(self.lengths)+1)),
                "长度(mm)": self.lengths,
                "宽度(mm)": self.widths,
                "面积(mm^2)": self.areas
            }
            pheno_dict = {
                "平均长度(mm)": self.mean_length,
                "平均宽度(mm)": self.mean_width,
                "平均面积(mm^2)": self.mean_area,
                "平均RGB值": self.mean_rgb[0],
                "主要RGB值": self.mode_rgb[0],
                "光泽度": self.glossiness,
                "对比度": self.gdglcm_feature[0],
                "不相似度": self.gdglcm_feature[1],
                "同质性": self.gdglcm_feature[2],
                "能量": self.gdglcm_feature[3],
                "相关性": self.gdglcm_feature[4],
                "角二阶矩": self.gdglcm_feature[5],
                "纹理复杂度": self.gdglcm_feature[6]
            }
            # 创建一个DataFrame
            detail_df = pd.DataFrame(detail)
            pheno_df = pd.DataFrame(pheno_dict, index=[0])
        elif self.type == 1:
            detail = {
                "籽粒编号": list(range(1,self.labels+1)),
                "籽粒中心坐标": self.centers,
                "籽粒长度(mm)": self.lengths,
                "籽粒宽度(mm)": self.widths,
                "籽粒厚度(mm)": self.depths,
                "籽粒体积(mm^3)": self.volumes
            }

            pheno_dict = {
                "籽粒平均长度(mm)": self.mean_length,
                "籽粒平均宽度(mm)": self.mean_width,
                "籽粒平均厚度(mm)": self.mean_depth,
                "籽粒平均体积(mm^3)": self.mean_vol
            }
            # 创建一个DataFrame
            detail_df = pd.DataFrame(detail)
            pheno_df = pd.DataFrame(pheno_dict, index=[0])

        # 将DataFrame保存到CSV文件
        detail_df.to_csv(filename + "_detail.csv", index=False)
        pheno_df.to_csv(filename + "_pheno.csv", index=False)
        print(f"saved data to {filename}")
