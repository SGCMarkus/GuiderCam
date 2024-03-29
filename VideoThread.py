from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import cv2
import time as t
from astropy.time import Time
import astropy.units as u

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray, Time)

    def __init__(self, camPort: int = -1, spf: float = 30, config = {}, rtspPath: str = ""):
        if(camPort > -1):
            self.useCamPort = True
            self.camPort = camPort
            self.targetSPF = spf * u.second
            if(config["ALLSKY"]):
                self.font_scale = config["ALLSKY"].getfloat("DateFontScale");
                self.font_margin = config["ALLSKY"].getint("DateFontMargin");
                self.font_thickness = config["ALLSKY"].getint("DateFontThickness")
            else:
                self.font_scale = 0.55;
                self.font_margin = 5;
                self.font_thickness = 1
        elif(rtspPath != ""):
            self.useCamPort = False
            self.rtspPath = rtspPath
            
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
        color = (255, 255, 255)

        size = cv2.getTextSize(text, font, self.font_scale, self.font_thickness)

        textWidth = size[0][0]
        textHeight = size[0][1]
        lineHeight = textHeight + size[1] + self.font_margin

        x = cv_img.shape[1] - self.font_margin - textWidth
        y = self.font_margin + size[0][1] + line * lineHeight

        return cv2.putText(cv_img, text, (x, y), font, self.font_scale, color, self.font_thickness)

    def runFromCamPort(self):
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

                        self.change_pixmap_signal.emit(cv_img, nowTime)
                lastTime = Time.now()
                cap.release()
            else:
                t.sleep(0.1)
        # shut down capture system
        cap.release()

    def runFromRtsp(self):
        cap = cv2.VideoCapture(self.rtspPath)
        self._run_flag = True
        
        while self._run_flag:
            if(not cap.isOpened()):
                cap = cv2.VideoCapture(self.rtspPath) # account for Timeouts/random disconnects

            ret, cv_img = cap.read()
            if(ret):
                self.change_pixmap_signal.emit(cv_img, Time.now())
            
        cap.release()

    def run(self):
        if(self.useCamPort):
            self.runFromCamPort()
        elif(self.rtspPath is not None):
            self.runFromRtsp()
            

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()