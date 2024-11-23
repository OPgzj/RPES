import os
from binoCamera import binoCamera
import sys
from Modbus import ScaleModbusRTU
import pandas as pd
import sys
from PySide6.QtCore import (QCoreApplication, QTimer,QMetaObject, QRect,
    QSize)
from PySide6.QtGui import (QIcon,QImage,  QPixmap)
from PySide6.QtWidgets import (QApplication, QFrame, QRadioButton, QGroupBox,
    QLabel, QMainWindow, QMenuBar, QProgressBar,QButtonGroup,
    QPushButton, QSizePolicy, QStatusBar, QTabWidget, QFileDialog,QMessageBox,
    QWidget)
import cv2

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class BSWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题

        self.setWindowTitle('批量拍摄')
        self.resize(666, 370)
        self.setMaximumSize(QSize(666, 370))
        self.setMinimumSize(QSize(666, 370))
        self.setStyleSheet(u"QMainWindow{\n"
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
        self.btnframe = QFrame(self)
        self.btnframe.setGeometry(QRect(35, 280, 170, 85))
        # 4个按钮
        self.createbatch = QPushButton('新建批次', self.btnframe)
        self.createbatch.setGeometry(QRect(10, 10, 70, 25))

        self.selectbatch = QPushButton('选择批次', self.btnframe)
        self.selectbatch.setGeometry(QRect(90, 10, 70, 25))

        self.scalezero = QPushButton('调零', self.btnframe)
        self.scalezero.setGeometry(QRect(10, 50, 70, 25))

        self.takeimages = QPushButton('拍摄图像', self.btnframe)
        self.takeimages.setGeometry(QRect(90, 50, 70, 25))

        self.Limg = QLabel(self)
        self.Limg.setGeometry(QRect(35, 10, 306, 256))
        self.Rimg = QLabel(self)
        self.Rimg.setGeometry(QRect(345, 10, 306, 256))

        self.infoGB = QGroupBox("info", self)
        self.infoGB.setGeometry(QRect(230, 280, 255, 85))
        self.scaleLabel = QLabel("电子秤度数:", self.infoGB)
        self.scaleLabel.setGeometry(QRect(20, 30, 70, 20))
        self.scaleNum = QLabel("0.000", self.infoGB)
        self.scaleNum.setGeometry(QRect(100, 30, 70, 20))
        self.batchLabel = QLabel("批次名称:", self.infoGB)
        self.batchLabel.setGeometry(QRect(20, 55, 70, 20))
        self.batchName = QLabel("null", self.infoGB)
        self.batchName.setGeometry(QRect(100, 55, 70, 20))


    class BatchSnap():
        def init():
            self.scale = null
        
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
        
        def take_photo(self, frame, filename):
            cv2.imwrite(filename, frame)
            print(f"照片已保存为 {filename}")



if __name__ == "__main__":
    # 创建QApplication对象
    app = QApplication(sys.argv)

    # 创建MyWidget实例
    my_widget = BSWidget()

    # 显示窗口
    my_widget.show()

    # 运行QApplication事件循环
    sys.exit(app.exec())
