from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import cv2
import time

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, camPort: int, fps: float = 30):
        self.camPort = camPort
        self.targetFPS = fps
        self.setDifferentialTimeForFPS()

        super().__init__()

    def setTargetFPS(self, fps: float):
        self.targetFPS = fps
        self.setDifferentialTimeForFPS()

    def setDifferentialTimeForFPS(self):
        self.differntialTime = 1000/self.targetFPS/1000


    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(self.camPort)
        self._run_flag = True
        lastTime = time.time()
        while self._run_flag:
            ret, cv_img = cap.read()
            nowTime = time.time()
            if ret and (nowTime - lastTime) > self.differntialTime:
                self.change_pixmap_signal.emit(cv_img)
                lastTime = time.time()
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()