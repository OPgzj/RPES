import cv2
from PySide6.QtWidgets import QMessageBox
import Exceptions

class StereoCamera(object):
    def __init__(self, camera_index:int):
        self.idx = camera_index
        self.width = 2448
        self.height = 2048

    def is_camera_connected(self):
        # Attempt to open the camera
        cap = cv2.VideoCapture(self.idx, cv2.CAP_DSHOW)

        # Check if the camera was opened successfully
        if cap.isOpened():
            cap.release()  # Release the camera if opened successfully
            return True  # Camera is connected
        else:
            return False  # Camera is not connected

    def open_camera(self):
        cap = cv2.VideoCapture(self.idx, cv2.CAP_DSHOW)
        # 设置分辨率
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self.cap = cap
        print(f"camera{self.idx} on")

    def camera_close(self):
        self.cap.release()
        print(f"camera {self.idx}off")

    def get_fream(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, -1)
            return frame
        else:
            QMessageBox.warning(None, "Warning", f"摄像头{self.idx}连接出错")
            raise Exceptions.CameraNotFoundError(f"Please check camera {self.idx} connection.")
            # exit()

'''
双目相机类，实现相机的
连接检测、开启、图像获取、关闭
'''
class binoCamera:
    def __init__(self, left_index=1, right_index=2):
        self.L_cam = StereoCamera(camera_index=left_index)
        self.R_cam = StereoCamera(camera_index=right_index)

    # 连接检测
    def check_binocam(self):
        L_stus = self.L_cam.is_camera_connected()
        R_stus = self.R_cam.is_camera_connected()
        return L_stus,R_stus

    # 开启相机
    def open_binocam(self):
        L_stus,R_stus = self.check_binocam()
        if L_stus and R_stus :
            self.L_cam.open_camera(self.L_cam.leftindex)
            self.R_cam.open_camera(self.R_cam.rightindex)

    # 获取画面
    def get_frames(self):
        try:
            left_frame = self.L_cam.get_fream()
            right_frame = self.R_cam.get_fream()
        except Exceptions.CameraNotFoundError as e:
         # 错误处理
            print(f"Error:{e}")
            raise Exceptions.FrameLostError()
        else:
            return left_frame, right_frame

        

    # 关闭摄像头
    def close(self):
        self.L_cam.camera_close()
        self.R_cam.camera_close()