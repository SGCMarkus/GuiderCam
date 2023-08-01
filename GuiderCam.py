import os, sys
from astropy.io import fits

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap

from matplotlib.backends.backend_qtagg import (
     FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from GuiderCamUI import Ui_GuiderCam

from alpaca.camera import Camera
from ciboulette.indiclient.camera import ATIKCam383L
from ciboulette.base import ciboulette
from ciboulette.utils import exposure
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits

import cv2

from Configuration import Configuration
from VideoThread import VideoThread
from WeatherCamControl import WeatherCamControl
import numpy as np

class GuiderCamWindow(QtWidgets.QMainWindow, Ui_GuiderCam):

    def __init__(self, *args, obj=None, **kwargs):
        super(GuiderCamWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setup_GuiderCamArea()
        self.setup_WeatherCamArea()

    def setup_GuiderCamArea(self):
        self.cibouletteClient = ciboulette.Ciboulette()
        self.exposure = exposure.Exposure()
        self.cibouletteClient.asi178

        self.curFig = Figure(figsize=(5,30))
        self.curFigAxis = self.curFig.add_subplot()

        fc = FigureCanvas(self.curFig)
        toolbar = NavigationToolbar(fc, self)
        self.vertLayoutMatplotlib.addWidget(toolbar)
        self.vertLayoutMatplotlib.addWidget(fc)

        self.lineEdit_IP_Port.setText("localhost:11111") # Default IP/port
        self.lineEdit_DeviceID.setText("0") # Default device ID

        self.slider_ExposureTime.valueChanged.connect(self.slider_ExposureTime_valueChanged)
        self.slider_Gain.valueChanged.connect(self.slider_Gain_valueChanged)

        self.spinBox_ExposureTime.valueChanged.connect(self.spinBox_ExposureTime_valueChanged)
        self.spinBox_Gain.valueChanged.connect(self.spinBox_Gain_valueChanged)
        
        self.button_connect.clicked.connect(self.button_connect_clicked)
        
        self.checkBox_startSeries.setEnabled(False)
        self.checkBox_startSeries.stateChanged.connect(self.checkBox_startSeries_checked)
        self.label_5.setEnabled(False)
        self.lineEdit_seriesNumber.setEnabled(False)
        self.button_startSeries.setEnabled(False)
        self.button_startSeries.setText("Take Image")
        self.button_startSeries.clicked.connect(self.button_startSeries_clicked)

    def setup_WeatherCamArea(self):
        self.label_VideoFrame.setFixedWidth(Configuration.resolutionX)
        self.label_VideoFrame.setFixedHeight(Configuration.resolutionY)

        a_cam_ports,w_cam_ports,n_w_cam_ports = Configuration.getCameraPorts()
        com_ports = Configuration.getSerialPorts()

        for w_cam_port in w_cam_ports:
            self.cb_CamDeviceIDs.addItem(str(w_cam_port))
        self.cb_COMPorts.addItems(com_ports)
        self.button_StartWeatherObs.clicked.connect(self.button_StartWeatherObs_clicked)
        self.startedVideoThread = False
        self.isNightMode = False

        self.button_ForceCameraMode.clicked.connect(self.button_ForceCameraMode_clicked)

    def button_ForceCameraMode_clicked(self):
        if(self.isNightMode):
            self.weatherCamConctrol.setDay()
            self.isNightMode = False
            self.button_ForceCameraMode.setText("Force Day Mode")
        else:
            self.weatherCamConctrol.setNight()
            self.isNightMode = True
            self.button_ForceCameraMode.setText("Force Night Mode")
        return

    def button_StartWeatherObs_clicked(self):
        if not self.startedVideoThread:
            camPort = int(self.cb_CamDeviceIDs.itemData(self.cb_CamDeviceIDs.currentIndex(), 2))
            self.weatherSerialPort = self.cb_COMPorts.itemData(self.cb_COMPorts.currentIndex(), 2)
            self.weatherCamConctrol = WeatherCamControl(self.weatherSerialPort)

            self.videoThread = VideoThread(camPort)
            self.videoThread.change_pixmap_signal.connect(self.update_image)
            self.videoThread.start()
            self.startedVideoThread = True
            self.button_StartWeatherObs.setText("Stop")
        else:
            self.videoThread.stop()
            self.startedVideoThread = False
            self.button_StartWeatherObs.setText("Start")


    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
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

    def slider_ExposureTime_valueChanged(self):
        self.spinBox_ExposureTime.setValue(self.slider_ExposureTime.value())

    def slider_Gain_valueChanged(self):
        self.spinBox_Gain.setValue(self.slider_Gain.value())

    def spinBox_ExposureTime_valueChanged(self):
        self.slider_ExposureTime.setValue(int(self.spinBox_ExposureTime.value()))

    def spinBox_Gain_valueChanged(self):
        self.slider_Gain.setValue(self.spinBox_Gain.value())

    def button_connect_clicked(self):
        self.adress = self.lineEdit_IP_Port.text()
        self.deviceID = int(self.lineEdit_DeviceID.text())
        self.ccd = Camera(self.adress, self.deviceID)
        
        self.checkBox_startSeries.setEnabled(True)
        if(self.checkBox_startSeries.isChecked()):
            self.label_5.setEnabled(True)
            self.lineEdit_seriesNumber.setEnabled(True)
        else:
            self.label_5.setEnabled(False)
            self.lineEdit_seriesNumber.setEnabled(False)
        self.button_startSeries.setEnabled(True)
        
    def checkBox_startSeries_checked(self, int):
        if(self.checkBox_startSeries.isChecked()):
            self.button_startSeries.setText("Take series")
            self.label_5.setEnabled(True)
            self.lineEdit_seriesNumber.setEnabled(True)
        else:
            self.button_startSeries.setText("Take image")
            self.label_5.setEnabled(False)
            self.lineEdit_seriesNumber.setEnabled(False)


    def button_startSeries_clicked(self):
        if(self.checkBox_startSeries.isChecked()):
            # TODO: series code
            return
        else:
            self.ccd.Gain = int(self.spinBox_Gain.value())
            self.exposure.exp_time = float(self.spinBox_ExposureTime.value())
            self.cibouletteClient.exposure = self.exposure
            self.cibouletteClient.camera(self.ccd)

            expose,frameid,datatype = self.cbl.exposure
            image_file = get_pkg_data_filename('dataset/CAM1_INIT_' + str(frameid) + '.fits')
            image_data = fits.getdata(image_file, ext=0)
            self.curFigAxis.clear()
            self.curFigAxis.imshow(image_data, origin='lower', cmap='gray')
            self.curFig.canvas.draw_idle()

if(not os.path.exists("dataset")):
    os.mkdir("dataset")
app = QtWidgets.QApplication(sys.argv)
window = GuiderCamWindow()
window.show()
app.exec()