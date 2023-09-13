import sys, os
from PyQt5 import QtWidgets

import configparser

from ASICam import ASICamWindow
from AllSkyWeather import AllSkyWeatherWindow
from Watec import WatecWindow

if __name__ == '__main__':
    useASI = False
    useWATEC = False
    useAllSky = False
    configFile = "template_config.conf"
    
    if(len(sys.argv) > 0):
        args = sys.argv[1:]
        #print(args)
        for i, arg in enumerate(args):
            match(arg):
                case "--use_asi":
                    useASI = True
                case "--use_watec":
                    useWATEC = True
                case "--useAllSky":
                    useAllSky = True
                case "--config":
                    try:
                        filename = args[i+1]
                        if(os.path.isfile(filename)):
                            configFile = filename
                        else: 
                            print("Specified config " + filename + " does not exist")
                            quit()
                    except Exception as e:
                        print(e)
                        quit()
    else:
        useASI = True
        useWATEC = True
        useAllSky = True

    if(not os.path.exists("dataset")):
        os.mkdir("dataset")
    app = QtWidgets.QApplication(sys.argv)

    configp = configparser.ConfigParser()
    configp.read(configFile)
    if(useASI):
        asiWindow = ASICamWindow(config=configp)
        asiWindow.show()
    if(useAllSky):
        aswWindow = AllSkyWeatherWindow(config=configp)
        aswWindow.show()
    if(useWATEC):
        watecWindow = WatecWindow(config=configp)
        watecWindow.show()
    if(useASI or useAllSky or useWATEC):
        app.exec()