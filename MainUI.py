# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainUI.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import numpy as np
from PySide6.QtCore import (QCoreApplication, QTimer,QMetaObject, QRect,
    QSize)
from PySide6.QtGui import (QIcon,QImage,  QPixmap)
from PySide6.QtWidgets import (QApplication, QFrame, QRadioButton, QGroupBox,
    QLabel, QMainWindow, QMenuBar, QProgressBar,QButtonGroup,
    QPushButton, QSizePolicy, QStatusBar, QTabWidget, QFileDialog,QMessageBox,
    QWidget)
import sys
import yolo_main as yolo
import binoCamera
import cv2
from Modbus import ScaleModbusRTU
import open3d as o3d
import os
from binoCamera import binoCamera
from PhenoEx import phenoExtractor
from phenoData import phenoDatum
from PCprocess import PointCloudProcess
import Exceptions

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(960, 660)
        MainWindow.setMinimumSize(QSize(960, 660))
        MainWindow.setMaximumSize(QSize(960, 660))
        MainWindow.setStyleSheet(u"QMainWindow{\n"
"	background-color:rgb(240, 240, 240);\n"
"	color:#2e2e2e;\n"
"}\n"
"\n"
"QWidget{\n"
"	background-color:rgb(240, 240, 240);\n"
"	font: 10pt \"Microsoft YaHei UI\";\n"
"}\n"
"QPushButton{	background-color:#e8df98;}\n"
"\n"
"QFrame{\n"
"background-color:rgb(250, 250, 250);\n"
"}\n"
"\n"
"QTabWidget::pane{	border: none;}\n"
"\n"
"QTabBar::tab{\n"
"	background-color:rgb(240, 240, 240);\n"
"	font-weight: bold;\n"
"}\n"
"\n"
"QLabel{background:transparent;}\n"
"\n"                          
"QRadioButton{background:transparent;}\n"
"\n"
"QTabBar::tab:selected{\n"
"	background-color:rgb(250, 250, 250);\n"
"	font-weight: bold;\n"
"}\n"
"QGroupBox {\n"
"    \n"
"    margin-left: 10px; /* \u4e3a\u6807\u9898\u7559\u51fa\u7a7a\u95f4 */\n"
"	margin-top:20px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left; /* \u6807\u9898\u4f4d\u7f6e\u5728\u5de6\u4e0a\u89d2 */\n"
"    left: 0px; /* \u5c06\u6807\u9898\u79fb\u51fa\u6846\u5916 */\n"
"    margin-left: 8px; /* \u6807\u9898\u4e0e\u6846\u4e4b\u95f4\u7684\u8ddd\u79bb */\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.MaintabWidget = QTabWidget(self.centralwidget)
        self.MaintabWidget.setObjectName(u"MaintabWidget")
        self.MaintabWidget.setGeometry(QRect(0, 0, 960, 620))
        self.MaintabWidget.setMinimumSize(QSize(960, 620))
        self.MaintabWidget.setMaximumSize(QSize(960, 620))
        self.MaintabWidget.setStyleSheet(u"")
        self.MaintabWidget.setTabShape(QTabWidget.Rounded)
        self.twoDim = QWidget()
        self.twoDim.setObjectName(u"twoDim")
        self.SubtabWidget_1 = QTabWidget(self.twoDim)
        self.SubtabWidget_1.setObjectName(u"SubtabWidget_1")
        self.SubtabWidget_1.setGeometry(QRect(0, 0, 431, 71))
        self.SubtabWidget_1.setTabShape(QTabWidget.Rounded)
        self.binoImg = QWidget()
        self.binoImg.setObjectName(u"binoImg")
        self.SelectImage = QPushButton(self.binoImg)
        self.SelectImage.setObjectName(u"SelectImage")
        self.SelectImage.setGeometry(QRect(20, 10, 70, 25))
        self.SubtabWidget_1.addTab(self.binoImg, "")
        self.binocamera = QWidget()
        self.binocamera.setObjectName(u"binocamera")
        self.cam2Exp = QLabel(self.binocamera)
        self.cam2Exp.setObjectName(u"cam2Exp")
        self.cam2Exp.setGeometry(QRect(110, 15, 54, 20))
        self.cam1Exp = QLabel(self.binocamera)
        self.cam1Exp.setObjectName(u"cam1Exp")
        self.cam1Exp.setGeometry(QRect(20, 15, 51, 20))
        self.cam2Status = QLabel(self.binocamera)
        self.cam2Status.setObjectName(u"cam2Status")
        self.cam2Status.setGeometry(QRect(170, 17, 15, 15))
        self.cam2Status.setMinimumSize(QSize(15, 15))
        self.cam2Status.setMaximumSize(QSize(15, 15))
        self.camCnt = QPushButton(self.binocamera)
        self.camCnt.setObjectName(u"camCnt")
        self.camCnt.setGeometry(QRect(200, 10, 90, 25))
        self.cam1Status = QLabel(self.binocamera)
        self.cam1Status.setObjectName(u"cam1Status")
        self.cam1Status.setGeometry(QRect(80, 17, 15, 15))
        self.SubtabWidget_1.addTab(self.binocamera, "")
        self.SubtabWidget_1.currentChanged.connect(self.on_subtw1_change)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cam1Status.sizePolicy().hasHeightForWidth())
        self.cam1Status.setSizePolicy(sizePolicy)
        self.cam1Status.setMinimumSize(QSize(15, 15))
        self.cam1Status.setMaximumSize(QSize(15, 15))
        self.TakeImages = QPushButton(self.binocamera)
        self.TakeImages.setObjectName(u"TakeImages")
        self.TakeImages.setGeometry(QRect(320, 10, 70, 25))
        self.ViewL = QLabel(self.twoDim)
        self.ViewL.setObjectName(u"ViewL")
        self.ViewL.setGeometry(QRect(20, 70, 306, 256))
        self.ViewR = QLabel(self.twoDim)
        self.ViewR.setObjectName(u"ViewR")
        self.ViewR.setGeometry(QRect(330, 70, 306, 256))
        self.frame_2 = QFrame(self.twoDim)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(720, 70, 160, 256))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        # 添加两个radiobutton
        self.scltWheat = QRadioButton(self.frame_2)
        self.scltWheat.setText("水稻")
        self.scltWheat.setGeometry(QRect(30, 10, 50, 20))
        self.scltBean = QRadioButton(self.frame_2)
        self.scltBean.setText("大豆")
        self.scltBean.setGeometry(QRect(30, 40, 50, 20))
        # 创建一个按钮组并将单选按钮添加到该组中
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.scltWheat)
        self.buttonGroup.addButton(self.scltBean)
        # 设置按钮组的互斥性
        self.buttonGroup.setExclusive(True)
        # 默认选中第一个单选按钮
        self.scltWheat.setChecked(True)

        self.scaleZero = QPushButton(self.frame_2)
        self.scaleZero.setObjectName(u"scaleZero")
        self.scaleZero.setGeometry(QRect(30, 80, 90, 25))
        self.CrackDetect = QPushButton(self.frame_2)
        self.CrackDetect.setObjectName(u"CrackDetect")
        self.CrackDetect.setGeometry(QRect(30, 120, 90, 25))
        self.Extraction = QPushButton(self.frame_2)
        self.Extraction.setObjectName(u"Extraction")
        self.Extraction.setGeometry(QRect(30, 160, 90, 25))
        self.SaveData = QPushButton(self.frame_2)
        self.SaveData.setObjectName(u"SaveData")
        self.SaveData.setGeometry(QRect(30, 200, 90, 25))
        self.frame_3 = QFrame(self.twoDim)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(30, 360, 920, 200))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gb_pheno = QGroupBox(self.frame_3)
        self.gb_pheno.setObjectName(u"groupBox")
        self.gb_pheno.setGeometry(QRect(0, 40, 180, 120))
        self.gb_pheno.setStyleSheet(u"")
        self.gb_color = QGroupBox(self.frame_3)
        self.gb_color.setObjectName(u"groupBox")
        self.gb_color.setGeometry(QRect(180, 40, 430, 120))
        self.gb_color.setStyleSheet(u"")
        self.gb_txtre = QGroupBox(self.frame_3)
        self.gb_txtre.setObjectName(u"groupBox")
        self.gb_txtre.setGeometry(QRect(610, 40, 300, 120))
        self.gb_txtre.setStyleSheet(u"")
        self.lb_length = QLabel(self.gb_pheno)
        self.lb_length.setObjectName(u"lb_length")
        self.lb_length.setGeometry(QRect(20, 30, 70, 20))
        self.lb_width = QLabel(self.gb_pheno)
        self.lb_width.setObjectName(u"lb_width")
        self.lb_width.setGeometry(QRect(20, 60, 70, 20))
        self.length = QLabel(self.gb_pheno)
        self.length.setObjectName(u"length")
        self.length.setGeometry(QRect(100, 30, 40, 20))
        self.width = QLabel(self.gb_pheno)
        self.width.setObjectName(u"width")
        self.width.setGeometry(QRect(100, 60, 40, 20))
        self.lb_area = QLabel(self.gb_pheno)
        self.lb_area.setObjectName(u"label_6")
        self.lb_area.setGeometry(QRect(20, 90, 95, 20))
        self.area = QLabel(self.gb_pheno)
        self.area.setObjectName(u"area")
        self.area.setGeometry(QRect(120, 90, 50, 20))

        self.lb_avgRGB = QLabel(self.gb_color)
        self.lb_avgRGB.setStyleSheet("font-weight:bold")
        self.lb_avgRGB.setObjectName(u"label_8")
        self.lb_avgRGB.setGeometry(QRect(20, 20, 55, 20))
        self.lb_mRGB = QLabel(self.gb_color)
        self.lb_mRGB.setStyleSheet("font-weight:bold")
        self.lb_mRGB.setObjectName(u"label_9")
        self.lb_mRGB.setGeometry(QRect(20, 70, 55, 20))
        # 加一堆label
        # self.lb_avgR = QLabel("R:", self.gb_color)
        # self.lb_avgR.setGeometry(QRect(20, 45, 15, 20))
        #
        # self.lb_priR = QLabel("R:", self.gb_color)
        # self.lb_priR.setGeometry(QRect(20, 95, 15, 20))
        #
        # self.avgR = QLabel(self.gb_color)
        # self.avgR.setGeometry(QRect(35, 45, 70, 20))
        # self.priR = QLabel(self.gb_color)
        # self.priR.setGeometry(QRect(35, 95, 70, 20))

        # 定义Y坐标的起始位置
        y_avg = 45
        y_pri = 95
        start_label = 20  # 标签的水平偏移
        start_value = 35  # 值的水平偏移
        height_label = 20  # 标签的高度
        width_label = 15  # 标签的宽度
        width_value = 70  # 值的宽度
        vertical_spacing = 42  # 两个颜色组之间的垂直间距
        offset = 10  # 组与组之间的间距

        # R, G, B labels
        self.lb_avgR = QLabel("R:", self.gb_color)
        self.lb_avgR.setGeometry(QRect(start_label, y_avg, width_label, height_label))
        self.lb_avgG = QLabel("G:", self.gb_color)
        self.lb_avgG.setGeometry(QRect(start_label + vertical_spacing, y_avg, width_label, height_label))
        self.lb_avgB = QLabel("B:", self.gb_color)
        self.lb_avgB.setGeometry(QRect(start_label + 2 * vertical_spacing, y_avg, width_label, height_label))

        self.lb_priR = QLabel("R:", self.gb_color)
        self.lb_priR.setGeometry(QRect(start_label, y_pri, width_label, height_label))
        self.lb_priG = QLabel("G:", self.gb_color)
        self.lb_priG.setGeometry(QRect(start_label + vertical_spacing, y_pri, width_label, height_label))
        self.lb_priB = QLabel("B:", self.gb_color)
        self.lb_priB.setGeometry(QRect(start_label + 2 * vertical_spacing, y_pri, width_label, height_label))

        self.avgR = QLabel("null", self.gb_color)
        self.avgR.setGeometry(QRect(start_value, y_avg, width_value, height_label))
        self.avgG = QLabel("null", self.gb_color)
        self.avgG.setGeometry(QRect(start_value + vertical_spacing, y_avg, width_value, height_label))
        self.avgB = QLabel("null", self.gb_color)
        self.avgB.setGeometry(QRect(start_value + 2 * vertical_spacing, y_avg, width_value, height_label))

        self.priR = QLabel("null", self.gb_color)
        self.priR.setGeometry(QRect(start_value, y_pri, width_value, height_label))
        self.priG = QLabel("null", self.gb_color)
        self.priG.setGeometry(QRect(start_value + vertical_spacing, y_pri, width_value, height_label))
        self.priB = QLabel("null", self.gb_color)
        self.priB.setGeometry(QRect(start_value + 2 * vertical_spacing, y_pri, width_value, height_label))
        # HSV labels
        self.lb_avgH = QLabel("H:", self.gb_color)
        self.lb_avgH.setGeometry(QRect(start_label + offset + 3 * vertical_spacing, y_avg, width_label, height_label))
        self.lb_avgS = QLabel("S:", self.gb_color)
        self.lb_avgS.setGeometry(QRect(start_label + offset + 4 * vertical_spacing, y_avg, width_label, height_label))
        self.lb_avgV = QLabel("V:", self.gb_color)
        self.lb_avgV.setGeometry(QRect(start_label + offset + 5 * vertical_spacing, y_avg, width_label, height_label))

        self.lb_priH = QLabel("H:", self.gb_color)
        self.lb_priH.setGeometry(QRect(start_label + offset + 3 * vertical_spacing, y_pri, width_label, height_label))
        self.lb_priS = QLabel("S:", self.gb_color)
        self.lb_priS.setGeometry(QRect(start_label + offset + 4 * vertical_spacing, y_pri, width_label, height_label))
        self.lb_priV = QLabel("V:", self.gb_color)
        self.lb_priV.setGeometry(QRect(start_label + offset + 5 * vertical_spacing, y_pri, width_label, height_label))

        self.avgH = QLabel("null", self.gb_color)
        self.avgH.setGeometry(QRect(start_value + offset + 3 * vertical_spacing, y_avg, width_value, height_label))
        self.avgS = QLabel("null", self.gb_color)
        self.avgS.setGeometry(QRect(start_value + offset + 4 * vertical_spacing, y_avg, width_value, height_label))
        self.avgV = QLabel("null", self.gb_color)
        self.avgV.setGeometry(QRect(start_value + offset + 5 * vertical_spacing, y_avg, width_value, height_label))

        self.priH = QLabel("null", self.gb_color)
        self.priH.setGeometry(QRect(start_value + offset + 3 * vertical_spacing, y_pri, width_value, height_label))
        self.priS = QLabel("null", self.gb_color)
        self.priS.setGeometry(QRect(start_value + offset + 4 * vertical_spacing, y_pri, width_value, height_label))
        self.priV = QLabel("null", self.gb_color)
        self.priV.setGeometry(QRect(start_value + offset + 5 * vertical_spacing, y_pri, width_value, height_label))

        # Lab labels
        self.lb_avgL = QLabel("L:", self.gb_color)
        self.lb_avgL.setGeometry(QRect(start_label + 2 * offset + 6 * vertical_spacing, y_avg, width_label, height_label))
        self.lb_avga = QLabel("a:", self.gb_color)
        self.lb_avga.setGeometry(QRect(start_label + 2 * offset  + 7 * vertical_spacing, y_avg, width_label, height_label))
        self.lb_avgb = QLabel("b:", self.gb_color)
        self.lb_avgb.setGeometry(QRect(start_label + 2 * offset  + 8 * vertical_spacing, y_avg, width_label, height_label))

        self.lb_priL = QLabel("L:", self.gb_color)
        self.lb_priL.setGeometry(QRect(start_label + 2 * offset + 6 * vertical_spacing, y_pri, width_label, height_label))
        self.lb_pri_a = QLabel("a:", self.gb_color)
        self.lb_pri_a.setGeometry(QRect(start_label + 2 * offset + 7 * vertical_spacing, y_pri, width_label, height_label))
        self.lb_pri_b = QLabel("b:", self.gb_color)
        self.lb_pri_b.setGeometry(QRect(start_label + 2 * offset + 8 * vertical_spacing, y_pri, width_label, height_label))

        self.avgL = QLabel("null", self.gb_color)
        self.avgL.setGeometry(QRect(start_value + 2 * offset + 6 * vertical_spacing, y_avg, width_value, height_label))
        self.avg_a = QLabel("null", self.gb_color)
        self.avg_a.setGeometry(QRect(start_value + 2 * offset + 7 * vertical_spacing, y_avg, width_value, height_label))
        self.avg_b = QLabel("null", self.gb_color)
        self.avg_b.setGeometry(QRect(start_value + 2 * offset + 8 * vertical_spacing, y_avg, width_value, height_label))

        self.priL = QLabel("null", self.gb_color)
        self.priL.setGeometry(QRect(start_value + 2 * offset + 6 * vertical_spacing, y_pri, width_value, height_label))
        self.pri_a = QLabel("null", self.gb_color)
        self.pri_a.setGeometry(QRect(start_value + 2 * offset + 7 * vertical_spacing, y_pri, width_value, height_label))
        self.pri_b = QLabel("null", self.gb_color)
        self.pri_b.setGeometry(QRect(start_value + 2 * offset + 8 * vertical_spacing, y_pri, width_value, height_label))


        self.lb_gloriness = QLabel(self.gb_txtre)
        self.lb_gloriness.setObjectName(u"label_7")
        self.lb_gloriness.setGeometry(QRect(20, 25, 60, 20))
        self.glossiness = QLabel(self.gb_txtre)
        self.glossiness.setObjectName(u"glossiness")
        self.glossiness.setGeometry(QRect(90, 25, 50, 20))

        # 创建显示参数名称的QLabel组件
        self.lb_contrast = QLabel("对比度:", self.gb_txtre)
        self.lb_contrast.setGeometry(QRect(20, 50, 60, 20))
        self.lb_dissimilarity = QLabel("不相似度:", self.gb_txtre)
        self.lb_dissimilarity.setGeometry(QRect(20, 75, 60, 20))
        self.lb_homogeneity = QLabel("同质性:", self.gb_txtre)
        self.lb_homogeneity.setGeometry(QRect(20, 100, 60, 20))

        self.lb_energy = QLabel("能量:", self.gb_txtre)
        self.lb_energy.setGeometry(QRect(160, 25, 60, 20))
        self.lb_correlation = QLabel("相关性:", self.gb_txtre)
        self.lb_correlation.setGeometry(QRect(160, 50, 60, 20))
        self.lb_ASM = QLabel("角二阶矩:", self.gb_txtre)
        self.lb_ASM.setGeometry(QRect(160, 75, 60, 20))
        self.lb_complexity = QLabel("纹理复杂度:", self.gb_txtre)
        self.lb_complexity.setGeometry(QRect(160, 100, 70, 20))

        # 创建显示参数值的QLabel组件
        self.contrast = QLabel("null", self.gb_txtre)
        self.contrast.setGeometry(QRect(90, 50, 50, 20))
        self.dissimilarity = QLabel("null", self.gb_txtre)
        self.dissimilarity.setGeometry(QRect(90, 75, 50, 20))
        self.homogeneity = QLabel("null", self.gb_txtre)
        self.homogeneity.setGeometry(QRect(90, 100, 50, 20))
        self.energy = QLabel("null", self.gb_txtre)
        self.energy.setGeometry(QRect(240, 25, 50, 20))
        self.correlation = QLabel("null", self.gb_txtre)
        self.correlation.setGeometry(QRect(240, 50, 50, 20))
        self.asm = QLabel("null", self.gb_txtre)
        self.asm.setGeometry(QRect(240, 75, 50, 20))
        self.complexity = QLabel("null", self.gb_txtre)
        self.complexity.setGeometry(QRect(240, 100, 50, 20))

        self.scaleNum = QLabel(self.frame_3)
        self.scaleNum.setObjectName(u"scaleNum")
        self.scaleNum.setGeometry(QRect(130, 5, 40, 20))
        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 5, 91, 20))

        self.MaintabWidget.addTab(self.twoDim, "")
        self.threeDim = QWidget()
        self.threeDim.setObjectName(u"threeDim")
        self.subWidget_2 = QTabWidget(self.threeDim)
        self.subWidget_2.setObjectName(u"subWidget_2")
        self.subWidget_2.setGeometry(QRect(0, 0, 960, 620))
        self.subWidget_2.setMinimumSize(QSize(960, 620))
        self.subWidget_2.setMaximumSize(QSize(960, 620))
        self.subWidget_2.setTabShape(QTabWidget.Rounded)
        self.PointCouldGen = QWidget()
        self.PointCouldGen.setObjectName(u"PointCouldGen")
        self.progressBar = QProgressBar(self.PointCouldGen)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(210, 460, 161, 25))
        self.progressBar.setValue(0)
        self.SelectImages = QPushButton(self.PointCouldGen)
        self.SelectImages.setObjectName(u"SelectImages")
        self.SelectImages.setGeometry(QRect(20, 10, 91, 25))
        self.ViewL_1 = QLabel(self.PointCouldGen)
        self.ViewL_1.setObjectName(u"ViewL_1")
        self.ViewL_1.setGeometry(QRect(20, 70, 306, 256))
        self.ViewR_1 = QLabel(self.PointCouldGen)
        self.ViewR_1.setObjectName(u"ViewR_1")
        self.ViewR_1.setGeometry(QRect(330, 70, 306, 256))
        self.GenPC = QPushButton(self.PointCouldGen)
        self.GenPC.setObjectName(u"GenPC")
        self.GenPC.setGeometry(QRect(40, 460, 75, 25))
        self.label_2 = QLabel(self.PointCouldGen)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(140, 460, 60, 25))
        self.SavePC = QPushButton(self.PointCouldGen)
        self.SavePC.setObjectName(u"SavePC")
        self.SavePC.setGeometry(QRect(40, 510, 75, 24))
        self.subWidget_2.addTab(self.PointCouldGen, "")
        self.PointCloudAnalysis = QWidget()
        self.PointCloudAnalysis.setObjectName(u"PointCloudAnalysis")
        self.frame = QFrame(self.PointCloudAnalysis)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(30, 30, 401, 331))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.pointcloudname = QLabel(self.frame)
        self.pointcloudname.setObjectName(u"pointcloudname")
        self.pointcloudname.setGeometry(QRect(30, 110, 200, 25))
        self.groupBox_2 = QGroupBox(self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(20, 200, 321, 91))
        self.groupBox_2.setStyleSheet(u"")
        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(20, 30, 70, 20))
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(20, 60, 70, 20))
        self.length3d = QLabel(self.groupBox_2)
        self.length3d.setObjectName(u"length3d")
        self.length3d.setGeometry(QRect(100, 30, 40, 20))
        self.width3d = QLabel(self.groupBox_2)
        self.width3d.setObjectName(u"width3d")
        self.width3d.setGeometry(QRect(100, 60, 40, 20))
        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(160, 30, 80, 20))
        self.depth = QLabel(self.groupBox_2)
        self.depth.setObjectName(u"depth")
        self.depth.setGeometry(QRect(250, 30, 50, 20))
        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(160, 60, 80, 20))
        self.vol = QLabel(self.groupBox_2)
        self.vol.setObjectName(u"vol")
        self.vol.setGeometry(QRect(250, 60, 50, 20))
        self.OpenPC = QPushButton(self.frame)
        self.OpenPC.setObjectName(u"OpenPC")
        self.OpenPC.setGeometry(QRect(30, 40, 75, 25))
        self.Extraction_3d = QPushButton(self.frame)
        self.Extraction_3d.setObjectName(u"Extraction_3d")
        self.Extraction_3d.setGeometry(QRect(130, 40, 90, 25))
        self.SaveData_3d = QPushButton(self.frame)
        self.SaveData_3d.setObjectName(u"SaveData_3d")
        self.SaveData_3d.setGeometry(QRect(240, 40, 90, 25))
        self.subWidget_2.addTab(self.PointCloudAnalysis, "")
        self.MaintabWidget.addTab(self.threeDim, "")
        self.MaintabWidget.currentChanged.connect(self.on_mtw_change)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 960, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.gentimer = QTimer()  # 定时器
        self.check_cam = False
        self.initialize()
        self.gentimer.timeout.connect(self.update)
        self.retranslateUi(MainWindow)
        self.activate()
        self.MaintabWidget.setCurrentIndex(0)
        self.SubtabWidget_1.setCurrentIndex(0)
        self.subWidget_2.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi
    '''
    初始化电子秤，时钟，相机，裂纹检测程序
    为视图添加最初的默认图像
    '''
    def initialize(self):
        self.tabindex = 0  # 哪个tabwidget打开了
        self.yolo = None  # 裂纹检测程序
        # 相机连接情况
        self.bCam = binoCamera(left_index=1,right_index=2)
        self.Cam1St = False
        self.Cam2St = False
        self.Cams_opened = False  # 是否开启相机
        self.changeCamStatus()
        # 显示默认图像
        init_img = cv2.imread(resource_path(os.path.join("res", "CAU.JPG")))
        self.show_binoimg(init_img, init_img)
        self.show_binoimg_pointcloud(init_img, init_img)
        self.weight = None  # 电子秤读数
        self.gentimer.start(300)  # 启动计时器
        # 连接电子秤
        self.scale = self.connect_scale()
        self.phenoExt = phenoExtractor()
        self.data = phenoDatum()
        # 点云
        self.PCP = PointCloudProcess()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("作物籽粒表型提取系统")
        # MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.SelectImage.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u56fe\u50cf", None))
        self.SubtabWidget_1.setTabText(self.SubtabWidget_1.indexOf(self.binoImg), QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u56fe\u50cf", None))
        self.cam2Exp.setText(QCoreApplication.translate("MainWindow", u"\u53f3\u76ee\u76f8\u673a", None))
        self.cam1Exp.setText(QCoreApplication.translate("MainWindow", u"\u5de6\u76ee\u76f8\u673a", None))
        self.cam2Status.setText("")
        self.camCnt.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5\u53cc\u76ee\u76f8\u673a", None))
        self.cam1Status.setText("")
        self.TakeImages.setText(QCoreApplication.translate("MainWindow", u"\u62cd\u6444\u56fe\u50cf", None))
        self.SubtabWidget_1.setTabText(self.SubtabWidget_1.indexOf(self.binocamera), QCoreApplication.translate("MainWindow", u"\u91c7\u96c6\u65b0\u56fe\u50cf", None))
        self.scaleZero.setText(QCoreApplication.translate("MainWindow", u"\u7535\u5b50\u79e4\u8c03\u96f6", None))
        self.CrackDetect.setText(QCoreApplication.translate("MainWindow", u"\u5927\u8c46\u88c2\u7eb9\u68c0\u6d4b", None))
        self.Extraction.setText(QCoreApplication.translate("MainWindow", u"\u8868\u578b\u63d0\u53d6", None))
        self.SaveData.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u8868\u578b\u6570\u636e", None))
        self.gb_pheno.setTitle(QCoreApplication.translate("MainWindow", u"籽粒表型参数", None))
        self.gb_color.setTitle(QCoreApplication.translate("MainWindow", u"籽粒颜色参数", None))
        self.gb_txtre.setTitle(QCoreApplication.translate("MainWindow", u"籽粒纹理特征", None))
        self.lb_length.setText(QCoreApplication.translate("MainWindow", u"\u957f\u5ea6(mm)\uff1a", None))
        self.lb_width.setText(QCoreApplication.translate("MainWindow", u"\u5bbd\u5ea6(mm)\uff1a", None))
        self.length.setText(QCoreApplication.translate("MainWindow", u"null", None))
        self.width.setText(QCoreApplication.translate("MainWindow", u"null", None))
        self.lb_area.setText(QCoreApplication.translate("MainWindow", u"<html><body>投影面积(mm<sup>2</sup>):</body></html>", None))
        self.area.setText(QCoreApplication.translate("MainWindow", u"null", None))
        self.lb_gloriness.setText(QCoreApplication.translate("MainWindow", u"\u5149\u6cfd\u5ea6\uff1a", None))
        self.glossiness.setText(QCoreApplication.translate("MainWindow", u"null", None))
        self.lb_avgRGB.setText(QCoreApplication.translate("MainWindow", u"平均颜色", None))
        self.lb_mRGB.setText(QCoreApplication.translate("MainWindow", u"主频颜色", None))
        self.avgR.setText(QCoreApplication.translate("MainWindow", u"null", None))
        self.priR.setText(QCoreApplication.translate("MainWindow", u"null", None))
        self.scaleNum.setText(QCoreApplication.translate("MainWindow", u"null", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u7535\u5b50\u79e4\u8bfb\u6570(g)\uff1a", None))
        self.MaintabWidget.setTabText(self.MaintabWidget.indexOf(self.twoDim), QCoreApplication.translate("MainWindow", u"2\u7ef4\u8868\u578b", None))
        self.SelectImages.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u53cc\u76ee\u56fe\u50cf", None))
        self.GenPC.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u70b9\u4e91", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u8fdb\u5ea6", None))
        self.SavePC.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u70b9\u4e91", None))
        self.subWidget_2.setTabText(self.subWidget_2.indexOf(self.PointCouldGen), QCoreApplication.translate("MainWindow", u"\u751f\u6210\u70b9\u4e91", None))
        self.pointcloudname.setText(QCoreApplication.translate("MainWindow", u"\u672a\u9009\u62e9\u70b9\u4e91", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u7c7d\u7c92\u5e73\u5747\u53c2\u6570", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u957f\u5ea6(mm)\uff1a", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u5bbd\u5ea6(mm)\uff1a", None))
        self.length3d.setText(QCoreApplication.translate("MainWindow", u"null", None))
        self.width3d.setText(QCoreApplication.translate("MainWindow", u"null", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u539a\u5ea6(mm)\uff1a", None))
        self.depth.setText(QCoreApplication.translate("MainWindow", u"null", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"<html><body>体积(mm<sup>3</sup>):</body></html>", None))
        self.vol.setText(QCoreApplication.translate("MainWindow", u"null", None))
        self.OpenPC.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u70b9\u4e91", None))
        self.Extraction_3d.setText(QCoreApplication.translate("MainWindow", u"\u8868\u578b\u63d0\u53d6", None))
        self.SaveData_3d.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u8868\u578b\u6570\u636e", None))
        self.subWidget_2.setTabText(self.subWidget_2.indexOf(self.PointCloudAnalysis), QCoreApplication.translate("MainWindow", u"\u4e09\u7ef4\u8868\u578b\u5206\u6790", None))
        self.MaintabWidget.setTabText(self.MaintabWidget.indexOf(self.threeDim), QCoreApplication.translate("MainWindow", u"3\u7ef4\u8868\u578b", None))
    # retranslateUi

    '''
    连接电子秤
    成功则返回实例
    否则返回空值
    '''
    def connect_scale(self):
        try:
            scale = ScaleModbusRTU(port='COM6', baudrate=9600, timeout=1)
            return scale
        except Exception as e:
            print(f"连接电子秤时发生错误: {e}")
            return None

    '''
    根据bool值改变两个显示灯的颜色
    True即成功连接，为(0, 255, 127)
    False为连接失败，为(67, 67, 67)
    '''
    def changeCamStatus(self):
        if self.Cam1St:
            self.cam1Status.setStyleSheet(u"QLabel{\n"
                                          "	background-color:rgb(0, 255, 127);\n"
                                          "}")
        elif not self.Cam1St:
            self.cam1Status.setStyleSheet(u"QLabel{\n"
                                          "	background-color:rgb(67, 67, 67);\n"
                                          "}")
        if self.Cam2St:
            self.cam2Status.setStyleSheet(u"QLabel{\n"
                                          "	background-color:rgb(0, 255, 127);\n"
                                          "}")
        elif not self.Cam2St:
            self.cam2Status.setStyleSheet(u"QLabel{\n"
                                          "	background-color:rgb(67, 67, 67);\n"
                                          "}")

    '''
    为各个按钮绑定各自的函数
    '''
    def activate(self):
        # 绑定按钮
        self.SelectImage.clicked.connect(self.on_open_photo_clicked)  # 选择双目图像
        self.scaleZero.clicked.connect(self.on_scaleZero_clicked)  # 电子秤调零
        self.Extraction.clicked.connect(self.on_Extraction_clicked)  # 提取大豆二维表型
        self.SaveData.clicked.connect(self.on_SaveData_clicked)  # 保存二维表型
        self.CrackDetect.clicked.connect(self.run_yolo)  # 运行裂纹检测程序
        self.camCnt.clicked.connect(self.on_camCnt_clicked)  # 连接双目相机
        self.TakeImages.clicked.connect(self.on_TakeImages_clicked)  # 拍摄双目图像
        self.SelectImages.clicked.connect(self.on_open_photo_pointcloud_clicked)  # 选择双目图像
        self.GenPC.clicked.connect(self.on_GenPC_clicked)  # 生成点云，其中需要调用self.progressBar
        self.SavePC.clicked.connect(self.on_SavePC_clicked)  # 保存点云
        self.OpenPC.clicked.connect(self.on_open_pointcloud_clicked)  # 打开点云
        self.Extraction_3d.clicked.connect(self.on_Extraction_3d_clicked)  # 提取三维表型
        self.SaveData_3d.clicked.connect(self.on_SaveData_3d_clicked)  # 保存三维表型


    '''
    更新相机和电子秤状态
    '''
    def update(self):
        if self.check_cam:  # 相机连接页面
            if not self.Cams_opened:  # 未打开相机，尝试连接
                self.Cam1St, self.Cam2St= self.bCam.check_binocam()
                self.changeCamStatus()
            elif (self.Cam1St and self.Cam2St) and self.Cams_opened:  # 已连接相机，更新画面
                try:
                    image_left, image_right = self.bCam.get_frames()
                except Exceptions.FrameLostError as e:
                        # 错误处理
                    print(f"Error:{e}")
                    self.Cam1St, self.Cam2St, self.Cams_opened = False
                    self.bCam.close()
                else: 
                    self.show_binoimg(image_left, image_right)
        if self.scale is not None:
            self.weight = self.scale.get_weight()
            self.scaleNum.setText(str(self.weight))

    def on_mtw_change(self):
        index = self.MaintabWidget.currentIndex()
        if index == 1:
            self.check_cam = False

    def on_subtw1_change(self):
        index = self.SubtabWidget_1.currentIndex()
        if index == 1:
            self.check_cam = True
        elif index == 0:
            self.check_cam = False

    def on_camCnt_clicked(self):
        if self.Cam1St and self.Cam2St:
            self.bCam.open_binocam()
            self.Cams_opened = True  # 具体更新画面在update里实现
        else:
            QMessageBox.information(None, "error", "相机未连接！")

    def on_TakeImages_clicked(self):
        if self.bCam:
            file_path, _ = QFileDialog.getSaveFileName(None, "Save File", "", "Image Files (*.jpg);;All Files (*)")
            if file_path:
                # print(f"Selected file: {file_path}")
                # 拆分文件名以获取路径和单纯的文件名
                file_name, _ = os.path.splitext(file_path)
                newfn_L = file_name + '_L.jpg'
                newfn_R = file_name + '_R.jpg'
                image_left,image_right = self.bCam.get_frames()
                self.take_photo(image_left, newfn_L)
                self.take_photo(image_right, newfn_R)
                self.phenoExt.img = image_left
        else:
            QMessageBox.information(None, "error", "相机未连接！")

    def take_photo(self, frame, filename):
        cv2.imwrite(filename, frame)
        print(f"照片已保存为 {filename}")

    def on_open_pointcloud_clicked(self):
        filepath = self.open_pointcloud()
        if len(filepath) != 0:
            self.PCP.pcd = o3d.io.read_point_cloud(filepath)
            self.PCP.display_pointcloud(self.PCP.pcd)
            self.pointcloudname.setText(filepath)

    def open_pointcloud(self, filter="Pointcloud files (*.pcd *.ply)"):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "点云文件选择", "E:\\ricePhenoExt\\pre", filter, options=options)
        return file_name

    def open_image(self, filter="Image files (*.png *.jpg *.bmp)"):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "单目图像选择", "E:\\ricePhenoExt\\pre", filter, options=options)
        return file_name
    
    # 打开双目图像
    def on_open_photo_clicked(self):
        self.Cams_opened = False
        file_name = self.open_image()
        L_img = cv2.imread(file_name)
        R_img = cv2.imread(resource_path(os.path.join("res", "CAU.JPG")))
        self.show_binoimg(L_img,R_img)
        self.phenoExt.img =L_img

    def show_binoimg(self, L_img_cv2, R_img_cv2):
        # 将OpenCV图像转换为QImage
        L_img_qt = cv2_to_qt(L_img_cv2)
        R_img_qt = cv2_to_qt(R_img_cv2)

        # 将QImage转换为QPixmap
        L_pixmap = QPixmap.fromImage(L_img_qt)
        R_pixmap = QPixmap.fromImage(R_img_qt)

        # 设置QGraphicsPixmapItem的Pixmap
        self.ViewL.setPixmap(L_pixmap)
        self.ViewR.setPixmap(R_pixmap)

    # 打开双目图像
    def on_open_photo_pointcloud_clicked(self):
        file_name = self.open_image()
        # print(file_name)
        # 查找最后一个点（.）的位置
        dot_index = file_name.rfind('.')

        # 如果找到了点，获取点之前的最后一个字符
        if dot_index != -1:
            last_char = file_name[dot_index - 1]
        else:
            # 如果文件名中没有点，则获取整个文件名的最后一个字符
            last_char = file_name[-1]

        if last_char == 'L':
            anotherfile = file_name.replace('L', 'R', dot_index - 1)
            L_img_cv2 = cv2.imread(file_name)
            R_img_cv2 = cv2.imread(anotherfile)

        elif last_char == 'R':
            anotherfile = file_name.replace('R', 'L', dot_index - 1)
            L_img_cv2 = cv2.imread(anotherfile)
            R_img_cv2 = cv2.imread(file_name)

        self.PCP.L_img, self.PCP.R_img = L_img_cv2,R_img_cv2
        self.progressBar.setValue(0)
        self.show_binoimg_pointcloud(L_img_cv2,R_img_cv2)

    def show_binoimg_pointcloud(self, L_img_cv2, R_img_cv2):
        # 将OpenCV图像转换为QImage
        L_img_qt = cv2_to_qt(L_img_cv2)
        R_img_qt = cv2_to_qt(R_img_cv2)

        # 将QImage转换为QPixmap
        L_pixmap = QPixmap.fromImage(L_img_qt)
        R_pixmap = QPixmap.fromImage(R_img_qt)

        # 设置QGraphicsPixmapItem的Pixmap
        self.ViewL_1.setPixmap(L_pixmap)
        self.ViewR_1.setPixmap(R_pixmap)

    def on_scaleZero_clicked(self):
        if self.scale is not None:
            self.scale.get_zero()
        else:
            QMessageBox.warning(None, "error", "未连接电子秤！")

    def on_Extraction_clicked(self):
        # 检查哪个单选按钮被选中
        selected_radio_button = None
        for button in self.buttonGroup.buttons():
            if button.isChecked():
                selected_radio_button = button
                break  # 找到选中的按钮后，跳出循环

        # 根据选中的单选按钮执行相应的操作
        if selected_radio_button is not None:
            if selected_radio_button == self.scltWheat:
                # 水稻被选中，执行相关操作
                print("提取水稻表型")
                self.phenoExt.seed_type = 0
            elif selected_radio_button == self.scltBean:
                # 大豆被选中，执行相关操作
                print("提取大豆表型")
                self.phenoExt.seed_type = 1
            self.pheno_img,pheno_result = self.phenoExt.forward()
            self.show_binoimg(self.phenoExt.img,self.pheno_img)
            num = pheno_result[0].shape[0]
            average_weight = None
            if self.weight is not None:
                average_weight = self.weight/num
            self.update_pheno([average_weight, pheno_result])

    '''
    保存二维表型提取后的图片与数据
    '''
    def on_SaveData_clicked(self):
        if self.data.type != 0:
            QMessageBox.warning(None, "error", "未完成表型提取！")
        else:
            file_path, _ = QFileDialog.getSaveFileName(None, "Save File", "", "")
            if file_path:
                self.take_photo(self.pheno_img, file_path+".jpg")
                self.data.save(file_path)

    '''
    根据双目图像生成点云
    步骤为预处理->生成深度图->生成点云->过滤
    根据步骤调整progressBar
    '''
    def on_GenPC_clicked(self):
        if (self.PCP.L_img is None) or (self.PCP.R_img is None):
            QMessageBox.warning(None, "error", "未选取双目图像！")
        else:
            # 预处理
            self.PCP.preprocess()
            self.show_binoimg_pointcloud(self.PCP.L_img,self.PCP.R_img)
            self.progressBar.setValue(20)
            # 生成深度图
            self.progressBar.setValue(40)
            self.PCP.get_disdep()
            # 生成点云
            self.progressBar.setValue(60)
            self.PCP.generate()
            #过滤
            self.progressBar.setValue(80)
            self.PCP.filter_pc()
            #下采样
            self.progressBar.setValue(100)
            self.PCP.downsampling()
            # 展示
            self.PCP.display_pointcloud(self.PCP.pcd)

    '''
    保存点云
    记住文件名
    在之后修改正在处理pointcloud的文件名和文件
    '''
    def on_SavePC_clicked(self):
        if self.progressBar.value() != 100:
            QMessageBox.warning(None, "error", "未完成点云生成！")
        else:
            file_path, _ = QFileDialog.getSaveFileName(None, "Save PointCloud", "", "")
            if file_path:
                self.PCP.save_pointcloud(file_path)
                self.pointcloudname.setText(file_path+".pcd")

    def on_Extraction_3d_clicked(self):
        if self.PCP.pcd is None:
            QMessageBox.warning(None, "error", "请先选择点云！")
        else:
            pheno = self.PCP.get3dPheno()
            self.update_pheno(pheno)

    def on_SaveData_3d_clicked(self):
        if self.data.type != 1:
            QMessageBox.warning(None, "error", "未完成表型提取！")
        else:
            file_path, _ = QFileDialog.getSaveFileName(None, "Save File", "", "")
            if file_path:
                self.data.save(file_path)

    def update_pheno(self, pheno_result):
        index = self.MaintabWidget.currentIndex()
        if index == 0:
            self.data.type = 0
            ## 二维表型
            self.data.update(pheno_result)
            self.scaleNum.setText(str(self.data.avg_weight))
            self.length.setText(str(self.data.mean_length))
            self.width.setText(str(self.data.mean_width))
            self.area.setText(str(self.data.mean_area))
            self.glossiness.setText(f'{self.data.glossiness:.5g}')
            self.contrast.setText(f'{self.data.gdglcm_feature[0]:.5g}')
            self.dissimilarity.setText(f'{self.data.gdglcm_feature[1]:.5g}')
            self.homogeneity.setText(f'{self.data.gdglcm_feature[2]:.5g}')
            self.energy.setText(f'{self.data.gdglcm_feature[3]:.5g}')
            self.correlation.setText(f'{self.data.gdglcm_feature[4]:.5g}')
            self.asm.setText(f'{self.data.gdglcm_feature[5]:.5g}')
            self.complexity.setText(f'{self.data.gdglcm_feature[6]:.5g}')
            self.avgR.setText(str(f'{self.data.mean_rgb[1][0]:.5g}'))
            self.priR.setText(str(f'{self.data.mode_rgb[1][0]:.5g}'))
            self.avgG.setText(str(f'{self.data.mean_rgb[1][1]:.5g}'))
            self.priG.setText(str(f'{self.data.mode_rgb[1][1]:.5g}'))
            self.avgB.setText(str(f'{self.data.mean_rgb[1][2]:.5g}'))
            self.priB.setText(str(f'{self.data.mode_rgb[1][2]:.5g}'))

            self.avgH.setText(str(f'{self.data.mean_hsv[0]:.3g}'))
            self.priH.setText(str(f'{self.data.mode_rgb[1][0]:.3g}'))
            self.avgS.setText(str(f'{self.data.mean_rgb[1][1]:.5g}'))
            self.priS.setText(str(f'{self.data.mode_rgb[1][1]:.5g}'))
            self.avgV.setText(str(f'{self.data.mean_rgb[1][2]:.5g}'))
            self.priV.setText(str(f'{self.data.mode_rgb[1][2]:.5g}'))

            self.avgL.setText(str(f'{self.data.mean_rgb[1][0]:.5g}'))
            self.priL.setText(str(f'{self.data.mode_rgb[1][0]:.5g}'))
            self.avg_a.setText(str(f'{self.data.mean_rgb[1][1]:.5g}'))
            self.pri_a.setText(str(f'{self.data.mode_rgb[1][1]:.5g}'))
            self.avg_b.setText(str(f'{self.data.mean_rgb[1][2]:.5g}'))
            self.pri_b.setText(str(f'{self.data.mode_rgb[1][2]:.5g}'))
        if index == 1:
            self.data.type = 1
            # 点云
            self.data.update(pheno_result)
            self.length3d.setText(str(self.data.mean_length))
            self.depth.setText(str(self.data.mean_depth))
            self.width3d.setText(str(self.data.mean_width))
            self.vol.setText(str(self.data.mean_vol))

    # 运行裂纹检测程序
    def run_yolo(self):
        if self.yolo is None:
            self.yolo = yolo.CrackDetectWindow()
        self.yolo.show()

    def close(self):
        # 停止定时器
        self.gentimer.stop()
        # 释放摄像头资源
        if self.Cams_opened:
            self.bCam.close()


def cv2_to_qt(cv2_img):
    # 先变换尺寸
    cv2_img = cv2.resize(cv2_img, (306, 256))
    # 转换颜色空间 BGR (OpenCV) -> RGB
    cv2_img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    # 将图像转换为 QImage
    height, width, channels = cv2_img_rgb.shape
    bytes_per_line = channels * width
    QImage_format = QImage.Format_RGB888
    return QImage(cv2_img_rgb.data, width, height, bytes_per_line, QImage_format)


# 继承QMainWindow类，以获取其属性和方法
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置界面为我们生成的界面
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(resource_path(os.path.join("res", "logo.PNG"))))

    def closeEvent(self, event):
        self.ui.close()

# 程序入口
if __name__ == "__main__":
    # 初始化QApplication，界面展示要包含在QApplication初始化之后，结束之前
    app = QApplication(sys.argv)

    # 初始化并展示我们的界面组件
    window = MyWidget()
    window.show()

    # 结束QApplication
    sys.exit(app.exec())

