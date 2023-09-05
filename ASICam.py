from matplotlib.figure import Figure

from PyQt5 import QtWidgets, QtCore

from matplotlib.backends.backend_qtagg import (
     FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from ASICamUI import Ui_ASICam
from QtRangeSlider import RangeSlider

from alpaca.camera import Camera
from ciboulette.base import ciboulette
from ciboulette.utils import exposure
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
import numpy as np

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
        self.curFig.subplots_adjust(left=0, right=0.999, top=0.999, bottom=0)
        self.curFigAxis = self.curFig.add_subplot()

        fc = FigureCanvas(self.curFig)
        toolbar = NavigationToolbar(fc, self)
        self.vertLayoutMatplotlib.addWidget(toolbar)
        self.vertLayoutMatplotlib.addWidget(fc)

        self.curHistogram = Figure(figsize=(1, 30))
        self.curHistogram.subplots_adjust(left=0, right=0.999, top=0.999, bottom=0)
        self.curHistogramAxis = self.curHistogram.add_subplot()
        self.curHistogramAxis.margins(x=0, y=0)
        fc2 = FigureCanvas(self.curHistogram)
        fc2.setMinimumSize(0, 100)
        fc2.setMaximumSize(10000, 100)
        self.vertLayoutHistogram.addWidget(fc2)
        self.histgramRangeSlider = RangeSlider(QtCore.Qt.Horizontal)
        self.histgramRangeSlider.setMinimumHeight(30)
        self.histgramRangeSlider.setMinimum(0)
        self.histgramRangeSlider.setMaximum(65535)
        self.histgramRangeSlider.setLow(0)
        self.histgramRangeSlider.setHigh(65535)
        self.histgramRangeSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.histgramRangeSlider.sliderMoved.connect(self.histogramRangeSlider_sliderMoved)
        self.vertLayoutHistogram.addWidget(self.histgramRangeSlider)

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

    def histogramRangeSlider_sliderMoved(self, lowVal, highVal):
        if(self.currentImage is None):
            return
        
        self.curFigImage.norm.autoscale([lowVal, highVal])
        self.curFig.canvas.draw_idle()

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

    def plotImage(self, image, minVal, maxVal):
        self.curFigAxis.clear()
        self.curFigImage = self.curFigAxis.imshow(image, origin='lower', cmap='gray', vmin=minVal, vmax=maxVal)            
        self.curFig.canvas.draw_idle()
        
        self.curHistogramAxis.clear()
        histogram, binEdges = np.histogram(image, bins=1024, range=(0, 65535))
        self.curHistogramAxis.plot(binEdges[0:-1], histogram)
        self.curHistogram.canvas.draw_idle()


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
            self.currentImage = image_data
            self.plotImage(image_data, self.histgramRangeSlider.low(), self.histgramRangeSlider.high())
            
