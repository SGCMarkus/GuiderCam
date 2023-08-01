from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import cv2

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, camPort: int):
        self.camPort = camPort
        super().__init__()

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(self.camPort)
        self._run_flag = True
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()