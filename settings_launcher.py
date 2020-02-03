import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from SettingsForm import Ui_MainWindow
from win32api import GetSystemMetrics


class SettingsWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, game=None):
        super().__init__()
        self.setupUi(self)
        self.game = game
        self.setFixedSize(284, 185)
        self.btn_save.clicked.connect(self.save)
        self.btn_close.clicked.connect(self.close)
        self.slider_volume_music.valueChanged.connect(self.change_p)
        self.load_settings()
        self.show()

    def change_p(self):
        if self.game is None:
            return
        self.game.music.set_volume(self.slider_volume_music.value() / 100)

    def load_settings(self):
        try:
            with open('data\settings data', encoding='utf8') as file:
                data = file.readlines()
        except FileNotFoundError:
            data = [f'matrix {GetSystemMetrics(0)}x{GetSystemMetrics(1)}', 'fullscreen true', 'volume 0.5']
        finally:
            packeges = list(filter(lambda x: os.path.isdir(f'data/levels/{x}'), os.listdir('data/levels')))
            print(packeges)
            for packege in packeges:
                self.comboBoxPacheges.addItem(packege)
            for line in data:
                key, val = line.split()
                if key == 'matrix':
                    x, y = list(map(int, val.split('x')))
                    self.spinBoxX.setValue(x)
                    self.spinBoxY.setValue(y)
                elif key == 'fullscreen':
                    val = val == 'true'
                    self.checkBoxFullScreen.setChecked(val)
                elif key == 'volume':
                    self.slider_volume_music.setValue(int(float(val) * 100))
                elif key == 'packege':
                    self.comboBoxPacheges.setCurrentIndex(packeges.index(val)) if val in packeges else None

    def save(self):
        with open('data\settings data', encoding='utf8', mode='w') as file:
            file.write(f'matrix {self.spinBoxX.value()}x{self.spinBoxY.value()}\n')
            file.write(f'fullscreen {"true" if self.checkBoxFullScreen.isChecked() else "false"}\n')
            file.write(f'volume {self.slider_volume_music.value() / 100}\n')
            file.write(f'packege {self.comboBoxPacheges.currentText()}')
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SettingsWindow()
    app.exec_()
