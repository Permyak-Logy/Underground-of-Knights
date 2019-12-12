import pygame, os
from win32api import GetSystemMetrics
from random import randint, choice


MODE_MENU, MODE_PLAY, MODE_PAUSE = 0, 1, 2


class GameExample:
    '''
    Главный класс игры
    '''

    def __init__(self):
        '''Инициализация'''
        pygame.init()

        # Скрытие курсора
        pygame.mouse.set_visible(False)

        # Инициализация параметров окна
        self.size = self.width, self.height = 800, 500

        # Инициализация главного кадра игры
        self.main_screen = pygame.display.set_mode(self.size)

        # Загрузка меню
        self.load_menu()

        # Некоторые переменныне в игре
        self.mode = MODE_MENU  # Переключатель между режимом меню MODE_MENU / в игре MODE_GAME / в паузе MODE_PAUSE
        self.battle_status = False  # Переключатель между режимом битвы (True) и мира (False)
        self.running = False  # Активнойсть программы
        self.image_arrow = pygame.transform.scale(self.load_image('arrow.png', -1), (22, 22))  # Картинка курсора

        # Центрирование окна
        self.center()

    def load_menu(self):
        '''Загруска меню'''

        # Временное сокращение некоторых функций
        _Font = pygame.font.Font
        _Color = pygame.Color

        # Пункты меню
        puncts = [PushButton(text='Играть', pos=(10, 400), size=(150, 50), color=_Color('green'),
                             font=_Font(None, 30), func=lambda: print('Играть')),

                  PushButton(text='Настройки', pos=(210, 400), size=(150, 50), color=_Color('yellow'),
                             font=_Font(None, 30), func=lambda: print('Настройки')),

                  PushButton(text='Руководство', pos=(410, 400), size=(150, 50), color=_Color('#942ad4'),
                             font=_Font(None, 30), func=lambda: print('Руководство')),

                  PushButton(text='Выйти', pos=(610, 400), size=(150, 50), color=_Color('red'),
                             font=_Font(None, 30), func=lambda: print('Выход'))]

        # Создание меню с раннее созданными пунктами
        self.menu = Menu(self, puncts)

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

            # Отрисовка экрана
            self.main_screen.fill(pygame.Color('black'))
            if self.mode == MODE_MENU:
                # Рисование меню
                self.menu.render(self.main_screen)
            if self.mode == MODE_PLAY:
                pass
            if pygame.mouse.get_focused():
                # Отрисовка курсора
                self.main_screen.blit(self.image_arrow, (pygame.mouse.get_pos()))

            # Обновление дисплея
            pygame.display.flip()

        # Закрытие игры
        self.close()

    def mousePressEvent(self, event):
        '''События мыши'''
        if self.mode == MODE_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяет элементы после нажатия мышкой
                self.menu.checkOnPress(event.pos)

    def keyPressEvent(self, event):
        '''События клавиатуры'''
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
        '''Выход из игры'''
        pygame.quit()
        print('-----Game closed------')


class Menu:
    def __init__(self, game, punkts=[]):
        self.game = game  # Подключение игры к меню
        background = self.game.load_image('background menu.jpg')  # Загрузка картинки фона
        self.image_background = pygame.transform.scale(background, self.game.size)  # Преобразование фона
        self.punkts = punkts  # Занесение пунктов меню

    def checkOnPress(self, pos):
        '''Проверяет меню после клика мышки''' # Не могу придумать...
        for punckt in self.punkts:
            punckt.on_click(pos)

    def render(self, screen, num_punkt=-1):
        '''Рисует меню'''
        screen.blit(self.image_background, (0, 0))  # Накладывет фон
        for punkt in self.punkts:
            # Рисует все пункты меню
            punkt.draw(screen, ispressed=(punkt.number == num_punkt))


class PushButton:
    '''
    Кнопки в меню игры
    '''
    def __init__(self, text=None, pos=(0, 0), size=(30, 10), font=None, color=(255, 255, 255),
                 color_active=(0, 255, 255), color_text=(0, 0, 0), image=None, func=None, number=0):
        '''Инициализация'''
        self.text = text  # Текст
        self.font = (pygame.font.Font(None, size[0]) if font is None else font)  # Шрифт
        self.pos = self.x, self.y = pos  # Позиция
        self.size = self.width, self.height = size  # Размеры
        self.number = number  # Порядковый номер пункта
        # Цвет основной / активный / текста и картинка
        self.color, self.color_active, self.color_text = color, color_active, color_text
        self.func = func  # Функция кнопки
        # Картинка
        self.image = pygame.transform.scale(image, self.size) if image is not None else None

    def draw(self, screen, ispressed=False):
        '''Рисует кнопку на screen'''
        surface = pygame.Surface(self.size)
        surface.fill(self.color if not ispressed else self.color_active)
        if self.image is not None:
            surface.blit(self.image, self.pos)
        if self.text is not None:
            text = self.font.render(self.text, 1, self.color_text)
            text_x = self.width // 2 - text.get_width() // 2
            text_y = self.height // 2 - text.get_height() // 2
            surface.blit(text, (text_x, text_y))

        screen.blit(surface, self.pos)

    def get_focused(self, pos):
        '''Возвращает True если pos  находится на кнопке, иначе False'''
        if not self.x <= pos[0] <= self.x + self.width:
            return False
        if not self.y <= pos[1] <= self.y + self.height:
            return False
        return True

    def on_click(self, pos):
        '''Вызывает функцию подключённую к кнопке, если она была нажата'''
        if self.func is None:
            return
        if not self.get_focused(pos):
            return
        self.func()


if __name__ == '__main__':
    ex = GameExample()
    ex.mainloop()
