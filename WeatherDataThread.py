from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import time as t
from astropy.time import Time
import astropy.units as u
import win32com.client as com
from typing import Final
import os

class WeatherDataThread(QThread):
    updateWeatherDataSignal = pyqtSignal(object)

    REL_SKY_TEMP_STR: Final[str] = "RelSkyTemp"
    AMBIENT_TEMP_STR: Final[str] = "AmbientTemp"
    SENSOR_TEMP_STR: Final[str] = "SensorTemp"
    WIND_STR: Final[str] = "Wind"
    HUMIDITY_STR: Final[str] = "Humidity"
    DEW_POINT_STR: Final[str] = "DewPoint"
    DAYLIGHT_STR: Final[str] = "Daylight"
    RAIN_F_STR: Final[str] = "RainF"
    WET_F_STR: Final[str] = "WetF"
    HEATER_STR: Final[str] = "Heater"
    LAST_TIME_OK_STR: Final[str] = "timeok"

    CLOUD_COND_STR: Final[str] = "CloudCond"
    WIND_COND_STR: Final[str] = "WindCond"
    RAIN_COND_STR: Final[str] = "RainCond"
    DAY_COND_STR: Final[str] = "DayCond"

    def __init__(self, config):
        super().__init__()
        self.config = config

    def getCloudConditionString(self, condition: int):
        match condition:
            case 1:
                retString = "Clear"
                retColor = "green"
            case 2:
                retString = "Cloudy"
                retColor = "yellow"
            case 3:
                retString = "Very Cloudy"
                retColor = "orange"
            case _:
                retString = "unknown"
                retColor = "red"
        return retString, retColor

    def getWindConditionString(self, condition: int):
        match condition:
            case 1:
                retString = "Calm"
                retColor = "green"
            case 2:
                retString = "Windy"
                retColor = "yellow"
            case 3:
                retString = "Very Windy"
                retColor = "orange"
            case _:
                retString = "unknown"
                retColor = "red"
        return retString, retColor

    def getRainConditionString(self, condition: int):
        match condition:
            case 1:
                retString = "Dry"
                retColor = "green"
            case 2:
                retString = "Wet"
                retColor = "orange"
            case 3:
                retString = "Rain"
                retColor = "red"
            case _:
                retString = "unknown"
                retColor = "red"
        return retString, retColor

    def getDayConditionString(self, condition: int):
        match condition:
            case 1:
                retString = "Dark"
                retColor = "green"
            case 2:
                retString = "Light"
                retColor = "green"
            case 3:
                retString = "Very Light"
                retColor = "green"
            case _:
                retString = "unknown"
                retColor = "red"
        return retString, retColor

    def getRainIcon(self, condition: bool):
        retColor = "black"
        retIcon = "\u25cb"
        if(condition):
            retColor = "dark blue"
            retIcon = "\u23fa"

        return retIcon, retColor

    def getWetIcon(self, condition: bool):
        retColor = "black"
        retIcon = "\u25fb"
        if(condition):
            retColor = "blue"
            retIcon = "\u25fc"

        return retIcon, retColor

    def run(self):
        self._run_flag = True
        if(not os.path.isfile(self.config["BOLTWOOD"]["BoltwoodClarityIIInstallPath"])):
            print("Clarity II not found! Install it to get Boltwood data")
        else:
            self.cloud = com.gencache.EnsureDispatch("ClarityII.CloudSensorII")
            CloudLevelStrEnabled = self.config["BOLTWOOD"].getboolean("CloudLevelStrEnabled")
            WindLevelStrEnabled = self.config["BOLTWOOD"].getboolean("WindLevelStrEnabled")
            HumidityLevelStrEnabled = self.config["BOLTWOOD"].getboolean("HumidityLevelStrEnabled")
            DaylightLevelStrEnabled = self.config["BOLTWOOD"].getboolean("DaylightLevelStrEnabled")
            RainIndicatorEnabled = self.config["BOLTWOOD"].getboolean("RainIndicatorEnabled")
            WetIndicatorEnabled = self.config["BOLTWOOD"].getboolean("WetIndicatorEnabled")
            SkyAmbTempEnabled = self.config["BOLTWOOD"].getboolean("SkyAmbTempEnabled")
            AmbientTempEnabled = self.config["BOLTWOOD"].getboolean("AmbientTempEnabled")
            SensorTempEnabled = self.config["BOLTWOOD"].getboolean("SensorTempEnabled")
            RainHeaterEnabled = self.config["BOLTWOOD"].getboolean("RainHeaterEnabled")
            WindSpeedEnabled = self.config["BOLTWOOD"].getboolean("WindSpeedEnabled")
            HumidityEnabled = self.config["BOLTWOOD"].getboolean("HumidityEnabled")
            DewPointEnabled = self.config["BOLTWOOD"].getboolean("DewPointEnabled")
            DaylightEnabled = self.config["BOLTWOOD"].getboolean("DaylightEnabled")
            lastTime = Time.now()
            while self._run_flag:
                if(self.cloud is not None):
                    data = {}
                    if(SkyAmbTempEnabled):
                        data[WeatherDataThread.REL_SKY_TEMP_STR] = self.cloud.RelSkyT
                    if(AmbientTempEnabled):
                        data[WeatherDataThread.AMBIENT_TEMP_STR] = self.cloud.AmbientT
                    if(SensorTempEnabled):
                        data[WeatherDataThread.SENSOR_TEMP_STR] = self.cloud.SensorT
                    if(WindSpeedEnabled):
                        data[WeatherDataThread.WIND_STR] = self.cloud.Wind
                    if(HumidityEnabled):
                        data[WeatherDataThread.HUMIDITY_STR] = self.cloud.HumidityPercent
                    if(DewPointEnabled):
                        data[WeatherDataThread.DEW_POINT_STR] = self.cloud.DewPointT
                    if(DaylightEnabled):
                        data[WeatherDataThread.DAYLIGHT_STR] = self.cloud.DayLightV
                    if(RainIndicatorEnabled):
                        data[WeatherDataThread.RAIN_F_STR] = self.cloud.RainF
                    if(WetIndicatorEnabled):
                        data[WeatherDataThread.WET_F_STR] = self.cloud.WetF
                    if(RainHeaterEnabled):
                        data[WeatherDataThread.HEATER_STR] = self.cloud.HeaterPercent
                    if(CloudLevelStrEnabled):
                         data[WeatherDataThread.CLOUD_COND_STR] = self.cloud.CloudCondition
                    if(WindLevelStrEnabled):
                        data[WeatherDataThread.WIND_COND_STR] = self.cloud.WindCondition
                    if(HumidityLevelStrEnabled):
                        data[WeatherDataThread.RAIN_COND_STR] = self.cloud.RainCondition
                    if(DaylightLevelStrEnabled):
                        data[WeatherDataThread.DAY_COND_STR] = self.cloud.DayCondition
                
                    data[WeatherDataThread.LAST_TIME_OK_STR] = self.cloud.SecondsSinceGoodData
                    self.updateWeatherDataSignal.emit(data)
                t.sleep(1)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()