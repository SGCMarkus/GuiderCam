# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ASICamUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ASICam(object):
    def setupUi(self, ASICam):
        ASICam.setObjectName("ASICam")
        ASICam.resize(932, 775)
        self.centralwidget = QtWidgets.QWidget(ASICam)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.hl_GuiderCam = QtWidgets.QHBoxLayout()
        self.hl_GuiderCam.setObjectName("hl_GuiderCam")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.checkBox_startSeries = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_startSeries.setObjectName("checkBox_startSeries")
        self.horizontalLayout_6.addWidget(self.checkBox_startSeries, 0, QtCore.Qt.AlignLeft)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5, 0, QtCore.Qt.AlignLeft)
        self.lineEdit_seriesNumber = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_seriesNumber.sizePolicy().hasHeightForWidth())
        self.lineEdit_seriesNumber.setSizePolicy(sizePolicy)
        self.lineEdit_seriesNumber.setObjectName("lineEdit_seriesNumber")
        self.horizontalLayout_6.addWidget(self.lineEdit_seriesNumber, 0, QtCore.Qt.AlignLeft)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.button_startSeries = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_startSeries.sizePolicy().hasHeightForWidth())
        self.button_startSeries.setSizePolicy(sizePolicy)
        self.button_startSeries.setObjectName("button_startSeries")
        self.horizontalLayout_6.addWidget(self.button_startSeries, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.gridLayout_2.addLayout(self.verticalLayout, 8, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.vertLayoutHistogram = QtWidgets.QVBoxLayout()
        self.vertLayoutHistogram.setObjectName("vertLayoutHistogram")
        self.horizontalLayout_7.addLayout(self.vertLayoutHistogram)
        self.gridLayout_2.addLayout(self.horizontalLayout_7, 3, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label, 0, QtCore.Qt.AlignLeft)
        self.spinBox_Gain = QtWidgets.QSpinBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_Gain.sizePolicy().hasHeightForWidth())
        self.spinBox_Gain.setSizePolicy(sizePolicy)
        self.spinBox_Gain.setMinimum(0)
        self.spinBox_Gain.setMaximum(1000)
        self.spinBox_Gain.setProperty("value", 10)
        self.spinBox_Gain.setObjectName("spinBox_Gain")
        self.horizontalLayout_5.addWidget(self.spinBox_Gain, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.slider_Gain = QtWidgets.QSlider(self.groupBox)
        self.slider_Gain.setMaximum(1000)
        self.slider_Gain.setProperty("value", 10)
        self.slider_Gain.setOrientation(QtCore.Qt.Horizontal)
        self.slider_Gain.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider_Gain.setTickInterval(10)
        self.slider_Gain.setObjectName("slider_Gain")
        self.verticalLayout_4.addWidget(self.slider_Gain)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 5, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_IP_Port = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_IP_Port.sizePolicy().hasHeightForWidth())
        self.lineEdit_IP_Port.setSizePolicy(sizePolicy)
        self.lineEdit_IP_Port.setInputMask("")
        self.lineEdit_IP_Port.setText("")
        self.lineEdit_IP_Port.setObjectName("lineEdit_IP_Port")
        self.horizontalLayout_3.addWidget(self.lineEdit_IP_Port)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.lineEdit_DeviceID = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_DeviceID.sizePolicy().hasHeightForWidth())
        self.lineEdit_DeviceID.setSizePolicy(sizePolicy)
        self.lineEdit_DeviceID.setInputMask("")
        self.lineEdit_DeviceID.setObjectName("lineEdit_DeviceID")
        self.horizontalLayout_3.addWidget(self.lineEdit_DeviceID)
        self.button_connect = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_connect.sizePolicy().hasHeightForWidth())
        self.button_connect.setSizePolicy(sizePolicy)
        self.button_connect.setObjectName("button_connect")
        self.horizontalLayout_3.addWidget(self.button_connect)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.vertLayoutMatplotlib = QtWidgets.QVBoxLayout()
        self.vertLayoutMatplotlib.setObjectName("vertLayoutMatplotlib")
        self.gridLayout_2.addLayout(self.vertLayoutMatplotlib, 1, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label1 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label1.sizePolicy().hasHeightForWidth())
        self.label1.setSizePolicy(sizePolicy)
        self.label1.setObjectName("label1")
        self.horizontalLayout_4.addWidget(self.label1, 0, QtCore.Qt.AlignLeft)
        self.spinBox_ExposureTime = QtWidgets.QDoubleSpinBox(self.groupBox)
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
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setIndent(-1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2, 0, QtCore.Qt.AlignLeft)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.slider_ExposureTime = QtWidgets.QSlider(self.groupBox)
        self.slider_ExposureTime.setMaximum(120)
        self.slider_ExposureTime.setProperty("value", 1)
        self.slider_ExposureTime.setOrientation(QtCore.Qt.Horizontal)
        self.slider_ExposureTime.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider_ExposureTime.setTickInterval(1)
        self.slider_ExposureTime.setObjectName("slider_ExposureTime")
        self.verticalLayout_3.addWidget(self.slider_ExposureTime)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 4, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 2, 0, 1, 1)
        self.hl_GuiderCam.addLayout(self.gridLayout_2)
        self.gridLayout_3.addLayout(self.hl_GuiderCam, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox)
        ASICam.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ASICam)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 932, 21))
        self.menubar.setObjectName("menubar")
        ASICam.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ASICam)
        self.statusbar.setObjectName("statusbar")
        ASICam.setStatusBar(self.statusbar)

        self.retranslateUi(ASICam)
        QtCore.QMetaObject.connectSlotsByName(ASICam)
        ASICam.setTabOrder(self.lineEdit_IP_Port, self.lineEdit_DeviceID)
        ASICam.setTabOrder(self.lineEdit_DeviceID, self.button_connect)
        ASICam.setTabOrder(self.button_connect, self.spinBox_ExposureTime)
        ASICam.setTabOrder(self.spinBox_ExposureTime, self.slider_ExposureTime)
        ASICam.setTabOrder(self.slider_ExposureTime, self.spinBox_Gain)
        ASICam.setTabOrder(self.spinBox_Gain, self.slider_Gain)
        ASICam.setTabOrder(self.slider_Gain, self.checkBox_startSeries)
        ASICam.setTabOrder(self.checkBox_startSeries, self.lineEdit_seriesNumber)
        ASICam.setTabOrder(self.lineEdit_seriesNumber, self.button_startSeries)

    def retranslateUi(self, ASICam):
        _translate = QtCore.QCoreApplication.translate
        ASICam.setWindowTitle(_translate("ASICam", "Cams"))
        self.groupBox.setTitle(_translate("ASICam", "ASI178"))
        self.checkBox_startSeries.setText(_translate("ASICam", "Start series"))
        self.label_5.setText(_translate("ASICam", "Series amount (0 = till stopped): "))
        self.button_startSeries.setText(_translate("ASICam", "Take Image"))
        self.label.setText(_translate("ASICam", "Gain: "))
        self.label_3.setText(_translate("ASICam", "Server IP:Port: "))
        self.label_4.setText(_translate("ASICam", "Device ID: "))
        self.button_connect.setText(_translate("ASICam", "Connect"))
        self.label1.setText(_translate("ASICam", "Exposure time:"))
        self.label_2.setText(_translate("ASICam", "s"))
