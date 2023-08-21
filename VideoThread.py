from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import cv2
import time as t
from astropy.time import Time
import astropy.units as u

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, camPort: int, spf: float = 30):
        self.camPort = camPort
        self.targetSPF = spf * u.second

        super().__init__()

    def setTargetSPF(self, spf: float):
        self.targetSPF = spf * u.second

    def putTimestampsOnImage(self, cv_img, when):
        mjd = int(when.mjd)
        tmp = when.iso.split('.')[0].split(' ')
        
        date = tmp[0]; time = tmp[1]

        cv_img = self.putLineOnImage(cv_img, date, 0)
        cv_img = self.putLineOnImage(cv_img, "UT " + time, 1)
        cv_img = self.putLineOnImage(cv_img, "MJD " + str(mjd), 2)
        return cv_img

    def putLineOnImage(self, cv_img, text, line):
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 0.55; margin = 5; thickness = 1
        color = (255, 255, 255)

        size = cv2.getTextSize(text, font, font_scale, thickness)

        textWidth = size[0][0]
        textHeight = size[0][1]
        lineHeight = textHeight + size[1] + margin

        x = cv_img.shape[1] - margin - textWidth
        y = margin + size[0][1] + line * lineHeight

        return cv2.putText(cv_img, text, (x, y), font, font_scale, color, thickness)

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(self.camPort)
        self._run_flag = True
        lastTime = Time.now()
        while self._run_flag:
            nowTime = Time.now()
            if (nowTime - lastTime).to(u.second) > self.targetSPF:
                cap.open(self.camPort)
                ret = cap.grab()
                if ret:
                    ret, cv_img = cap.retrieve()
                    if ret:
                        cv_img = self.putTimestampsOnImage(cv_img, nowTime)

                        self.change_pixmap_signal.emit(cv_img)
                lastTime = Time.now()
                cap.release()
            else:
                t.sleep(0.1)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()