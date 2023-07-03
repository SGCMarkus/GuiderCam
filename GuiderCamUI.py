# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guidercam.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GuiderCam(object):
    def setupUi(self, GuiderCam):
        GuiderCam.setObjectName("GuiderCam")
        GuiderCam.resize(1212, 736)
        self.centralwidget = QtWidgets.QWidget(GuiderCam)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.vertLayoutMatplotlib = QtWidgets.QVBoxLayout()
        self.vertLayoutMatplotlib.setObjectName("vertLayoutMatplotlib")
        self.horizontalLayout.addLayout(self.vertLayoutMatplotlib)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label, 0, QtCore.Qt.AlignLeft)
        self.spinBox_Gain = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_Gain.sizePolicy().hasHeightForWidth())
        self.spinBox_Gain.setSizePolicy(sizePolicy)
        self.spinBox_Gain.setMinimum(1)
        self.spinBox_Gain.setMaximum(1000)
        self.spinBox_Gain.setProperty("value", 10)
        self.spinBox_Gain.setObjectName("spinBox_Gain")
        self.horizontalLayout_5.addWidget(self.spinBox_Gain, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.slider_Gain = QtWidgets.QSlider(self.centralwidget)
        self.slider_Gain.setMaximum(1000)
        self.slider_Gain.setProperty("value", 10)
        self.slider_Gain.setOrientation(QtCore.Qt.Horizontal)
        self.slider_Gain.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider_Gain.setTickInterval(10)
        self.slider_Gain.setObjectName("slider_Gain")
        self.verticalLayout_4.addWidget(self.slider_Gain)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 7, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_IP_Port = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_IP_Port.sizePolicy().hasHeightForWidth())
        self.lineEdit_IP_Port.setSizePolicy(sizePolicy)
        self.lineEdit_IP_Port.setInputMask("")
        self.lineEdit_IP_Port.setText("")
        self.lineEdit_IP_Port.setObjectName("lineEdit_IP_Port")
        self.horizontalLayout_3.addWidget(self.lineEdit_IP_Port)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.lineEdit_DeviceID = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_DeviceID.sizePolicy().hasHeightForWidth())
        self.lineEdit_DeviceID.setSizePolicy(sizePolicy)
        self.lineEdit_DeviceID.setInputMask("")
        self.lineEdit_DeviceID.setObjectName("lineEdit_DeviceID")
        self.horizontalLayout_3.addWidget(self.lineEdit_DeviceID)
        self.button_connect = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_connect.sizePolicy().hasHeightForWidth())
        self.button_connect.setSizePolicy(sizePolicy)
        self.button_connect.setObjectName("button_connect")
        self.horizontalLayout_3.addWidget(self.button_connect)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label1.sizePolicy().hasHeightForWidth())
        self.label1.setSizePolicy(sizePolicy)
        self.label1.setObjectName("label1")
        self.horizontalLayout_4.addWidget(self.label1, 0, QtCore.Qt.AlignLeft)
        self.spinBox_ExposureTime = QtWidgets.QDoubleSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_ExposureTime.sizePolicy().hasHeightForWidth())
        self.spinBox_ExposureTime.setSizePolicy(sizePolicy)
        self.spinBox_ExposureTime.setDecimals(3)
        self.spinBox_ExposureTime.setMaximum(120.0)
        self.spinBox_ExposureTime.setSingleStep(0.1)
        self.spinBox_ExposureTime.setProperty("value", 1.0)
        self.spinBox_ExposureTime.setObjectName("spinBox_ExposureTime")
        self.horizontalLayout_4.addWidget(self.spinBox_ExposureTime, 0, QtCore.Qt.AlignLeft)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setIndent(-1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2, 0, QtCore.Qt.AlignLeft)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.slider_ExposureTime = QtWidgets.QSlider(self.centralwidget)
        self.slider_ExposureTime.setMaximum(120)
        self.slider_ExposureTime.setProperty("value", 1)
        self.slider_ExposureTime.setOrientation(QtCore.Qt.Horizontal)
        self.slider_ExposureTime.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider_ExposureTime.setTickInterval(1)
        self.slider_ExposureTime.setObjectName("slider_ExposureTime")
        self.verticalLayout_3.addWidget(self.slider_ExposureTime)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.checkBox_startSeries = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_startSeries.setObjectName("checkBox_startSeries")
        self.horizontalLayout_6.addWidget(self.checkBox_startSeries, 0, QtCore.Qt.AlignLeft)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5, 0, QtCore.Qt.AlignLeft)
        self.lineEdit_seriesNumber = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_seriesNumber.sizePolicy().hasHeightForWidth())
        self.lineEdit_seriesNumber.setSizePolicy(sizePolicy)
        self.lineEdit_seriesNumber.setObjectName("lineEdit_seriesNumber")
        self.horizontalLayout_6.addWidget(self.lineEdit_seriesNumber, 0, QtCore.Qt.AlignLeft)
        self.button_startSeries = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_startSeries.sizePolicy().hasHeightForWidth())
        self.button_startSeries.setSizePolicy(sizePolicy)
        self.button_startSeries.setObjectName("button_startSeries")
        self.horizontalLayout_6.addWidget(self.button_startSeries, 0, QtCore.Qt.AlignLeft)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.gridLayout_2.addLayout(self.verticalLayout, 5, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        GuiderCam.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(GuiderCam)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1212, 21))
        self.menubar.setObjectName("menubar")
        GuiderCam.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(GuiderCam)
        self.statusbar.setObjectName("statusbar")
        GuiderCam.setStatusBar(self.statusbar)

        self.retranslateUi(GuiderCam)
        QtCore.QMetaObject.connectSlotsByName(GuiderCam)

    def retranslateUi(self, GuiderCam):
        _translate = QtCore.QCoreApplication.translate
        GuiderCam.setWindowTitle(_translate("GuiderCam", "Guider Cam"))
        self.label.setText(_translate("GuiderCam", "Gain: "))
        self.label_3.setText(_translate("GuiderCam", "Server IP:Port: "))
        self.label_4.setText(_translate("GuiderCam", "Device ID: "))
        self.button_connect.setText(_translate("GuiderCam", "Connect"))
        self.label1.setText(_translate("GuiderCam", "Exposure time:"))
        self.label_2.setText(_translate("GuiderCam", "s"))
        self.checkBox_startSeries.setText(_translate("GuiderCam", "Start series"))
        self.label_5.setText(_translate("GuiderCam", "Series amount (0 = till stopped): "))
        self.button_startSeries.setText(_translate("GuiderCam", "Take Image"))
