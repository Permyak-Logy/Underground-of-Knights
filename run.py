import pygame
import os


MODE_MENU, MODE_GAME, MODE_PAUSE, = 0, 1, 2
DEBUG_INFO = True


class GameExample:
    '''
    Главный класс игры
    '''

    def __init__(self):
        '''Инициализация'''
        (print('init Game') if DEBUG_INFO else None)
        pygame.init()

        # Скрытие курсора
        pygame.mouse.set_visible(False)

        # Инициализация размеров окна
        n = 600
        self.size = self.width, self.height = n * 2, n

        # Инициализация главного кадра игры
        self.main_screen = pygame.display.set_mode(self.size)

        # Установка титульного имени окна
        pygame.display.set_caption('Soul Knight Demo')

        # Установка иконки
        pygame.display.set_icon(self.load_image('icon.png'))

        # Загрузка меню
        self.load_menu()

        # Некоторые переменныне в игре
        self.mode = MODE_MENU  # Переключатель между режимом меню MODE_MENU / в игре MODE_GAME / в паузе MODE_PAUSE
        self.running = False  # Активнойсть программы
        self.image_arrow = pygame.transform.scale(self.load_image('arrow.png', -1), (22, 22))  # Картинка курсора

        # Центрирование окна
        self.center()

    def load_menu(self):
        '''Загруска меню'''
        (print('\tinit menu:\n') if DEBUG_INFO else None)
        # Временное сокращение некоторых функций
        _Font = pygame.font.Font
        _SysFont = pygame.font.SysFont
        _Color = pygame.Color

        # fonts = ['consolas', 'cuprum', 'gabriola', ''] # Красивые шрифты
        # Пункты меню
        puncts = [Punct(text='Soul Knight Demo', pos=(int(self.width * 0.5), int(self.height * 0.45)), size=-1,
                        isfill=False, color_text=_Color('white'), number=0,
                        font=_SysFont('gabriola', self.height // 10), bolden=False),

                  Punct(text='Играть', pos=(int(self.width * 0.05), int(self.height * 0.8)), size=-1,
                        isfill=False, color_text=_Color('green'), number=1,
                        font=_SysFont('gabriola', self.height // 20), func=self.start_game),

                  Punct(text='Настройки', pos=(int(self.width * 0.3), int(self.height * 0.8)), size=-1,
                        isfill=False, color_text=_Color('white'), number=2,
                        font=_SysFont('gabriola', self.height // 20), func=self.open_settings),

                  Punct(text='Руководство', pos=(int(self.width * 0.55), int(self.height * 0.8)), size=-1,
                        isfill=False, color_text=_Color('white'), number=3,
                        font=_SysFont('gabriola', self.height // 20), func=self.open_guide),

                  Punct(text='Выйти', pos=(int(self.width * 0.8), int(self.height * 0.8)), size=-1,
                        isfill=False, color_text=_Color('red'), number=4,
                        font=_SysFont('gabriola', self.height // 20), func=self.close)]

        # Создание меню с раннее созданными пунктами
        self.menu = Menu(self, puncts)

    def start_game(self):
        '''Начать игру'''
        (print('GameExample.start_game()') if DEBUG_INFO else None)
        self.mode = MODE_GAME


    def open_settings(self):
        '''Открывает настройки'''
        (print('GameExample.open_settings()') if DEBUG_INFO else None)

    def open_guide(self):
        '''Открывает руководство'''
        (print('GameExample.open_guide()') if DEBUG_INFO else None)

    def start_screen_opening(self):
        '''Зашрузочная заставка'''
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.main_screen.fill(pygame.color.Color('black'))
            pygame.display.flip()

    def mainloop(self):
        ''' Главный цикл программы '''
        (print('\n-----Game started------') if DEBUG_INFO else None)

        self.running = True
        # self.start_screen_opening()
        while self.running:
            # Проверка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_press_event(event)
                if event.type == pygame.KEYDOWN:
                    self.key_press_event(event)

            # Отрисовка экрана
            self.main_screen.fill(pygame.Color('black'))
            if self.mode == MODE_MENU:
                # Рисование меню
                self.menu.render(self.main_screen)
            if self.mode == MODE_GAME:
                pass
            if pygame.mouse.get_focused():
                # Отрисовка курсора
                self.main_screen.blit(self.image_arrow, (pygame.mouse.get_pos()))

            # Обновление дисплея
            pygame.display.flip()

        # Закрытие игры
        pygame.quit()
        (print('-----Game finished------') if DEBUG_INFO else None)

    def mouse_press_event(self, event):
        '''События мыши'''
        if self.mode == MODE_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяет элементы после нажатия мышкой
                self.menu.checkOnPress(event.pos)

    def key_press_event(self, event):
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
        '''Выход из игры, и завершение главного цикла'''
        (print('GameExample.close()') if DEBUG_INFO else None)
        self.running = False


class Menu:
    def __init__(self, game, punkts=None):
        self.game = game  # Подключение игры к меню
        background = self.game.load_image('background menu.jpg')  # Загрузка картинки фона
        self.image_background = pygame.transform.scale(background, self.game.size)  # Преобразование фона
        self.punkts = punkts if punkts is not None else list()  # Занесение пунктов меню

    def checkOnPress(self, pos):
        '''Проверяет меню после клика мышки'''  # Не могу придумать...
        for punckt in self.punkts:
            punckt.on_click(pos)

    def render(self, screen):
        '''Рисует меню'''
        screen.blit(self.image_background, (0, 0))  # Накладывет фон
        for punkt in self.punkts:
            # Рисует все пункты меню
            punkt.draw(screen, ispressed=punkt.get_focused(pygame.mouse.get_pos()))


class Punct:
    '''
    Кнопки в меню игры
    '''

    def __init__(self, text=None, pos=(0, 0), size=-1, font=None, color=(100, 100, 100), isfill=True,
                 color_active=(0, 255, 255), color_text=(0, 0, 0), image=None, func=None, number=0, bolden=True):
        '''Инициализация'''
        (print(f'\t\tinit punct text: "{text}"", number: "{number}" : ', end='') if DEBUG_INFO else None)

        self.text = text                                                            # Текст
        self.font = (pygame.font.Font(None, size[0]) if font is None else font)     # Шрифт
        self.pos = self.x, self.y = pos                                             # Позиция
        self.number = number                                                        # Порядковый номер пункта

        # Цвет основной / активный / текста и картинка
        self.color, self.color_active, self.color_text = color, color_active, color_text

        self.func = func                                                                        # Функция кнопки
        self.image = pygame.transform.scale(image, self.size) if image is not None else None    # Картика пункта
        self.isfill = isfill                                                                    # Заливка
        self.isshow = True                                                                      # Отображние
        self.bolden = bolden                             # Флаг выделения при наведении курсора

        if size == -1:  # Автоматическая генерация размера
            (self.font.set_bold(True) if bolden else None)
            size = self.font.size(self.text)
            (self.font.set_bold(False) if bolden else None)

        self.size = self.width, self.height = size          # Размеры

        (print('True\n', end='') if DEBUG_INFO else None)

    def show(self):
        """Показать виджет"""
        self.isshow = True

    def hide(self):
        """Скрыть виджет"""
        self.isshow = False

    def connect(self, func):
        """Подключить функцию"""
        self.func = func

    def draw(self, screen, ispressed=False):
        '''Рисует кнопку на screen'''
        if not self.isshow:
            # Не рисует если пункт скрыт
            return
        surface = pygame.Surface(self.size)
        if self.isfill:  # Заливка области
            surface.fill(self.color if
                         not ispressed or
                         not self.bolden else
                         self.color_active)
        else:  # Преобразование в прозрачный фон
            surface.fill((1, 0, 0))
            surface.set_colorkey((1, 0, 0))
            surface.convert_alpha()

        if self.image is not None:  # наложение картинки если есть она
            surface.blit(self.image, self.pos)

        if self.text is not None:  # Наложение текста если он есть
            if not ispressed or not self.bolden:
                # Создание surface текста
                text = self.font.render(self.text, 1, self.color_text)
            else:
                # Создание surface выделенного текста
                self.font.set_bold(True)
                text = self.font.render(self.text, 1, self.color_text)
                self.font.set_bold(False)

            # Вычесление центра текста
            text_x = self.width // 2 - text.get_width() // 2
            text_y = self.height // 2 - text.get_height() // 2

            # Наложение текста
            surface.blit(text, (text_x, text_y))

        # Наложение получившегося изображения punct на screen
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


class GameSpace:
    def __init__(self, game, punkts=None):
        self.game = game
        self.punkts = punkts if punkts is not None else list()
        self.levels = []
        self.current_level_index = 0

    def check_on_press_punkts(self, pos):
        for punkt in self.punkts:
            punkt.on_click(pos)

    def render(self, screen):
        pass

    def update(self):
        pass

    def add_level(self):
        pass

    def start_random_generation(self, lvl_count=5):
        pass


class Level:
    def __init__(self, gamespace):
        self.game_space = gamespace

    def render(self, screen):
        pass

    def add_sector(self):
        pass

    def start_random_generation(self, sector_count=5):
        pass


class Sector:
    '''
    Класс комнаты или сектора в игре
    '''

    def __init__(self, level, mode):
        pass

    def render(self, screen):
        pass

    def add_object(self, obj):
        pass

    def start_random_generation(self, enemy_count=8):
        pass


if __name__ == '__main__':
    ex = GameExample()
    ex.mainloop()
