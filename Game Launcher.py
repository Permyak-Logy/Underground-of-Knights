import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from SettingsForm import Ui_MainWindow
from win32api import GetSystemMetrics


class SettingsWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_save.clicked.connect(self.save)
        self.btn_cancel.clicked.connect(self.open_main_menu)
        self.btn_play.clicked.connect(self.play)
        self.btn_open_settings.clicked.connect(self.open_settings)
        self.btn_close.clicked.connect(self.close)
        self.background_image.setPixmap(QPixmap("data\images\\background menu.png").scaled(self.size()))
        self.background_image.resize(self.size())
        self.open_main_menu()
        self.show()

    def play(self):
        self.hide()
        if os.access("run.py", os.F_OK):
            os.system("python run.py")
        elif os.access("Underground of Knights.exe", os.F_OK):
            os.startfile('Underground of Knights.exe')
        self.close()

    def open_main_menu(self):
        for row in range(self.gridLayoutSettings.rowCount()):
            for col in range(self.gridLayoutSettings.columnCount()):
                elem = self.gridLayoutSettings.itemAtPosition(row, col)
                # print(dir(elem))
                elem.widget().hide() if elem is not None else None
        self.btn_save.hide()
        self.btn_cancel.hide()

        self.btn_play.show()
        self.btn_open_settings.show()
        self.btn_close.show()

    def open_settings(self):
        self.load_settings()
        for row in range(self.gridLayoutSettings.rowCount()):
            for col in range(self.gridLayoutSettings.columnCount()):
                elem = self.gridLayoutSettings.itemAtPosition(row, col)
                elem.widget().show() if elem is not None else None
        self.btn_save.show()
        self.btn_cancel.show()

        self.btn_play.hide()
        self.btn_open_settings.hide()
        self.btn_close.hide()

    def load_settings(self):
        try:
            with open('data\settings data', encoding='utf8') as file:
                data = file.readlines()
        except FileNotFoundError:
            data = [f'matrix {GetSystemMetrics(0)}x{GetSystemMetrics(1)}', 'fullscreen true', 'volume 0.5']
        finally:
            packages = list(filter(lambda x: os.path.isdir(f'data/levels/{x}'), os.listdir('data/levels')))
            matrixs = ["7680x4320", "5120x2880", "3200x1800", "1920x1080", "1280x720", "640x360"]
            matrixs = list(filter(lambda x: int(x.split('x')[0]) <= GetSystemMetrics(0) and
                                            int(x.split('x')[1]) <= GetSystemMetrics(1), matrixs))
            self.comboBoxPackages.clear()
            self.comboBoxMatrix.clear()
            for package in packages:
                self.comboBoxPackages.addItem(package)

            for matrix in matrixs:
                self.comboBoxMatrix.addItem(matrix)
            for line in data:
                key, val = line.split()
                if key == 'matrix':
                    self.comboBoxMatrix.setCurrentIndex(matrixs.index(val)) if val in matrixs else None
                if key == 'fullscreen':
                    val = val == 'true'
                    self.checkBoxFullScreen.setChecked(val)
                elif key == 'volume':
                    self.slider_volume_music.setValue(int(float(val) * 100))
                elif key == 'packege':
                    self.comboBoxPackages.setCurrentIndex(packages.index(val)) if val in packages else None

    def save(self):
        with open('data\settings data', encoding='utf8', mode='w') as file:
            file.write(f'matrix {self.comboBoxMatrix.currentText()}\n')
            file.write(f'fullscreen {"true" if self.checkBoxFullScreen.isChecked() else "false"}\n')
            file.write(f'volume {self.slider_volume_music.value() / 100}\n')
            file.write(f'package {self.comboBoxPackages.currentText()}')
        self.open_main_menu()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SettingsWindow()
    app.exec_()
