import os, sys
import datetime

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap

from AllSkyWeatherUI import Ui_AllSkyWeather

import cv2
import traceback
import mysql.connector

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
        if(self.autoStart):
            self.button_StartWeatherObs_clicked()

    def setup_AllSkyWeatherUI(self):
        try:
            self.autoStart = self.config["ALLSKY"].getboolean("AutoStart")
            self.label_VideoFrame.setFixedWidth(self.config["ALLSKY"].getint("ResolutionX"))
            self.label_VideoFrame.setFixedHeight(self.config["ALLSKY"].getint("ResolutionY"))

            configFileCamDeviceID = self.config["ALLSKY"]["DeviceID"]
            configFileComPort = self.config["ALLSKY"]["ComPort"]

            a_cam_ports,w_cam_ports,n_w_cam_ports = Configuration.getCameraPorts()
            com_ports = Configuration.getSerialPorts()

            matchingCamIDIndex = -1
            matchingComPortIndex = -1

            for i, w_cam_port in enumerate(w_cam_ports):
                self.cb_CamDeviceIDs.addItem(str(w_cam_port))
                if(str(w_cam_port) == configFileCamDeviceID):
                    matchingCamIDIndex = i
                
            self.cb_COMPorts.addItems(com_ports)
            for i, com_port in enumerate(com_ports):
                self.cb_COMPorts.addItem(str(com_port))
                if(str(com_port) == configFileComPort):
                    matchingComPortIndex = i

            if(matchingCamIDIndex >= 0):
                self.cb_CamDeviceIDs.setCurrentIndex(matchingCamIDIndex)
            else:
                print("Error, Camera DeviceID not found!")
                print("Disabling AutoStart")
                self.autoStart = False
            if(matchingComPortIndex >= 0):
                self.cb_COMPorts.setCurrentIndex(matchingComPortIndex)
            else:
                print("Error, Camera COM Port not found!")
                print("Disabling AutoStart")
                self.autoStart = False

            supportedSPF = self.config["ALLSKY"]["Framerates"].split(",")
            selectedSPF = self.config["ALLSKY"].getint("DefaultFrameRateIndex")
            self.cb_SupportedSPF.addItems(supportedSPF)
            if(len(supportedSPF) > 0 and len(supportedSPF) > selectedSPF):
                self.cb_SupportedSPF.setCurrentIndex(selectedSPF)
            self.cb_SupportedSPF.currentTextChanged.connect(self.cb_SupportedSPF_TextChanged)

            self.button_StartWeatherObs.clicked.connect(self.button_StartWeatherObs_clicked)
            self.startedVideoThread = False
            self.isNightMode = False
            self.saveImageDataBasePath = self.config["ALLSKY"]["ImageSavePath"]

            if(self.config["ALLSKY"].getboolean("SupportsNightMode")):
                Configuration.day_settings = self.config["ALLSKY"]["DayModeCommands"].split(",")
                Configuration.night_settings = self.config["ALLSKY"]["NightModeCommands"].split(",")
                Configuration.time_between_commands = self.config["ALLSKY"].getfloat("TimeBetweenCommands")
                self.button_ForceCameraMode.clicked.connect(self.button_ForceCameraMode_clicked)
            else:
                self.button_ForceCameraMode.setVisible(False)

            if(self.config["BOLTWOOD"].getboolean("BoltwoodEnabled")):
                
                self.CloudLevelStrEnabled = self.config["BOLTWOOD"].getboolean("CloudLevelStrEnabled")
                self.WindLevelStrEnabled = self.config["BOLTWOOD"].getboolean("WindLevelStrEnabled")
                self.HumidityLevelStrEnabled = self.config["BOLTWOOD"].getboolean("HumidityLevelStrEnabled")
                self.DaylightLevelStrEnabled = self.config["BOLTWOOD"].getboolean("DaylightLevelStrEnabled")
                self.RainIndicatorEnabled = self.config["BOLTWOOD"].getboolean("RainIndicatorEnabled")
                self.WetIndicatorEnabled = self.config["BOLTWOOD"].getboolean("WetIndicatorEnabled")
                self.SkyAmbTempEnabled = self.config["BOLTWOOD"].getboolean("SkyAmbTempEnabled")
                self.AmbientTempEnabled = self.config["BOLTWOOD"].getboolean("AmbientTempEnabled")
                self.SensorTempEnabled = self.config["BOLTWOOD"].getboolean("SensorTempEnabled")
                self.RainHeaterEnabled = self.config["BOLTWOOD"].getboolean("RainHeaterEnabled")
                self.WindSpeedEnabled = self.config["BOLTWOOD"].getboolean("WindSpeedEnabled")
                self.HumidityEnabled = self.config["BOLTWOOD"].getboolean("HumidityEnabled")
                self.DewPointEnabled = self.config["BOLTWOOD"].getboolean("DewPointEnabled")
                self.DaylightEnabled = self.config["BOLTWOOD"].getboolean("DaylightEnabled")

                if(not self.CloudLevelStrEnabled):
                    self.lb_CloudLevelString.setVisible(False)
                if(not self.WindLevelStrEnabled):
                    self.lb_WindSpeedLevelString.setVisible(False)
            
                if(not self.HumidityLevelStrEnabled):
                    self.lb_HumidityString.setVisible(False)
            
                if(not self.DaylightLevelStrEnabled):
                    self.lb_DaylightString.setVisible(False)

                if(not self.RainIndicatorEnabled):
                    self.lb_RainIndicator.setVisible(False)
                    self.label_17.setVisible(False)
            
                if(not self.WetIndicatorEnabled):
                    self.lb_WetIndicator.setVisible(False)
                    self.label_12.setVisible(False)
        
                if(not self.SkyAmbTempEnabled):
                    self.lb_SkyAmbTemp.setVisible(False)
                    self.label_10.setVisible(False)
                if(not self.AmbientTempEnabled):
                    self.lb_AmbientTemp.setVisible(False)
                    self.label_11.setVisible(False)
                if(not self.SensorTempEnabled):
                    self.lb_SensorTemp.setVisible(False)
                    self.label_13.setVisible(False)
                if(not self.RainHeaterEnabled):
                    self.lb_RainHeater.setVisible(False)
                    self.label_14.setVisible(False)
                if(not self.WindSpeedEnabled):
                    self.lb_WindSpeed.setVisible(False)
                    self.label_9.setVisible(False)
                if(not self.HumidityEnabled):
                    self.lb_Humidity.setVisible(False)
                    self.label_16.setVisible(False)
                if(not self.DewPointEnabled):
                    self.lb_DewPoint.setVisible(False)
                    self.label_18.setVisible(False)
                if(not self.DaylightEnabled):
                    self.lb_Daylight.setVisible(False)
                    self.label_20.setVisible(False)

                self.resetDBAvgValues()
                self.connectToDB()
                self.startedWeatherDataThread = False
                self.weatherDataThread = WeatherDataThread(self.config)
                self.weatherDataThread.updateWeatherDataSignal.connect(self.updateWeatherData)
                if(self.config["BOLTWOOD"].getboolean("AutoStart")):
                    self.lastWeatherDataUpdate = datetime.datetime.utcnow()
                    self.weatherDataThread.start()
            else:
                self.groupBox_3.setVisible(False)
        except Exception as e:
            print("Failed to configure AllSky")
            traceback.print_exc()

    def connectToDB(self):
        if(self.config["BOLTWOOD"]["DataBaseHost"]
           and self.config["BOLTWOOD"]["DataBaseName"]
           and self.config["BOLTWOOD"]["DataBaseUser"]
           and self.config["BOLTWOOD"]["DataBasePW"]):
            try:
                self.dbCon = mysql.connector.connect(host=self.config["BOLTWOOD"]["DataBaseHost"],
                                                     user=self.config["BOLTWOOD"]["DataBaseUser"],
                                                     password=self.config["BOLTWOOD"]["DataBasePW"],
                                                     database=self.config["BOLTWOOD"]["DataBaseName"])
            except Exception as e:
                print("Could not connect to database")
                print(e)
                traceback.print_exc()
                self.dbCon = None
        else:
            self.dbCon = None

    def resetDBAvgValues(self):
        self.Trelsky=[]
        self.Tambient=[]
        self.Tsensor=[]
        self.wind=[]
        self.humidity=[]
        self.dewpt=[]
        self.daylight=[]
        self.Frain=[]
        self.Fwet=[]
        self.heater=[]
        self.timeok=[]

    def updateWeatherData(self, data):
        if(data is None):
            return
        
        currentWeatherDataUpdate = datetime.datetime.utcnow()

        dbComlumnsString = list()
        dbValues = list()

        if(self.CloudLevelStrEnabled):
            cloudCond = int(data[WeatherDataThread.CLOUD_COND_STR])
            cloudStr, cloudColor = self.weatherDataThread.getCloudConditionString(cloudCond)
            self.lb_CloudLevelString.setText(cloudStr)
            self.lb_CloudLevelString.setStyleSheet("color: " + cloudColor)
            
        if(self.WindLevelStrEnabled):
            windCond = int(data[WeatherDataThread.WIND_COND_STR])
            windStr, windColor = self.weatherDataThread.getWindConditionString(windCond)
            self.lb_WindSpeedLevelString.setText(windStr)
            self.lb_WindSpeedLevelString.setStyleSheet("color: " + windColor)
            
        if(self.HumidityLevelStrEnabled):
            rainCond = int(data[WeatherDataThread.RAIN_COND_STR])
            rainStr, rainColor = self.weatherDataThread.getRainConditionString(rainCond)
            self.lb_HumidityString.setText(rainStr)
            self.lb_HumidityString.setStyleSheet("color: " + rainColor)
            
        if(self.DaylightLevelStrEnabled):
            dayCond = int(data[WeatherDataThread.DAY_COND_STR])
            dayStr, dayColor = self.weatherDataThread.getDayConditionString(dayCond)
            self.lb_DaylightString.setText(dayStr)
            self.lb_DaylightString.setStyleSheet("color: " + dayColor)

        if(self.RainIndicatorEnabled):
            rainF = bool(data[WeatherDataThread.RAIN_F_STR])
            rainFIcon, rainFColor = self.weatherDataThread.getRainIcon(rainF)
            self.lb_RainIndicator.setText(rainFIcon)
            self.lb_RainIndicator.setStyleSheet("color: " + rainFColor)
            self.Frain.append(data[WeatherDataThread.RAIN_F_STR])
            dbComlumnsString.append("Rain")
            dbValues.append(np.any(self.Frain))
            
        if(self.WetIndicatorEnabled):
            wetF = bool(data[WeatherDataThread.WET_F_STR])
            wetFIcon, wetFColor = self.weatherDataThread.getWetIcon(wetF)
            self.lb_WetIndicator.setText(wetFIcon)
            self.lb_WetIndicator.setStyleSheet("color: " + wetFColor)
            self.Fwet.append(data[WeatherDataThread.WET_F_STR])
            dbComlumnsString.append("Wet")
            dbValues.append(np.any(self.Fwet))
        
        if(self.SkyAmbTempEnabled):
            self.lb_SkyAmbTemp.setText(str(data[WeatherDataThread.REL_SKY_TEMP_STR]))
            self.Trelsky.append(data[WeatherDataThread.REL_SKY_TEMP_STR])
            dbComlumnsString.append("Trelsky")
            dbValues.append(np.mean(self.Trelsky))
        if(self.AmbientTempEnabled):
            self.lb_AmbientTemp.setText(str(data[WeatherDataThread.AMBIENT_TEMP_STR]))
            self.Tambient.append(data[WeatherDataThread.REL_SKY_TEMP_STR])
            dbComlumnsString.append("Tambient")
            dbValues.append(np.mean(self.Tambient))
        if(self.SensorTempEnabled):
            self.lb_SensorTemp.setText(str(data[WeatherDataThread.SENSOR_TEMP_STR]))
            self.Tsensor.append(data[WeatherDataThread.REL_SKY_TEMP_STR])
            dbComlumnsString.append("Tsensor")
            dbValues.append(np.mean(self.Tsensor))
        if(self.RainHeaterEnabled):
            self.lb_RainHeater.setText(str(data[WeatherDataThread.HEATER_STR]))
            self.heater.append(data[WeatherDataThread.REL_SKY_TEMP_STR])
            dbComlumnsString.append("Heater")
            dbValues.append(np.mean(self.heater))
        if(self.WindSpeedEnabled):
            self.lb_WindSpeed.setText(str(data[WeatherDataThread.WIND_STR]))
            self.wind.append(data[WeatherDataThread.REL_SKY_TEMP_STR])
            dbComlumnsString.append("Wind")
            dbValues.append(np.mean(self.wind))
            dbComlumnsString.append("WindMax")
            dbValues.append(np.max(self.wind))
        if(self.HumidityEnabled):
            self.lb_Humidity.setText(str(data[WeatherDataThread.HUMIDITY_STR]))
            self.humidity.append(data[WeatherDataThread.REL_SKY_TEMP_STR])
            dbComlumnsString.append("Humidity")
            dbValues.append(np.mean(self.humidity))
        if(self.DewPointEnabled):
            self.lb_DewPoint.setText(str(data[WeatherDataThread.DEW_POINT_STR]))
            self.dewpt.append(data[WeatherDataThread.REL_SKY_TEMP_STR])
            dbComlumnsString.append("DewPoint")
            dbValues.append(np.mean(self.dewpt))
        if(self.DaylightEnabled):
            self.lb_Daylight.setText(str(data[WeatherDataThread.DAYLIGHT_STR]))
            self.daylight.append(data[WeatherDataThread.REL_SKY_TEMP_STR])
            dbComlumnsString.append("Daylight")
            dbValues.append(np.mean(self.daylight))

        self.lb_LastWeatherUpdate.setText(str(data[WeatherDataThread.LAST_TIME_OK_STR]))
        self.timeok.append(data[WeatherDataThread.REL_SKY_TEMP_STR])
        dbComlumnsString.append("Rain")
        dbValues.append(np.mean(self.timeok))

        if(currentWeatherDataUpdate - self.lastWeatherDataUpdate > datetime.timedelta(seconds=59)
           and self.dbCon is not None):
            dbComlumnsString.append("date")
            dbValues.append(str(currentWeatherDataUpdate))
            sqlString = "INSERT INTO boltwood (" + ",".join(dbComlumnsString) + ") VALUES (" + ",".join(dbValues) + ")"

            dbCursor = self.dbCon.cursor()
            dbCursor.execute(sqlString)
            self.dbCon.commit()

            self.resetDBAvgValues()
        self.lastWeatherDataUpdate = currentWeatherDataUpdate

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

            self.videoThread = VideoThread(camPort=camPort, spf=fps, config=self.config)
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
