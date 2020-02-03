# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingsFrom2.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(284, 185)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_music = QtWidgets.QLabel(self.centralwidget)
        self.label_music.setObjectName("label_music")
        self.gridLayout.addWidget(self.label_music, 0, 0, 1, 1)
        self.slider_volume_music = QtWidgets.QSlider(self.centralwidget)
        self.slider_volume_music.setMaximum(100)
        self.slider_volume_music.setOrientation(QtCore.Qt.Horizontal)
        self.slider_volume_music.setObjectName("slider_volume_music")
        self.gridLayout.addWidget(self.slider_volume_music, 0, 1, 1, 4)
        self.label_matrix = QtWidgets.QLabel(self.centralwidget)
        self.label_matrix.setObjectName("label_matrix")
        self.gridLayout.addWidget(self.label_matrix, 1, 0, 1, 3)
        self.spinBoxX = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBoxX.setMinimum(800)
        self.spinBoxX.setMaximum(1920)
        self.spinBoxX.setSingleStep(10)
        self.spinBoxX.setProperty("value", 800)
        self.spinBoxX.setObjectName("spinBoxX")
        self.gridLayout.addWidget(self.spinBoxX, 1, 3, 1, 1)
        self.spinBoxY = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBoxY.setMinimum(600)
        self.spinBoxY.setMaximum(1080)
        self.spinBoxY.setSingleStep(10)
        self.spinBoxY.setObjectName("spinBoxY")
        self.gridLayout.addWidget(self.spinBoxY, 1, 4, 1, 1)
        self.label_packege = QtWidgets.QLabel(self.centralwidget)
        self.label_packege.setObjectName("label_packege")
        self.gridLayout.addWidget(self.label_packege, 3, 0, 1, 2)
        self.btn_save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_save.setObjectName("btn_save")
        self.gridLayout.addWidget(self.btn_save, 4, 3, 1, 1)
        self.btn_close = QtWidgets.QPushButton(self.centralwidget)
        self.btn_close.setObjectName("btn_close")
        self.gridLayout.addWidget(self.btn_close, 4, 4, 1, 1)
        self.comboBoxPacheges = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxPacheges.setObjectName("comboBoxPacheges")
        self.gridLayout.addWidget(self.comboBoxPacheges, 3, 2, 1, 3)
        self.checkBoxFullScreen = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxFullScreen.setObjectName("checkBoxFullScreen")
        self.gridLayout.addWidget(self.checkBoxFullScreen, 2, 0, 1, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 284, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Settings"))
        self.label_music.setText(_translate("MainWindow", "Music .o0"))
        self.label_matrix.setText(_translate("MainWindow", "Matrix (width, height)"))
        self.label_packege.setText(_translate("MainWindow", "Packege"))
        self.btn_save.setText(_translate("MainWindow", "save"))
        self.btn_close.setText(_translate("MainWindow", "cancel"))
        self.checkBoxFullScreen.setText(_translate("MainWindow", "Full screen"))
