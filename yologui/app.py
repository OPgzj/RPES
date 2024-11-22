from PySide6.QtWidgets import QApplication, QSplashScreen, QMainWindow, QProgressBar, QWidget
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
import sys
import time

# logging.disable(logging.CRITICAL)  # 禁用所有级别的日志
import yologui.main_window as main_window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('resource/icons/main_icon.png'))  # 图标

    # 创建启动页面，设置为无边框
    splash_pix = QPixmap("resource/icons/background3.png").scaled(900, 800, Qt.AspectRatioMode.KeepAspectRatio)
    splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
    splash.show()

    # 主页面
    CrackDetectWindow = main_window.CrackDetectWindow()
    CrackDetectWindow.show()

    # 启动页面在主页面加载完成后关闭
    splash.finish(CrackDetectWindow)

    sys.exit(app.exec())

def run_as_yolo():
    app = QMainWindow()

    # 主页面
    CrackDetectWindow = main_window.CrackDetectWindow()
    CrackDetectWindow.show()

    return app.exec()


