from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import cv2
from astropy.time import Time
import astropy.units as u

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
        self.differntialTime = 1/self.targetFPS * u.second

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
        font_scale = 2; margin = 5; thickness = 2
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
            if (nowTime - lastTime).to(u.second) > self.differntialTime:
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
                sleep(0.1)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()