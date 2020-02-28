import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from SettingsForm import Ui_MainWindow
from win32api import GetSystemMetrics
import run


class SettingsWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """Инициализация"""
        super().__init__()
        self.setupUi(self)  # Загрузка формы

        # Поключение кнопок к их функциям
        self.btn_save.clicked.connect(self.save)  # Сохранить
        self.btn_cancel.clicked.connect(self.open_main_menu)  # Отмена
        self.btn_play.clicked.connect(self.play)  # Играть
        self.btn_open_settings.clicked.connect(self.open_settings)  # Настройки
        self.btn_close.clicked.connect(self.close)  # Выйти

        # Установка фона
        self.background_image.setPixmap(QPixmap("data\images\\background menu.png").scaled(self.size()))
        self.background_image.resize(self.size())

        # Открытие главного меню
        self.open_main_menu()

    def play(self):
        """Запускает игру"""
        self.hide()
        run.GameExample().mainloop()

    def open_main_menu(self):
        """Открывает главное меню"""
        # Сокрытие виджетов настроек
        for row in range(self.gridLayoutSettings.rowCount()):
            for col in range(self.gridLayoutSettings.columnCount()):
                elem = self.gridLayoutSettings.itemAtPosition(row, col)
                elem.widget().hide() if elem is not None else None
        self.btn_save.hide()
        self.btn_cancel.hide()

        # Показ виджетов главного меню
        self.btn_play.show()
        self.btn_open_settings.show()
        self.btn_close.show()

    def open_settings(self):
        """Открывает меню настроек"""
        self.load_settings()  # Загрузка актуальных настроек из файла settings data
        # Показ виджетов настроек
        for row in range(self.gridLayoutSettings.rowCount()):
            for col in range(self.gridLayoutSettings.columnCount()):
                elem = self.gridLayoutSettings.itemAtPosition(row, col)
                elem.widget().show() if elem is not None else None
        self.btn_save.show()
        self.btn_cancel.show()

        # Сокрытие виджетов главного меню
        self.btn_play.hide()
        self.btn_open_settings.hide()
        self.btn_close.hide()

    def load_settings(self):
        """Загрузка актуальных настроек из главного меню"""
        try:
            # Если есть раннее созданный файл то программа загрузид данные из него
            with open('data\settings data', encoding='utf8') as file:
                data = file.readlines()
        except FileNotFoundError:
            # Иначе сама сгенерирует настройки
            data = [f'matrix 640x360', 'fullscreen true', 'volume 0.5', 'package std']
        finally:
            # Загрузка доступных пакетов уровней
            packages = list(filter(lambda x: os.path.isdir(f'data/levels/{x}'), os.listdir('data/levels')))
            # Очистка старых данных и занесение новых в соответствующий comboBox
            self.comboBoxPackages.clear()
            for package in packages:
                self.comboBoxPackages.addItem(package)
            # Загрузка допустимых разрешений экрана
            matrixs = ["7680x4320", "5120x2880", "3200x1800", "1920x1080", "1280x720", "640x360"]
            matrixs = list(filter(lambda x: int(x.split('x')[0]) <= GetSystemMetrics(0) and
                                            int(x.split('x')[1]) <= GetSystemMetrics(1), matrixs))
            # Очистка старых данных и занесение новых в соответствующий comboBox
            self.comboBoxMatrix.clear()
            for matrix in matrixs:
                self.comboBoxMatrix.addItem(matrix)

            # Обновление актуальных настроек
            for line in data:
                key, val = line.split()
                if key == 'matrix':  # Разрешение
                    self.comboBoxMatrix.setCurrentIndex(matrixs.index(val)) if val in matrixs else None
                if key == 'fullscreen':  # Полноэкранный режим
                    val = val == 'true'
                    self.checkBoxFullScreen.setChecked(val)
                elif key == 'volume':  # Громкость
                    self.slider_volume_music.setValue(int(float(val) * 100))
                elif key == 'package':  # Пакет уровней
                    self.comboBoxPackages.setCurrentIndex(packages.index(val)) if val in packages else None

    def save(self):
        """Сохранение новых настроек и переход в главное меню"""
        with open('data\settings data', encoding='utf8', mode='w') as file:
            file.write(f'matrix {self.comboBoxMatrix.currentText()}\n')
            file.write(f'fullscreen {"true" if self.checkBoxFullScreen.isChecked() else "false"}\n')
            file.write(f'volume {self.slider_volume_music.value() / 100}\n')
            file.write(f'package {self.comboBoxPackages.currentText()}')
        self.open_main_menu()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SettingsWindow()
    ex.show()
    app.exec_()
