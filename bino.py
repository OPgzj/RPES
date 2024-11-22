# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bino.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTimer, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QWidget,QFileDialog, QMessageBox)

import cv2
import os
import binoCamera
import PhenoEx
import PCprocess
from Modbus import ScaleModbusRTU

class bino_Form(QWidget):
    def __init__(self, window_type=1, L_img=None, R_img=None ):
        super().__init__()
        self.L_img = L_img
        self.R_img = R_img
        self.window_type = window_type
        self.setupUi(self)


    def setupUi(self, Qwidget):
        # if not parent.objectName():
        #     parent.setObjectName(u"Form")
        Qwidget.setObjectName(u"Form")
        Qwidget.resize(1275, 640)
        self.L_Win = QLabel(Qwidget)
        self.L_Win.setObjectName(u"L_Win")
        self.L_Win.setGeometry(QRect(10, 10, 612, 512))
        self.R_Win = QLabel(Qwidget)
        self.R_Win.setObjectName(u"R_Win")
        self.R_Win.setGeometry(QRect(640, 10, 612, 512))

        if self.window_type == 1:  # 双目图像
            self.pushButton = QPushButton(Qwidget)
            self.pushButton.setObjectName(u"pushButton")
            self.pushButton.setGeometry(QRect(160, 560, 75, 24))
            self.pushButton.clicked.connect(self.on_preprocess_clicked)
            self.pushButton_2 = QPushButton(Qwidget)
            self.pushButton_2.setObjectName(u"pushButton_2")
            self.pushButton_2.setGeometry(QRect(560, 560, 120, 24))
            self.pushButton_2.clicked.connect(self.on_disdep_clicked)
            self.pushButton_3 = QPushButton(Qwidget)
            self.pushButton_3.setObjectName(u"pushButton_3")
            self.pushButton_3.setGeometry(QRect(930, 560, 120, 24))
            self.pushButton_3.clicked.connect(self.on_genpc_clicked)
            # 显示图像
            self.show_binoimg()

        elif self.window_type == 2:  # 双目相机
            self.pushButton= QPushButton(Qwidget)
            self.pushButton.setObjectName(u"pushButton_2")
            self.pushButton.setGeometry(QRect(560, 560, 75, 24))
            self.pushButton.clicked.connect(self.save_image)
            self.timer_camera = QTimer()  # 定时器
            self.timer_camera.timeout.connect(self.show_binocamera)
            self.open_binocamera()  # 打开相机
            self.scale = ScaleModbusRTU(port='COM6', baudrate=9600, timeout=1)

        elif self.window_type == 3:  # 二维大豆表型提取
            self.pushButton = QPushButton(Qwidget)
            self.pushButton.setObjectName(u"pushButton")
            self.pushButton.setGeometry(QRect(160, 560, 75, 24))
            self.pushButton.clicked.connect(self.on_preprocess_clicked)
            self.pushButton_2 = QPushButton(Qwidget)
            self.pushButton_2.setObjectName(u"pushButton_2")
            self.pushButton_2.setGeometry(QRect(560, 560, 120, 24))
            self.pushButton_2.clicked.connect(self.on_getbino_clicked)
            self.pushButton_3 = QPushButton(Qwidget)
            self.pushButton_3.setObjectName(u"pushButton_3")
            self.pushButton_3.setGeometry(QRect(930, 560, 120, 24))
            self.pushButton_3.clicked.connect(self.on_soyphenoext_clicked)

            self.R_img = PhenoEx.get_gray(self.L_img)
            self.show_binoimg()

        elif self.window_type == 4:  # 二维水稻表型提取
            self.pushButton = QPushButton(Qwidget)
            self.pushButton.setObjectName(u"pushButton")
            self.pushButton.setGeometry(QRect(160, 560, 75, 24))
            self.pushButton.clicked.connect(self.on_preprocess_clicked)
            self.pushButton_2 = QPushButton(Qwidget)
            self.pushButton_2.setObjectName(u"pushButton_2")
            self.pushButton_2.setGeometry(QRect(560, 560, 120, 24))
            self.pushButton_2.clicked.connect(self.on_getbino_clicked)
            self.pushButton_3 = QPushButton(Qwidget)
            self.pushButton_3.setObjectName(u"pushButton_3")
            self.pushButton_3.setGeometry(QRect(930, 560, 120, 24))
            self.pushButton_3.clicked.connect(self.on_phenoext_clicked)

            self.R_img = PhenoEx.get_gray(self.L_img)
            self.show_binoimg()


        self.retranslateUi(Qwidget)

        QMetaObject.connectSlotsByName(Qwidget)
    # setupUi

    def retranslateUi(self, Qwidget):
        if self.window_type == 1:
            Qwidget.setWindowTitle(QCoreApplication.translate("Form", u"双目图像", None))
            self.pushButton.setText(QCoreApplication.translate("Form", u"预处理", None))
            self.pushButton_2.setText(QCoreApplication.translate("Form", u"生成视差图\深度图", None))
            self.pushButton_3.setText(QCoreApplication.translate("Form", u"三维重建生成点云", None))
        elif self.window_type == 2:
            Qwidget.setWindowTitle(QCoreApplication.translate("Form", u"双目相机", None))
            self.pushButton.setText(QCoreApplication.translate("Form", u"拍照", None))
        elif self.window_type == 3:
            Qwidget.setWindowTitle(QCoreApplication.translate("Form", u"二维大豆表型提取", None))
            self.pushButton.setText(QCoreApplication.translate("Form", u"预处理", None))
            self.pushButton_2.setText(QCoreApplication.translate("Form", u"生成二值图", None))
            self.pushButton_3.setText(QCoreApplication.translate("Form", u"二维表型提取", None))
        elif self.window_type == 4:
            Qwidget.setWindowTitle(QCoreApplication.translate("Form", u"二维水稻表型提取", None))
            self.pushButton.setText(QCoreApplication.translate("Form", u"预处理", None))
            self.pushButton_2.setText(QCoreApplication.translate("Form", u"生成二值图", None))
            self.pushButton_3.setText(QCoreApplication.translate("Form", u"二维表型提取", None))
    # retranslateUi

    def cv2_to_qt(self, cv2_img):
        # 先变换尺寸
        cv2_img = cv2.resize(cv2_img, (612, 512))
        # 转换颜色空间 BGR (OpenCV) -> RGB
        cv2_img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        # 将图像转换为 QImage
        height, width, channels = cv2_img_rgb.shape
        bytes_per_line = channels * width
        QImage_format = QImage.Format_RGB888
        return QImage(cv2_img_rgb.data, width, height, bytes_per_line, QImage_format)

    def show_binoimg(self):
        L_img_qt = self.cv2_to_qt(self.L_img)
        R_img_qt = self.cv2_to_qt(self.R_img)
        self.L_Win.setPixmap(QPixmap.fromImage(L_img_qt))
        self.R_Win.setPixmap(QPixmap.fromImage(R_img_qt))

    def on_preprocess_clicked(self):
        tempL = PhenoEx.get_Mfilted(self.L_img)
        tempR = PhenoEx.get_Mfilted(self.R_img)
        if self.window_type == 1:  # 双目图像校正
            self.L_img, self.R_img, self.Q = PCprocess.undistortion(tempL, tempR)
        elif self.window_type == 4:
            self.L_img, self.R_img = tempL, tempR
            reply = QMessageBox.information(None, "info", f"是否去除镜面反射？",
                                            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Ok:
                self.remove_reflection()
        QMessageBox.information(None, "info", f"完成预处理")
        self.show_binoimg()


    def on_disdep_clicked(self):
        self.dis, dis_color = PCprocess.get_disparity(self.L_img, self.R_img)
        self.R_img = dis_color
        self.show_binoimg()

    def on_genpc_clicked(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PointClouds Files (*.ply);;All Files (*)")
        if file_path:
            # 拆分文件名以获取路径和单纯的文件名
            file_name, _ = os.path.splitext(file_path)
            QMessageBox.information(None, "info", f"保存至{file_name}")
            # print(f"Selected file: ")
            PCprocess.get_pointclouds(self.dis, self.Q, self.L_img, file_name)


    def remove_reflection(self):
        bch = PhenoEx.get_rgb(self.L_img)[2]
        binary = cv2.threshold(bch, 70, 255, cv2.THRESH_BINARY)[1]
        mask = PhenoEx.mor_open(binary)

        result = PhenoEx.subctract_mask(self.R_img, mask)

        self.R_img = result
        self.show_binoimg()

    def on_getbino_clicked(self):
        bimg = PhenoEx.get_Mfilted(self.R_img)
        thresholds = [50, 130]  # 小麦和大豆的参数不同
        self.R_img = PhenoEx.get_thresh(bimg, threshold=thresholds[self.window_type-3])  # 二值化
        QMessageBox.information(None, "info", f"完成二值化")
        # if self.window_type == 4:
        self.R_img = PhenoEx.morphological_processing(self.R_img)
        QMessageBox.information(None, "info", f"完成形态学处理")
        # print("完成形态学处理")
        self.show_binoimg()

    def on_phenoext_clicked(self):
        stats = PhenoEx.get_stats(self.R_img)[1:]
        mor_img = self.R_img.copy()
        masked, sum_pixels = PhenoEx.get_mask(self.L_img, mor_img)
        mean_rgb = PhenoEx.get_RGB(masked, sum_pixels)
        mode_rgb = PhenoEx.get_RGB_mode(masked, mor_img)
        meanimg = PhenoEx.colorImage(mean_rgb)
        modeimg = PhenoEx.colorImage(mode_rgb)
        self.R_img = PhenoEx.draw_rectangle_with_label(self.L_img, stats)
        self.show_binoimg()
        # 计算光泽度
        glossiness = PhenoEx.get_glossiness(masked)
        # 纹理复杂度计算
        gdglcm_feature = PhenoEx.get_gdglcm_feature(masked)  # 计算GDGLCM特征
        PhenoEx.show2images(meanimg, modeimg, '平均rgb', '众数rgb')
        reply =QMessageBox.information(None, "info", f"完成二维表型提取，是否导出？", QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        # 检查用户是否点击了"确定"按钮
        if reply == QMessageBox.Ok:
            # 执行后续内容
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Image Files (*.jpg);;All Files (*)")
            if file_path:
                # print(f"Selected file: {file_path}")
                # 拆分文件名以获取路径和单纯的文件名
                file_name, _ = os.path.splitext(file_path)
                PhenoEx.save_csv(stats, mean_rgb, mode_rgb, glossiness, gdglcm_feature, file_name)
                self.take_photo(self.R_img, file_path)
                QMessageBox.information(None, "info", f"将数据保存至{file_name}")

    def on_soyphenoext_clicked(self):
        stats = PhenoEx.get_stats(self.R_img)[1:]
        mor_img = self.R_img.copy()
        masked, sum_pixels = PhenoEx.get_mask(self.L_img, mor_img)
        mean_rgb = PhenoEx.get_RGB(masked, sum_pixels)
        mode_rgb = PhenoEx.get_RGB_mode(masked, mor_img)
        meanimg = PhenoEx.colorImage(mean_rgb)
        modeimg = PhenoEx.colorImage(mode_rgb)
        self.R_img = PhenoEx.draw_rectangle_with_label(self.L_img, stats)
        self.show_binoimg()
        # 计算光泽度
        glossiness = PhenoEx.get_glossiness(masked)
        # 纹理复杂度计算
        gdglcm_feature = PhenoEx.get_gdglcm_feature(masked) # 计算GDGLCM特征
        # 显示颜色
        PhenoEx.show2images(meanimg, modeimg, '平均rgb', '众数rgb')
        reply =QMessageBox.information(None, "info", f"完成二维表型提取，是否导出？", QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        # 检查用户是否点击了"确定"按钮
        if reply == QMessageBox.Ok:
            # 执行后续内容
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Image Files (*.jpg);;All Files (*)")
            if file_path:
                # print(f"Selected file: {file_path}")
                # 拆分文件名以获取路径和单纯的文件名
                file_name, _ = os.path.splitext(file_path)
                PhenoEx.save_csv(stats, mean_rgb, mode_rgb, glossiness, gdglcm_feature, file_name)
                self.take_photo(self.R_img, file_path)
                QMessageBox.information(None, "info", f"将数据保存至{file_name}")

    def open_binocamera(self):
        self.cameraL = binoCamera.StereoCamera()
        self.cameraR = binoCamera.StereoCamera()
        self.cameraL.open_camera(self.cameraL.leftindex)
        self.cameraR.open_camera(self.cameraR.rightindex)
        self.timer_camera.start(30)

    def show_binocamera(self):
        self.L_img = self.cameraL.get_fream()
        self.R_img = self.cameraR.get_fream()
        self.show_binoimg()

    def save_image(self):
        weight = self.scale.get_weight()
        QMessageBox.information(None, "重量", f"{weight}g")
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Image Files (*.jpg);;All Files (*)")
        if file_path:
            # print(f"Selected file: {file_path}")
            # 拆分文件名以获取路径和单纯的文件名
            file_name, _ = os.path.splitext(file_path)
            newfn_L = file_name + '_L.jpg'
            newfn_R = file_name + '_R.jpg'
            image_left = self.cameraL.get_fream()
            image_right = self.cameraR.get_fream()
            self.take_photo(image_left, newfn_L)
            self.take_photo(image_right, newfn_R)

    def take_photo(self, frame, filename):
        cv2.imwrite(filename, frame)
        QMessageBox.information(None, "info", f"照片已保存为 {filename}")
        # print(f"照片已保存为 {filename}")

    def closeEvent(self, event):
        if self.window_type == 2:
            # print("关闭双目相机")
            QMessageBox.information(None, "info", f"已关闭双目相机")
            # 停止定时器
            self.timer_camera.stop()
            # 释放摄像头资源
            self.cameraL.camera_close()
            self.cameraR.camera_close()



