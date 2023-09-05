from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap

from WATECUI import Ui_WATEC

import cv2
import time

from Configuration import Configuration
from VideoThread import VideoThread
from Anel import Anel
from AnelClickThread import AnelClickThread
import numpy as np
from astropy.time import Time

class WatecWindow(QtWidgets.QMainWindow, Ui_WATEC):

    def __init__(self, *args, obj=None, **kwargs):
        super(WatecWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setup_WatecUI()

    def setup_WatecUI(self):
        self.label_VideoFrame.setFixedWidth(Configuration.resolutionX)
        self.label_VideoFrame.setFixedHeight(Configuration.resolutionY)

        self.startedVideoThread = False
        self.button_StartRecording.setEnabled(False)
        self.lineEdit_recordPath.setEnabled(False)
        self.button_WatecRemoteDown.setEnabled(False)
        self.button_WatecRemoteEnter.setEnabled(False)
        self.button_WatecRemoteLeft.setEnabled(False)
        self.button_WatecRemoteRight.setEnabled(False)
        self.button_WatecRemoteUp.setEnabled(False)

        self.button_connect.clicked.connect(self.button_connect_clicked)
        self.setWatecControlEnabled(False)

        self.lineEdit_IP_Port.setText("192.168.1.118:8554/watec")
        self.WatecUpPort = 4
        self.WatecDownPort = 8
        self.WatecLeftPort = 5
        self.WatecRightPort = 6
        self.WatecEnterPort = 7
        self.WatecAnelIOIP = "192.168.1.110"
        self.WatecIOOnOffSleep = 0.1
        
        self.button_WatecRemoteDown.clicked.connect(self.button_WatecRemoteDown_clicked)
        self.button_WatecRemoteUp.clicked.connect(self.button_WatecRemoteUp_clicked)
        self.button_WatecRemoteLeft.clicked.connect(self.button_WatecRemoteLeft_clicked)
        self.button_WatecRemoteRight.clicked.connect(self.button_WatecRemoteRight_clicked)
        self.button_WatecRemoteEnter.clicked.connect(self.button_WatecRemoteEnter_clicked)

    def setWatecControlEnabled(self, enabled: bool):
        self.button_StartRecording.setEnabled(enabled)
        self.lineEdit_recordPath.setEnabled(enabled)
        self.button_WatecRemoteDown.setEnabled(enabled)
        self.button_WatecRemoteEnter.setEnabled(enabled)
        self.button_WatecRemoteLeft.setEnabled(enabled)
        self.button_WatecRemoteRight.setEnabled(enabled)
        self.button_WatecRemoteUp.setEnabled(enabled)

    def button_connect_clicked(self):
        if(self.lineEdit_IP_Port.text() is None):
            return

        rtspPath = "rtsp://"+self.lineEdit_IP_Port.text()
        if not self.startedVideoThread:
            self.videoThread = VideoThread(rtspPath=rtspPath)
            self.videoThread.change_pixmap_signal.connect(self.update_image)
            self.videoThread.start()
            self.startedVideoThread = True
            self.button_connect.setText("Stop")
            self.setWatecControlEnabled(True)
            self.WatecAnel = Anel(self.WatecAnelIOIP)
        else:
            self.videoThread.stop()
            self.startedVideoThread = False
            self.button_connect.setText("Connect")
            self.setWatecControlEnabled(False)
            self.WatecAnel = None

        return

    def button_WatecRemoteDown_clicked(self):
        if(self.WatecAnel is not None):
            self.downThread = AnelClickThread(self.WatecAnel, self.WatecDownPort, True, self.WatecIOOnOffSleep)
            self.downThread.start()
    
    def button_WatecRemoteUp_clicked(self):
        if(self.WatecAnel is not None):
            self.upThread = AnelClickThread(self.WatecAnel, self.WatecUpPort, True, self.WatecIOOnOffSleep)
            self.upThread.start()
    
    def button_WatecRemoteLeft_clicked(self):
        if(self.WatecAnel is not None):
            self.leftThread = AnelClickThread(self.WatecAnel, self.WatecLeftPort, True, self.WatecIOOnOffSleep)
            self.leftThread.start()
    
    def button_WatecRemoteRight_clicked(self):
        if(self.WatecAnel is not None):
            self.rightThread = AnelClickThread(self.WatecAnel, self.WatecRightPort, True, self.WatecIOOnOffSleep)
            self.rightThread.start()
    
    def button_WatecRemoteEnter_clicked(self):
        if(self.WatecAnel is not None):
            self.enterThread = AnelClickThread(self.WatecAnel, self.WatecEnterPort, True, self.WatecIOOnOffSleep)
            self.enterThread.start()

    @pyqtSlot(np.ndarray, Time)
    def update_image(self, cv_img, nowTime):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.label_VideoFrame.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(Configuration.resolutionX, Configuration.resolutionY, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)