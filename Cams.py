import sys, os
from PyQt5 import QtWidgets

from ASICam import ASICamWindow
from AllSkyWeather import AllSkyWeatherWindow
from Watec import WatecWindow

if(not os.path.exists("dataset")):
    os.mkdir("dataset")
app = QtWidgets.QApplication(sys.argv)
asiWindow = ASICamWindow()
asiWindow.show()
aswWindow = AllSkyWeatherWindow()
aswWindow.show()
#watecWindow = WatecWindow()
#watecWindow.show()
app.exec()