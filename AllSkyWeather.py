import os, sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap

from AllSkyWeatherUI import Ui_AllSkyWeather

import cv2

from Configuration import Configuration
from VideoThread import VideoThread
from WeatherCamControl import WeatherCamControl
from WeatherDataThread import WeatherDataThread
import numpy as np
from astropy.time import Time

class AllSkyWeatherWindow(QtWidgets.QMainWindow, Ui_AllSkyWeather):

    def __init__(self, *args, obj=None, **kwargs):
        super(AllSkyWeatherWindow, self).__init__()
        self.setupUi(self)
        self.config = kwargs["config"]

        self.setup_AllSkyWeatherUI()

    def setup_AllSkyWeatherUI(self):
        self.label_VideoFrame.setFixedWidth(Configuration.resolutionX)
        self.label_VideoFrame.setFixedHeight(Configuration.resolutionY)

        a_cam_ports,w_cam_ports,n_w_cam_ports = Configuration.getCameraPorts()
        com_ports = Configuration.getSerialPorts()

        for w_cam_port in w_cam_ports:
            self.cb_CamDeviceIDs.addItem(str(w_cam_port))
        self.cb_COMPorts.addItems(com_ports)
        supportedSPF = ["5", "10", "20", "30", "60"]
        self.cb_SupportedSPF.addItems(supportedSPF)
        if(len(supportedSPF) > 0):
            self.cb_SupportedSPF.setCurrentIndex(0)
        self.cb_SupportedSPF.currentTextChanged.connect(self.cb_SupportedSPF_TextChanged)

        self.button_StartWeatherObs.clicked.connect(self.button_StartWeatherObs_clicked)
        self.startedVideoThread = False
        self.isNightMode = False
        self.saveImageDataBasePath = "C:/Daten/ORION"

        self.button_ForceCameraMode.clicked.connect(self.button_ForceCameraMode_clicked)
        
        self.startedWeatherDataThread = False
        self.weatherDataThread = WeatherDataThread()
        self.weatherDataThread.updateWeatherDataSignal.connect(self.updateWeatherData)
        self.weatherDataThread.start()

    def updateWeatherData(self, data):
        if(data is None):
            return
        
        cloudCond = int(data[WeatherDataThread.CLOUD_COND_STR])
        windCond = int(data[WeatherDataThread.WIND_COND_STR])
        rainCond = int(data[WeatherDataThread.RAIN_COND_STR])
        dayCond = int(data[WeatherDataThread.DAY_COND_STR])

        rainF = bool(data[WeatherDataThread.RAIN_F_STR])
        wetF = bool(data[WeatherDataThread.WET_F_STR])
        
        cloudStr, cloudColor = self.weatherDataThread.getCloudConditionString(cloudCond)
        windStr, windColor = self.weatherDataThread.getWindConditionString(windCond)
        rainStr, rainColor = self.weatherDataThread.getRainConditionString(rainCond)
        dayStr, dayColor = self.weatherDataThread.getDayConditionString(dayCond)
        
        rainFIcon, rainFColor = self.weatherDataThread.getRainIcon(rainF)
        wetFIcon, wetFColor = self.weatherDataThread.getWetIcon(wetF)

        self.lb_CloudLevelString.setText(cloudStr)
        self.lb_CloudLevelString.setStyleSheet("color: " + cloudColor)
        self.lb_WindSpeedLevelString.setText(windStr)
        self.lb_WindSpeedLevelString.setStyleSheet("color: " + windColor)
        self.lb_HumidityString.setText(rainStr)
        self.lb_HumidityString.setStyleSheet("color: " + rainColor)
        self.lb_DaylightString.setText(dayStr)
        self.lb_DaylightString.setStyleSheet("color: " + dayColor)
        
        self.lb_RainIndicator.setText(rainFIcon)
        self.lb_RainIndicator.setStyleSheet("color: " + rainFColor)
        self.lb_WetIndicator.setText(wetFIcon)
        self.lb_WetIndicator.setStyleSheet("color: " + wetFColor)

        self.lb_SkyAmbTemp.setText(str(data[WeatherDataThread.REL_SKY_TEMP_STR]))
        self.lb_AmbientTemp.setText(str(data[WeatherDataThread.AMBIENT_TEMP_STR]))
        self.lb_SensorTemp.setText(str(data[WeatherDataThread.SENSOR_TEMP_STR]))
        self.lb_RainHeater.setText(str(data[WeatherDataThread.HEATER_STR]))
        self.lb_WindSpeed.setText(str(data[WeatherDataThread.WIND_STR]))
        self.lb_Humidity.setText(str(data[WeatherDataThread.HUMIDITY_STR]))
        self.lb_DewPoint.setText(str(data[WeatherDataThread.DEW_POINT_STR]))
        self.lb_Daylight.setText(str(data[WeatherDataThread.DAYLIGHT_STR]))
        
        self.lb_LastWeatherUpdate.setText(str(data[WeatherDataThread.LAST_TIME_OK_STR]))

    def cb_SupportedSPF_TextChanged(self, value):
        if not self.startedVideoThread:
            return
        
        spf = float(value)
        self.videoThread.setTargetSPF(spf)

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
            fps = float(self.cb_SupportedSPF.itemData(self.cb_SupportedSPF.currentIndex(), 2))

            self.videoThread = VideoThread(camPort=camPort, spf=fps)
            self.videoThread.change_pixmap_signal.connect(self.update_image)
            self.videoThread.start()
            self.startedVideoThread = True
            self.button_StartWeatherObs.setText("Stop")
            self.cb_SupportedSPF.setEnabled(True)
            self.button_ForceCameraMode.setEnabled(True)
        else:
            self.videoThread.stop()
            self.startedVideoThread = False
            self.button_StartWeatherObs.setText("Start")
            self.cb_SupportedSPF.setEnabled(False)
            self.button_ForceCameraMode.setEnabled(False)


    @pyqtSlot(np.ndarray, Time)
    def update_image(self, cv_img, nowTime):
        """Updates the image_label with a new opencv image"""
        mjdStr = str(int(nowTime.mjd))
        tmp = nowTime.iso.split('.')[0].split(' ')[1]

        dataPath = self.saveImageDataBasePath + "/" + mjdStr + "/"
        fileName = "frame_" + mjdStr + "_" + tmp.replace(":", "_") + ".jpg"
        if(not os.path.exists(dataPath)):
            os.mkdir(dataPath)

        cv2.imwrite(dataPath + fileName, cv_img)
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
