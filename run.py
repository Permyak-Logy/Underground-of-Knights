import pygame, os
from win32api import GetSystemMetrics
from random import randint, choice


MODE_MENU, MODE_PLAY, MODE_PAUSE = 0, 1, 2


class GameExample:
    '''
    Главный класс игры
    '''

    def __init__(self):
        pygame.init()

        # Инициализация параметров окна
        self.size = self.width, self.height = 500, 500

        # Инициализация главного кадра игры
        self.main_screen = pygame.display.set_mode(self.size)

        # Загрузка кадра меню и его виджетов
        self.load_menu_screen()

        # Некоторые переменныне в игре
        self.mode = MODE_MENU  # Переключатель между режимом меню (0) / в игре (1) / в паузе (2)
        self.battle_status = False  # Переключатель между режимом битвы (True) и мира (False)
        self.running = False

        # Центрирование окна
        self.center()

    def load_menu_screen(self):
        self.menu_screen = pygame.Surface([self.width, self.height])  # Холст меню
        self.menu_buttons = []  # Список виджетов меню
        
        btn_test = PushButton(self.menu_screen, size=(100, 50), color=(0, 255, 255), pos=(10, 30),
                              func=self.some_func)  # Тестовая кнопка
        self.menu_buttons.append(btn_test)

    def load_game_screen(self):
        self.play_screen = pygame.Surface([self.width, self.height])  # Холст игры

    def mainloop(self):
        ''' Главный цикл программы '''

        print('-----Game started------')
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousePressEvent(event)
                if event.type == pygame.KEYDOWN:
                    self.keyPressEvent(event)

            if self.mode == MODE_PLAY:
                self.checkEvents()

            # Отрисовка экрана
            self.main_screen.fill(pygame.Color('black'))
            if self.mode == MODE_MENU:
                self.main_screen.blit(self.menu_screen, (0, 0))
            if self.mode == MODE_PLAY:
                self.main_screen.blit(self.play_screen, (0, 0))

            # Обновление кадра
            pygame.display.flip()

        # Закрытие игры
        self.close()

    def some_func(self):
        '''Функция теста функционала кнопки.'''
        print('Some func был активирован')

    def checkEvents(self):
        pass

    def mousePressEvent(self, event):
        if self.mode == MODE_MENU:
            click_pos = event.pos
            for buttons in self.menu_buttons:
                buttons.check_click(click_pos)

    def keyPressEvent(self, event):
        pass

    def load_image(self, name, colorkey=None):
        """
        Возвращает картинку с именем name. Если есть colorkey, то у картинки делается фон прозрачным.
        Если colorkey == -1 то берётся цвет из самого верхнего угла картинки, иначе ...
        """
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname).convert()

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def center(self):
        """Центрирование как в QT"""
        # qp = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().center()
        # qp.moveCenter(cp)
        # self.move(qp.topLeft())

    def close(self):
        pygame.quit()
        print('-----Game closed------')


class PushButton:
    '''
    Кнопки в меню игры
    '''
    def __init__(self, screen, size=(30, 10), pos=(0, 0), color=(255, 255, 255), image=None, func=None):
        self.screen = screen
        self.pos = self.x, self.y = pos
        self.size = self.width, self.height = size
        self.color = color
        self.func = func
        self.surface = pygame.Surface(list(size))
        self.surface.fill(color)
        if image is not None:
            self.surface.blit(pygame.transform.scale(image, size))
        self.screen.blit(self.surface, pos)

    def check_click(self, pos):
        '''Вызывает функцию подключённую к кнопке если она была нажата'''
        if self.func is None:
            return
        if not self.x <= pos[0] <= self.x + self.width:
            return
        if not self.y <= pos[1] <= self.y + self.height:
            return
        self.func()


if __name__ == '__main__':
    ex = GameExample()
    ex.mainloop()
