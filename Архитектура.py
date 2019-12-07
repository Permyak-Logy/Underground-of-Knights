import pygame
from win32api import GetSystemMetrics
from random import randint, choice


class GameExample:
    '''
    Главный класс игры
    '''
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 300, 300
        self.main_screen = pygame.display.set_mode(self.size)
        self.center()
        self.running = True

    def center(self):
        """Центрирование как в QT"""
        # qp = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().center()
        # qp.moveCenter(cp)
        # self.move(qp.topLeft())

    def checkEvents(self):
        pass
    
    def mousePressEvent(self, event):
        pass
    
    def keyPressEvent(self, event):
        pass

    def mainloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousePressEvent(event)
                if event.type == pygame.KEYDOWN:
                    self.keyPressEvent(event)

            self.checkEvents()

            pygame.display.flip()
        self.close()
    
    def close(self):
        pygame.quit()


class BoardLevel:
    '''
    Класс уровня локации
    '''
    def __init__(self, game):
        pass
    
    def generation(self):
        pass


class Sector:
    '''
    Класс комнаты или сектора в игре
    '''
    def __init__(self, board, mode):
        pass
    
    def create_objects(self):
        pass


class BaseObject:
    '''
    Основной класс для всех объектов в игре
    '''
    def __init__(self, game):
        pass


class Wall(BaseObject):
    '''
    Класс неподвижных стен, перегородок и т.п. в Sector
    '''
    def __init__(self, game):
        pass


class Hero(BaseObject):
    '''
    Основной класс для персонажей
    '''
    def __init__(self, game):
        pass


class Player(Hero):
    '''
    Класс объекта игрока
    '''
    def __init__(self, game):
        pass


class Enemy(Hero):
    '''
    Основной класс для врагов
    '''
    def __init__(self, game):
        pass


class Item:
    '''
    Основной класс предметов игры
    '''
    def __init__(self, game):
        pass


class Weapon(Item):
    '''
    Основной класс для оружия
    '''
    def __init__(self, game):
        pass


class Armor(Item):
    '''
    Основной класс для брони
    '''
    def __init__(self, game):
        pass


class Booster(Item):
    '''
    Основной класс для разных бустеров
    '''
    def __init__(self, game):
        pass


if __name__ == '__main__':
    ex = GameExample()
    ex.mainloop()
