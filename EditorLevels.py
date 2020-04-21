from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt
import sys


class EditorLevels(QMainWindow):
    def __init__(self):
        super().__init__()
        self.field = []
        self.initUI()

    def initUI(self):
        rect = 60
        self.field = [[Cell(self, pos=(x, y)) for x in range(rect)] for y in range(rect)]
        self.resize(15 * 60, 15 * 60)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S:
            self.save_level()

    def save_level(self):
        data = '\n'.join([' '.join(list(map(lambda x: x.get_symbol(), row))) for row in self.field])
        with open('level.txt', mode='w', encoding='utf8') as file:
            file.write(data)
        print('Save as level.txt')


class Cell(QPushButton):
    icons = {
        0: ('QPushButton{background-color: black;}', '_'),
        1: ('QPushButton{background-color: White;}', '.'),
        2: ('QPushButton{background-color: gray;}', '#'),
        3: ('QPushButton{background-color: green;}', '@'),
        4: ('QPushButton{background-color: BlueViolet;}', 'W'),
        5: ('QPushButton{background-color: Purple;}', 'A'),
        6: ('QPushButton{background-color: yellow;}', 'T'),
        7: ('QPushButton{background-color: red;}', 'e'),
        8: ('QPushButton{background-color: LightSeaGreen;}', 'E')
    }

    def __init__(self, window, state=0, pos=(0, 0)):
        super().__init__(window)
        size = QSize(15, 15)
        self.resize(size)
        self.move(size.width() * pos[0], size.height() * pos[1])
        self.state = state
        self.setStyleSheet(self.icons[self.state][0])
        self.clicked.connect(self.change_state)

    def change_state(self):
        self.state = (self.state + 1) % len(self.icons.keys())
        self.setStyleSheet(self.icons[self.state][0])

    def get_symbol(self):
        return self.icons[self.state][1]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EditorLevels()
    ex.show()
    sys.exit(app.exec_())
