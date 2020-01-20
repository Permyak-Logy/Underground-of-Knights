# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingsFrom.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(210, 227)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        MainWindow.setFont(font)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_music = QtWidgets.QLabel(self.centralwidget)
        self.label_music.setObjectName("label_music")
        self.gridLayout.addWidget(self.label_music, 1, 0, 1, 1)
        self.label_matrix = QtWidgets.QLabel(self.centralwidget)
        self.label_matrix.setObjectName("label_matrix")
        self.gridLayout.addWidget(self.label_matrix, 2, 0, 1, 1)
        self.spinBoxX = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBoxX.setMinimum(800)
        self.spinBoxX.setMaximum(1920)
        self.spinBoxX.setSingleStep(10)
        self.spinBoxX.setProperty("value", 1920)
        self.spinBoxX.setObjectName("spinBoxX")
        self.gridLayout.addWidget(self.spinBoxX, 2, 1, 1, 1)
        self.spinBoxY = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBoxY.setMinimum(600)
        self.spinBoxY.setMaximum(1080)
        self.spinBoxY.setSingleStep(10)
        self.spinBoxY.setProperty("value", 1080)
        self.spinBoxY.setObjectName("spinBoxY")
        self.gridLayout.addWidget(self.spinBoxY, 2, 2, 1, 1)
        self.slider_volume_music = QtWidgets.QSlider(self.centralwidget)
        self.slider_volume_music.setMaximum(100)
        self.slider_volume_music.setProperty("value", 10)
        self.slider_volume_music.setOrientation(QtCore.Qt.Horizontal)
        self.slider_volume_music.setObjectName("slider_volume_music")
        self.gridLayout.addWidget(self.slider_volume_music, 1, 1, 1, 2)
        self.btn_close = QtWidgets.QPushButton(self.centralwidget)
        self.btn_close.setObjectName("btn_close")
        self.gridLayout.addWidget(self.btn_close, 4, 2, 1, 1)
        self.btn_save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_save.setObjectName("btn_save")
        self.gridLayout.addWidget(self.btn_save, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.checkBoxFullScreen = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxFullScreen.setChecked(True)
        self.checkBoxFullScreen.setTristate(False)
        self.checkBoxFullScreen.setObjectName("checkBoxFullScreen")
        self.gridLayout.addWidget(self.checkBoxFullScreen, 3, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 210, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Settings Game"))
        self.label_music.setText(_translate("MainWindow", "Music .o0"))
        self.label_matrix.setText(_translate("MainWindow", "Matrix (x, y)"))
        self.btn_close.setText(_translate("MainWindow", "cancel"))
        self.btn_save.setText(_translate("MainWindow", "save"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; font-style:italic;\">Настройки вступают в силу<br/>после перезапуска игры</span></p></body></html>"))
        self.checkBoxFullScreen.setText(_translate("MainWindow", "Full screen"))
