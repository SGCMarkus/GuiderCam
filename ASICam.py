from matplotlib.figure import Figure

from PyQt5 import QtWidgets

from matplotlib.backends.backend_qtagg import (
     FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from ASICamUI import Ui_ASICam

from alpaca.camera import Camera
from ciboulette.base import ciboulette
from ciboulette.utils import exposure
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits

class ASICamWindow(QtWidgets.QMainWindow, Ui_ASICam):

    def __init__(self, *args, obj=None, **kwargs):
        super(ASICamWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setup_ASICamUI()

    def setup_ASICamUI(self):
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

            expose,frameid,datatype = self.cibouletteClient.exposure
            image_file = get_pkg_data_filename('dataset/CAM1_INIT_' + str(frameid) + '.fits')
            image_data = fits.getdata(image_file, ext=0)
            self.curFigAxis.clear()
            self.curFigAxis.imshow(image_data, origin='lower', cmap='gray')
            self.curFig.canvas.draw_idle()
