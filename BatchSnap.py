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
    QLabel, QMainWindow, QMenuBar, QProgressBar,QButtonGroup, QTableWidget, QTableWidgetItem, 
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
        
        # 创建按钮框架
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

        # 图像标签
        self.Limg = QLabel(self)
        self.Limg.setGeometry(QRect(35, 10, 306, 256))
        self.Rimg = QLabel(self)
        self.Rimg.setGeometry(QRect(345, 10, 306, 256))

        # 信息框
        self.infoGB = QGroupBox("info", self)
        self.infoGB.setGeometry(QRect(230, 280, 150, 85))
        self.scaleLabel = QLabel("电子秤度数:", self.infoGB)
        self.scaleLabel.setGeometry(QRect(20, 30, 70, 20))
        self.scaleNum = QLabel("0.000", self.infoGB)
        self.scaleNum.setGeometry(QRect(100, 30, 70, 20))
        self.batchLabel = QLabel("批次名称:", self.infoGB)
        self.batchLabel.setGeometry(QRect(20, 55, 70, 20))
        self.batchName = QLabel("null", self.infoGB)
        self.batchName.setGeometry(QRect(100, 55, 70, 20))

        # 创建 QTableWidget
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(400, 280, 206, 90))  # 修改位置和大小
        self.tableWidget.setColumnCount(2)  # 设置列数
        self.tableWidget.setHorizontalHeaderLabels(["名称", "重量"])  # 设置列头
        self.tableWidget.horizontalHeader().setStretchLastSection(True)  # 自动扩展最后一列

    # 函数：添加行到 QTableWidget
    def add_to_table(self, name, weight):
        row_count = self.tableWidget.rowCount()  # 获取当前行数
        self.tableWidget.insertRow(row_count)  # 插入新行
        self.tableWidget.setItem(row_count, 0, QTableWidgetItem(name))  # 设置名称列的值
        self.tableWidget.setItem(row_count, 1, QTableWidgetItem(str(weight)))  # 设置重量列的值

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
        else:
            QMessageBox.information(None, "error", "相机未连接！")

    def take_photo(self, frame, filename):
        cv2.imwrite(filename, frame)
        print(f"照片已保存为 {filename}")

    def on_createbatch_clicked(self):
        # 打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", "")  # 获取选择的文件夹路径
        if folder_path:
            # 获取输入框中的文件夹名称（这里假设有一个输入框）
            batch_name = self.batchName.text()

            # 在选择的文件夹下创建新文件夹
            new_folder_path = os.path.join(folder_path, batch_name)
            os.makedirs(new_folder_path, exist_ok=True)  # 创建文件夹，若存在则忽略

            # 在新文件夹中创建一个 CSV 文件
            csv_file_path = os.path.join(new_folder_path, f"{batch_name}.csv")
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["名称", "重量"])  # 写入 CSV 的表头

            # 提示文件夹和文件创建成功
            QMessageBox.information(self, "成功", f"文件夹和 CSV 文件已创建：\n{csv_file_path}")

    def select_batch(self):
        # 打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", "")  # 获取选择的文件夹路径
        if folder_path:
            # 获取输入框中的文件夹名称（这里假设有一个输入框）
            batch_name = self.batchName.text()

            # 构造 CSV 文件路径
            csv_file_path = os.path.join(folder_path, f"{batch_name}.csv")

            # 检查文件是否存在
            if os.path.isfile(csv_file_path):
                # 文件存在，输出路径
                QMessageBox.information(self, "文件找到", f"找到文件：\n{csv_file_path}")
            else:
                # 文件不存在，报错
                QMessageBox.warning(self, "错误", f"在该文件夹中找不到名为 '{batch_name}.csv' 的文件。")



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
