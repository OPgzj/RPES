# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pcui.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtWidgets import (QApplication, QPushButton, QSizePolicy, QWidget, QFileDialog,QMessageBox)
import PCprocess
import os
import open3d as o3d

class pointcloud_Form(QWidget):
    def __init__(self, pcd=None):
        super().__init__()
        self.pcd = pcd
        self.clst = []
        self.setupUi(self)

    def setupUi(self, QWidget):
        if not QWidget.objectName():
            QWidget.setObjectName(u"Form")
        QWidget.resize(242, 143)
        self.pushButton = QPushButton(QWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(30, 40, 75, 24))
        self.pushButton.clicked.connect(self.on_open_pointcloud_clicked)
        self.pushButton_2 = QPushButton(QWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(130, 40, 75, 24))
        self.pushButton_2.clicked.connect(self.on_filter_clicked)
        self.pushButton_3 = QPushButton(QWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(30, 90, 75, 24))
        self.pushButton_3.clicked.connect(self.on_clustering_clicked)
        self.pushButton_4 = QPushButton(QWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(130, 90, 80, 24))
        self.pushButton_4.clicked.connect(self.on_get3dpheno_clicked)

        self.retranslateUi(QWidget)

        QMetaObject.connectSlotsByName(QWidget)
        if self.pcd is not None:
            self.show_pointcloud()
    # setupUi

    def retranslateUi(self, QWidget):
        QWidget.setWindowTitle(QCoreApplication.translate("Form", u"点云处理", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"打开pcd", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"过滤离群点", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"聚类", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"导出三维表型", None))
    # retranslateUi

    def open_pointcloud(self, filter="Pointcloud files (*.ply *.pcd )"):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "点云文件选择", "", filter, options=options)
        return file_name

    def on_open_pointcloud_clicked(self):
        filepath = self.open_pointcloud()
        if len(filepath) != 0:
            self.file_name, _ = os.path.splitext(filepath)
            QMessageBox.information(None, "info", f"打开{self.file_name}")
            self.pcd = o3d.io.read_point_cloud(filepath)
            self.show_pointcloud(self.pcd, with_axis=True)
            # 更改窗口标题
            self.setWindowTitle(f"正在处理{self.file_name}")

    def on_filter_clicked(self):
        if self.pcd == None:
            QMessageBox.warning(None, "error", "未选择点云！")
        else:
            temppcd = PCprocess.filter_pc(self.pcd)
            self.show_pointcloud(temppcd)
            reply = QMessageBox.information(None, "info", f"完成点云过滤，是否保存？", QMessageBox.Ok | QMessageBox.Cancel)
            # 检查用户是否点击了"确定"按钮
            if reply == QMessageBox.Ok:
                path = self.file_name + "_filtered.pcd"
                QMessageBox.information(None, "info", f"点云已保存至 {path}")
                o3d.io.write_point_cloud(path, temppcd)
                self.pcd = temppcd

    def on_clustering_clicked(self):
        if self.pcd == None:
            QMessageBox.warning(None, "error", "未选择点云！")
        else:
            downpcd = PCprocess.downsampling(self.pcd)
            resultpcd, clst, label = PCprocess.clustering(downpcd)
            QMessageBox.information(None, "info", f"聚类结果为{label}")
            self.show_pointcloud(resultpcd)
            reply = QMessageBox.information(None, "info", f"是否使用此聚类结果？", QMessageBox.Ok | QMessageBox.Cancel)
            # 检查用户是否点击了"确定"按钮
            if reply == QMessageBox.Ok:
                self.label = label
                self.clst = clst
                self.downpcd = downpcd

    def on_get3dpheno_clicked(self):
        if len(self.clst) == 0:
            QMessageBox.warning(None, "error", "未完成聚类！")
        else:
            path = self.file_name + "_3Dpheno.csv"
            QMessageBox.information(None, "info", f"三维表型已保存至 {path}")
            PCprocess.get3dPheno(self.label, self.clst, self.downpcd, path)

    '''
    这个方法会创建一个包含三个相互垂直的箭头的坐标框架，其中红色箭头对应X轴，绿色箭头对应Y轴，蓝色箭头对应Z轴。
    '''
    def draw_with_axis(self, geoms):
        # 创建一个坐标轴几何体
        axis_pcd = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0, origin=[0, 0, 0])
        # 将坐标轴和其它几何体一起绘制
        o3d.visualization.draw_geometries([axis_pcd] + [geoms])

    def show_pointcloud(self, pcd, with_axis=False):
        if with_axis:
            self.draw_with_axis(pcd)
        else:
            o3d.visualization.draw_geometries([pcd])


