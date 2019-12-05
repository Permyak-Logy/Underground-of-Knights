import pygame
from win32api import GetSystemMetrics
from random import randint, choice


class GameExample:
    '''
    Главный класс игры
    '''
    def __init__(self):
        pass
    
    def checkEvents(self):
        pass
    
    def mousePressEvent(self, event):
        pass
    
    def keyPressEvent(self, event):
        pass
    
    def mainloop(self):
        # Тут будет произходить основной цикл программы
        pass
    
    def close(self):
        pass


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
