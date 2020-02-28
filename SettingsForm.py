# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingsForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 360)
        MainWindow.setMinimumSize(QtCore.QSize(640, 360))
        MainWindow.setMaximumSize(QtCore.QSize(640, 360))
        MainWindow.setWindowOpacity(1.0)

        self.background_image = QtWidgets.QLabel(MainWindow)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 0, 621, 261))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayoutSettings = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayoutSettings.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutSettings.setObjectName("gridLayoutSettings")

        self.label_packege = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_packege.setObjectName("label_packege")
        self.gridLayoutSettings.addWidget(self.label_packege, 3, 0, 1, 1)

        self.label_matrix = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_matrix.setObjectName("label_matrix")
        self.gridLayoutSettings.addWidget(self.label_matrix, 1, 0, 1, 1)

        self.label_music = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_music.setObjectName("label_music")
        self.gridLayoutSettings.addWidget(self.label_music, 0, 0, 1, 1)

        self.comboBoxPackages = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBoxPackages.setObjectName("comboBoxPackages")
        self.gridLayoutSettings.addWidget(self.comboBoxPackages, 3, 1, 1, 1)

        self.slider_volume_music = QtWidgets.QSlider(self.gridLayoutWidget)
        self.slider_volume_music.setMaximum(100)
        self.slider_volume_music.setOrientation(QtCore.Qt.Horizontal)
        self.slider_volume_music.setObjectName("slider_volume_music")
        self.gridLayoutSettings.addWidget(self.slider_volume_music, 0, 1, 1, 1)

        self.comboBoxMatrix = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBoxMatrix.setObjectName("comboBoxMatrix")
        self.gridLayoutSettings.addWidget(self.comboBoxMatrix, 1, 1, 1, 1)

        self.checkBoxFullScreen = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBoxFullScreen.setText("")
        self.checkBoxFullScreen.setObjectName("checkBoxFullScreen")
        self.gridLayoutSettings.addWidget(self.checkBoxFullScreen, 2, 1, 1, 1)

        self.label_fullscreen = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_fullscreen.setObjectName("label_fullscreen")
        self.gridLayoutSettings.addWidget(self.label_fullscreen, 2, 0, 1, 1)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(450, 280, 181, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutSaveCancel = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayoutSaveCancel.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutSaveCancel.setObjectName("horizontalLayoutSaveCancel")

        self.btn_save = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayoutSaveCancel.addWidget(self.btn_save)

        self.btn_cancel = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayoutSaveCancel.addWidget(self.btn_cancel)

        self.btn_play = QtWidgets.QPushButton("Играть", MainWindow)
        self.btn_play.move(500, 220)

        self.btn_open_settings = QtWidgets.QPushButton("Настройки", MainWindow)
        self.btn_open_settings.move(500, 260)

        self.btn_close = QtWidgets.QPushButton("Выйти", MainWindow)
        self.btn_close.move(500, 300)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Game Launcher \"Underground of Knights\""))
        self.label_packege.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Набор уровней</span></p></body></html>"))
        self.label_matrix.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Разрешение экрана</span></p></body></html>"))
        self.label_music.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Музыка .o0</span></p></body></html>"))
        self.label_fullscreen.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Полноэкранный режим</span></p></body></html>"))
        self.btn_save.setText(_translate("MainWindow", "сохранить"))
        self.btn_cancel.setText(_translate("MainWindow", "отмена"))
        self.btn_play.setText(_translate("MainWindow", "Играть"))
        self.btn_close.setText(_translate("MainWindow", "Выйти"))
        self.btn_open_settings.setText(_translate("MainWindow", "Настройки"))