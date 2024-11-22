# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QWidget, QFileDialog, QMessageBox)
import sys
from bino import bino_Form
from pcui import pointcloud_Form
import cv2
import yolo_main as yolo

class Ui_mainMenu(object):
    def setupUi(self, mainMenu):
        if not mainMenu.objectName():
            mainMenu.setObjectName(u"mainMenu")
        mainMenu.resize(400, 159)
        self.openCamera = QPushButton(mainMenu)
        self.openCamera.setObjectName(u"openCamera")
        self.openCamera.setGeometry(QRect(10, 110, 90, 24))
        self.openCamera.clicked.connect(self.on_open_cameras_clicked)  # 单击打开图像
        self.get2D = QPushButton(mainMenu)
        self.get2D.setObjectName(u"get2D")
        self.get2D.setGeometry(QRect(100, 110, 90, 24))
        self.get2D.clicked.connect(self.on_open_get2D_clicked)
        self.openPhoto = QPushButton(mainMenu)
        self.openPhoto.setObjectName(u"openPhoto")
        self.openPhoto.setGeometry(QRect(190, 110, 100, 24))
        self.openPhoto.clicked.connect(self.on_open_photo_clicked)  # 单击打开图像
        self.label = QLabel(mainMenu)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(110, 40, 191, 16))
        self.openPC = QPushButton(mainMenu)
        self.openPC.setObjectName(u"openPC")
        self.openPC.setGeometry(QRect(290, 110, 90, 24))
        self.openPC.clicked.connect(self.on_open_pc_clicked)  # 单击打开点云
        self.yolo = None  # 裂纹检测程序
        self.retranslateUi(mainMenu)

        QMetaObject.connectSlotsByName(mainMenu)
    # setupUi

    def retranslateUi(self, mainMenu):
        mainMenu.setWindowTitle(QCoreApplication.translate("mainMenu", u"系统主页", None))
        self.openCamera.setText(QCoreApplication.translate("mainMenu", u"打开双目相机", None))
        self.get2D.setText(QCoreApplication.translate("mainMenu", u"分析二维表型", None))
        self.openPhoto.setText(QCoreApplication.translate("mainMenu", u"三维点云生成", None))
        self.label.setText(QCoreApplication.translate("mainMenu", u"高通量作物种子表型提取系统", None))
        self.openPC.setText(QCoreApplication.translate("mainMenu", u"三维表型分析", None))
    # retranslateUi

    def open_image(self, filter="Image files (*.png *.jpg *.bmp)"):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "单目图像选择", "", filter, options=options)
        return file_name

    def open_pointcloud(self, filter="Pointcloud files (*.pcd )"):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "点云文件选择", "", filter, options=options)
        return file_name

    # 打开双目图像
    def on_open_photo_clicked(self):
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

        self.binowidget = bino_Form(window_type=1, L_img=L_img_cv2, R_img=R_img_cv2)
        self.binowidget.show()

    def on_open_get2D_clicked(self):
        # 区分是水稻还是大豆
        # 创建一个QMessageBox实例
        msg_box = QMessageBox()
        msg_box.setWindowTitle("作物类型选择")
        msg_box.setText("请给出将要分析的作物类型")

        # 添加自定义按钮并设置文本
        soybean_button = msg_box.addButton("大豆", QMessageBox.AcceptRole)  # 可以自定义角色，这里用AcceptRole模拟Ok
        rice_button = msg_box.addButton("水稻", QMessageBox.RejectRole)  # RejectRole模拟Cancel
        # 显示对话框并获取点击的按钮
        result = msg_box.exec()
        if msg_box.clickedButton() == soybean_button:  # 用户需要检测大豆
            soymsg_box = QMessageBox()
            soymsg_box.setWindowTitle("操作选择")
            soymsg_box.setText("请选择将要执行的检测类型")

            # 添加自定义按钮并设置文本
            crkdtc = soymsg_box.addButton("裂纹检测", QMessageBox.AcceptRole)  # 可以自定义角色，这里用AcceptRole模拟Ok
            phenoext = soymsg_box.addButton("二维表型提取", QMessageBox.RejectRole)  # RejectRole模拟Cancel

            soyrst = soymsg_box.exec()

            if soymsg_box.clickedButton() == crkdtc:
                QMessageBox.information(None, "info", "即将启动裂纹检测程序")
                self.run_yolo()
            elif soymsg_box.clickedButton() == phenoext:
                file_name = self.open_image()
                img = cv2.imread(file_name)
                self.binowidget = bino_Form(window_type=3, L_img=img)
                self.binowidget.show()
        elif msg_box.clickedButton() == rice_button:  # 检测水稻
            file_name = self.open_image()
            img = cv2.imread(file_name)
            self.binowidget = bino_Form(window_type=4, L_img=img)
            self.binowidget.show()



    # 打开双目相机
    def on_open_cameras_clicked(self):
        self.binowidget = bino_Form(window_type=2)
        self.binowidget.show()


    def on_open_pc_clicked(self):
        self.pcwidget = pointcloud_Form()
        self.pcwidget.show()

    # 运行裂纹检测程序
    def run_yolo(self):
        if self.yolo is None:
            self.yolo = yolo.CrackDetectWindow()
        self.yolo.show()



# 继承QWidget类，以获取其属性和方法
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        # 设置界面为我们生成的界面
        self.ui = Ui_mainMenu()
        self.ui.setupUi(self)



# 程序入口
if __name__ == "__main__":
    # 初始化QApplication，界面展示要包含在QApplication初始化之后，结束之前
    app = QApplication(sys.argv)

    # 初始化并展示我们的界面组件
    window = MyWidget()
    window.show()

    # 结束QApplication
    sys.exit(app.exec())

