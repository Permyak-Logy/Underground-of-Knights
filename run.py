import pygame
import os
import sys
from win32api import GetSystemMetrics

MODE_MENU, MODE_GAME, MODE_SETTINGS = 0, 1, 2
DEBUG_INFO = True
FULL_SCREEN = False


class GameExample:
    '''
    Главный класс игры
    '''

    def __init__(self):
        '''Инициализация'''
        print('init Game') if DEBUG_INFO else None
        pygame.init()

        # Скрытие курсора
        pygame.mouse.set_visible(False)

        # Инициализация экрана
        if FULL_SCREEN:
            # Инициализация размеров окна
            self.size = self.width, self.height = GetSystemMetrics(0), GetSystemMetrics(1)
            # Инициализация главного кадра игры
            self.main_screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF |
                                                       pygame.FULLSCREEN)
        else:
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

        # Загруска игрового пространства
        self.load_game_space()

        # Некоторые переменныне в игре
        self.mode = MODE_MENU  # Переключатель между режимами меню MODE_MENU / игра MODE_GAME / настройки MODE_SETTINGS
        self.image_arrow = pygame.transform.scale(self.load_image('arrow.png', -1), (22, 22))  # Картинка курсора

        # Центрирование окна
        self.center()

    def mainloop(self):
        ''' Главный цикл программы '''
        print('\n-----Game started------') if DEBUG_INFO else None

        # self.start_screen_opening()
        while True:
            # Проверка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
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
                self.game_space.update()
                # Рисование ирового пространства
                self.game_space.render(self.main_screen)
            if pygame.mouse.get_focused():
                # Отрисовка курсора
                self.main_screen.blit(self.image_arrow, (pygame.mouse.get_pos()))

            # Обновление дисплея
            pygame.display.flip()

    @staticmethod
    def load_image(name, colorkey=None):
        """
        Возвращает картинку с именем name. Если есть colorkey, то у картинки делается фон прозрачным.
        Если colorkey == -1 то берётся цвет из самого верхнего угла картинки, иначе ...
        """
        fullname = os.path.join('data\images', name)
        image = pygame.image.load(fullname).convert()

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def load_menu(self):
        '''Загруска меню'''
        print('\tinit menu:\n') if DEBUG_INFO else None
        # Сокращение некоторых функций
        _Font = pygame.font.Font
        _SysFont = pygame.font.SysFont
        _Color = pygame.Color

        # fonts = ['consolas', 'cuprum', 'gabriola', ''] # Красивые шрифты
        # Пункты меню
        punkts = [Punkt(text='Soul Knight Demo', pos=(int(self.width * 0.5), int(self.height * 0.45)), size=-1,
                        isfill=False, color_text=_Color('white'), number=0,
                        font=_SysFont('gabriola', self.height // 10), bolden=False),

                  Punkt(text='Играть', pos=(int(self.width * 0.05), int(self.height * 0.8)), size=-1,
                        isfill=False, color_text=_Color('green'), number=1,
                        font=_SysFont('gabriola', self.height // 20), func=self.start_game),

                  Punkt(text='Настройки', pos=(int(self.width * 0.3), int(self.height * 0.8)), size=-1,
                        isfill=False, color_text=_Color('white'), number=2,
                        font=_SysFont('gabriola', self.height // 20), func=self.open_settings),

                  Punkt(text='Руководство', pos=(int(self.width * 0.55), int(self.height * 0.8)), size=-1,
                        isfill=False, color_text=_Color('white'), number=3,
                        font=_SysFont('gabriola', self.height // 20), func=self.open_guide),

                  Punkt(text='Выйти', pos=(int(self.width * 0.8), int(self.height * 0.8)), size=-1,
                        isfill=False, color_text=_Color('red'), number=4,
                        font=_SysFont('gabriola', self.height // 20), func=self.terminate)]

        # Создание меню с раннее созданными пунктами
        self.menu = Menu(self, punkts)

    def load_game_space(self):
        '''Загрузка ирового пространства'''
        print('\tinit game space:\n') if DEBUG_INFO else None
        # Сокращение некоторых функций
        _Font = pygame.font.Font
        _SysFont = pygame.font.SysFont
        _Color = pygame.Color

        punkts = [Punkt(text='Exit', pos=(int(self.width * 0.01), int(self.height * 0.01)), size=-1,
                        isfill=False, color_text=_Color('yellow'), number=5,
                        font=_SysFont('gabriola', self.height // 20), func=self.open_menu),
                  Punkt(text='Pause', pos=(int(self.width * 0.01), int(self.height * 0.07)), size=-1,
                        isfill=False, color_text=_Color('yellow'), number=6,
                        font=_SysFont('gabriola', self.height // 20), func=self.set_pause),

                  Punkt(text='PAUSE', pos=(0, 0), size=self.size,
                        isfill=False, color_text=_Color('blue'), number=7, bolden=False,
                        font=_SysFont(None, self.height // 2), func=self.unset_pause)]

        self.game_space = GameSpace(self, punkts)

        self.game_space.get_punkt(7).hide()

    def mouse_press_event(self, event):
        '''События мыши'''
        if self.mode == MODE_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Проверяет элементы после нажатия мышкой
                self.menu.check_on_press_punkts(event.pos)

        if self.mode == MODE_GAME:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_space.check_on_press_punkts(event.pos):
                    pass
                elif self.game_space.player.take_thing(event.pos):
                    pass
                elif not self.game_space.pause_status:
                    self.game_space.player.attack(event.pos)

    def key_press_event(self, event):
        '''События клавиатуры'''
        if self.mode == MODE_GAME:
            if event.key == pygame.K_p:
                if self.game_space.pause_status:
                    self.unset_pause()
                else:
                    self.set_pause()
            elif event.key == pygame.K_ESCAPE:
                self.open_menu()

    def start_game(self):
        '''Начать игру'''
        print('GameExample.start_game()') if DEBUG_INFO else None
        self.mode = MODE_GAME
        self.game_space.new_game()
        self.unset_pause()
        self.menu.music_start()

    def open_menu(self):
        '''Открывает меню'''
        print('GameExample.open_menu()') if DEBUG_INFO else None
        self.mode = MODE_MENU
        self.set_pause()
        self.menu.music_start(True)

    def open_settings(self):
        '''Открывает настройки'''
        print('GameExample.open_settings()') if DEBUG_INFO else None

    def open_guide(self):
        '''Открывает руководство'''
        print('GameExample.open_guide()') if DEBUG_INFO else None

    def set_pause(self):
        print('GameExample.set_pause()') if DEBUG_INFO else None
        self.game_space.pause_status = True
        self.game_space.get_punkt(5).hide()
        self.game_space.get_punkt(6).hide()
        self.game_space.get_punkt(7).show()

    def unset_pause(self):
        print('GameExample.unset_pause()') if DEBUG_INFO else None
        self.game_space.pause_status = False
        self.game_space.get_punkt(5).show()
        self.game_space.get_punkt(6).show()
        self.game_space.get_punkt(7).hide()

    def start_screen_opening(self):
        '''Зашрузочная заставка'''
        print('GameExample.start_screen_opening()') if DEBUG_INFO else None
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.main_screen.fill(pygame.color.Color('black'))
            pygame.display.flip()

    def center(self):
        """Центрирование как в QT"""
        print('GameExample.center()') if DEBUG_INFO else None
        # qp = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().center()
        # qp.moveCenter(cp)
        # self.move(qp.topLeft())

    @staticmethod
    def terminate():
        '''Выход из игры, и завершение главного цикла'''
        print('GameExample.close()') if DEBUG_INFO else None
        pygame.quit()
        print('-----Game closed-----')
        sys.exit()


class Menu:
    '''
    Меню игры
    '''

    def __init__(self, game, punkts=None):
        self.game = game  # Подключение игры
        background = self.game.load_image('background menu.jpg')  # Загрузка картинки фона
        self.image_background = pygame.transform.scale(background, self.game.size)  # Преобразование фона
        self.punkts = punkts if punkts is not None else list()  # Занесение пунктов
        pygame.mixer.music.load('data/music/main_menu.mp3')
        self.music_start(True, 0.2)

    def music_start(self, start=False, volume=False):
        # Отвечает за запуск музыки в главном меню
        if start:
            pygame.mixer.music.play(-1)
            # изменение громкости если передан параметр
            if volume:
                pygame.mixer.music.set_volume(volume)
        else:
            pygame.mixer.music.pause()

    def check_on_press_punkts(self, pos):
        '''Проверяет пункты на нажатие'''  # Не могу придумать...
        for punckt in self.punkts:
            if punckt.on_click(pos):
                return True
        return False

    def render(self, screen):
        '''Рисует меню'''
        screen.blit(self.image_background, (0, 0))  # Накладывет фон
        for punkt in self.punkts:
            # Рисует все пункты меню
            punkt.draw(screen, ispressed=punkt.get_focused(pygame.mouse.get_pos()))

    def add_punkt(self, punkt):
        self.punkts.append(punkt)

    def add_punkts(self, *punkts):
        self.punkts += list(punkts)

    def get_punkt(self, number):
        '''Возвращает пункт по заданному номеру'''
        for punkt in self.punkts:
            if punkt.number == number:
                return punkt


class GameSpace:
    '''
    Игровое пространство
    '''

    def __init__(self, game, punkts=None):
        self.game = game  # Подключение игры
        self.punkts = punkts if punkts is not None else list()  # Занесение пунктов
        self.levels = []  # Список уровней
        self.level_x = self.level_y = 0
        self.pause_status = False
        self.size_cell = int(self.game.height * 0.09)

        self.all_sprites = pygame.sprite.Group()  # Все спрайты
        self.walls_group = pygame.sprite.Group()  # Спрайты стен
        self.items_group = pygame.sprite.Group()  # Спрайты вещей
        self.enemies_group = pygame.sprite.Group()  # Спрайты врагов
        self.player_group = pygame.sprite.Group()  # Спрайт игрока
        self.tiles_group = pygame.sprite.Group()  # Спрайты земли

        self.player = None  # Создание игрока
        self.clock = None  # Создание игрового времени

        self.camera = Camera(self)

    def render(self, screen):
        '''Рисует игровое пространство'''
        self.tiles_group.draw(screen)
        self.walls_group.draw(screen)
        self.items_group.draw(screen)
        self.player_group.draw(screen)
        self.enemies_group.draw(screen)

        for punkt in self.punkts:
            punkt.draw(screen, ispressed=punkt.get_focused(pygame.mouse.get_pos()))

    def add_punkt(self, punkt):
        self.punkts.append(punkt)

    def add_punkts(self, *punkts):
        self.punkts += list(punkts)

    def check_on_press_punkts(self, pos):
        '''Проверяет пункты на нажатиe'''
        for punkt in self.punkts:
            if punkt.on_click(pos):
                return True
        return False

    def new_game(self):
        '''Сбрасывает предыдущий прогресс и данные'''
        print('GameSpace.new_game()') if DEBUG_INFO else None

        self.levels.clear()
        self.load_levels('test')
        self.player = Player(self, 0, 0)
        self.level_x, level_y = self.generate_level(self.get_next_level())
        self.clock = pygame.time.Clock()

    def get_next_level(self):
        try:
            return self.levels.pop(0)
        except IndexError:
            return None

    def finish_game(self, message=None):
        '''Заканчивает игру'''
        print('Game.Space.finish_game()') if DEBUG_INFO else None
        self.game.set_pause()
        # Что то надо туть сделать

    def update(self):
        '''Обновляет данные игры'''
        if self.pause_status is True:
            return
        tick = self.clock.tick()
        self.player_group.update(tick)
        self.camera.update(self.player)
        for sprite in self.all_sprites:
            self.camera.apply(sprite)

    def generate_level(self, level):
        print('\tStart generate level') if DEBUG_INFO else None
        if level is None:
            self.finish_game('Уровни кончились!!!')
            return 0, 0
        self.empty_sprites()
        for y in range(len(level)):
            for x in range(len(level[y])):
                obj = level[y][x]
                if obj != '_' and obj != '#':
                    Tile(self, x, y)
                if obj == '#':
                    Wall(self, x, y)
                if obj == '@':
                    self.player.set_pos(x, y)
                    self.player.add(self.player_group, self.all_sprites)

        print('\tFinish generate level')
        return x, y

    def load_levels(self, directory):
        '''Загрузка пакета уровней'''
        print('GameSpace.load_levels()') if DEBUG_INFO else None
        try:
            print(f'\tStart load levels {directory}') if DEBUG_INFO else None
            self.levels.clear()
            for i in range(1, 10 ** 10):
                print(f'\t\t--- connect level lvl_{i} ', end='') if DEBUG_INFO else None
                filename = f"data/levels/{directory}/lvl_{i}.txt"
                # читаем уровень, убирая символы перевода строки
                with open(filename, 'r') as mapFile:
                    level_map = [line.strip().split() for line in mapFile]

                # и подсчитываем максимальную длину
                max_width = max(map(len, level_map))

                # дополняем каждую строку пустыми клетками ('.')
                self.levels.append(list(map(lambda x: x + ['_'] * (max_width - len(x)), level_map)))
                print('True') if DEBUG_INFO else None

        except FileNotFoundError:
            print('False') if DEBUG_INFO else None
            print(f'\tFinish load levels {directory}') if DEBUG_INFO else None
            [print([print(row) for row in level]) for level in self.levels]

    def empty_sprites(self):
        print('GameSpace.empty_sprites()') if DEBUG_INFO else None
        self.all_sprites.empty()
        self.walls_group.empty()
        self.items_group.empty()
        self.enemies_group.empty()
        self.tiles_group.empty()
        self.player_group.empty()

    def get_punkt(self, number):
        '''Возвращает пункт по заданному номеру'''
        for punkt in self.punkts:
            if punkt.number == number:
                return punkt


class Punkt:
    '''
    Виджеты (похожи на PushButton и Label из библиотеки PyQt5)
    '''

    def __init__(self, text=None, pos=(0, 0), size=-1, font=None, color=(100, 100, 100), isfill=True,
                 color_active=(0, 255, 255), color_text=(0, 0, 0), image=None, func=None, number=0, bolden=True):
        '''Инициализация'''
        print(f'\t\tinit punct text: "{text}"", number: "{number}" : ', end='') if DEBUG_INFO else None

        self.set_text(text)  # Установка текста
        self.set_font(font)  # Установка шрифта
        self.connect(func)  # Подключение функции
        self.set_image(image)  # Установка картинки
        self.show()  # Отображение
        self.set_color(color, color_active, color_text)  # Установка цветов элементов
        self.isfill = isfill  # Заливка
        self.bolden = bolden  # Флаг выделения при наведении курсора
        if size == -1:  # Автоматическая генерация размера
            self.resize(self.get_size_text())
        else:
            self.resize(size)
        self.move(*pos)
        self.number = number

        print('True\n', end='') if DEBUG_INFO else None

    def set_text(self, text):
        '''Устанавливает текст'''
        self.text = text

    def set_font(self, font):
        '''Устанавливает шрифт'''
        self.font = pygame.font.Font(None, 16) if font is None else font

    def set_image(self, image):
        '''Устанавливает картинку'''
        self.image = pygame.transform.scale(image, self.size) if image is not None else None

    def set_color(self, color=None, color_active=None, color_text=None):
        '''Устанавливает цвета элементов'''
        if color is not None:
            self.color = color
        if color_active is not None:
            self.color_active = color_active
        if color_text is not None:
            self.color_text = color_text

    def move(self, x, y):
        '''Устанавливает координаты пункта'''
        self.pos = self.x, self.y = x, y

    def resize(self, size):
        '''Меняет размеры'''
        self.size = self.width, self.height = size

    def get_size_text(self):
        self.font.set_bold(True) if self.bolden else None
        size = self.font.size(self.text)
        self.font.set_bold(False) if self.bolden else None
        return size

    def show(self):
        """Показать виджет"""
        self.isshowed = True

    def hide(self):
        """Скрыть виджет"""
        self.isshowed = False

    def connect(self, func):
        """Подключить функцию"""
        self.func = func

    def draw(self, screen, ispressed=False):
        '''Рисует кнопку на screen'''
        if not self.isshowed:
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
            return False
        if not self.get_focused(pos):
            return False
        if not self.isshowed:
            return False
        self.func()
        return True


class AnimatedSpriteForHero(object):
    def init_animation(self, sheet, columns, rows):
        self.std_image = self.image
        self.frames_run = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames_run.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update_animation(self, *args):
        if args[1] == 1 or (args[1] == 0 and args[2] == 1):
            self.cur_frame = (self.cur_frame + 5.7 * args[0] / 1000 * args[3] *
                              len(self.frames_run) / 10) % len(self.frames_run)
            self.image = self.frames_run[int(self.cur_frame)]
        elif args[1] == -1 or (args[1] == 0 and args[2] == -1):
            self.cur_frame = (self.cur_frame + 5.7 * args[0] / 1000 * args[3] *
                              len(self.frames_run) / 10) % len(self.frames_run)
            self.image = pygame.transform.flip(self.frames_run[int(self.cur_frame)], True, False)
        else:
            self.cur_frame = 0
            self.image = self.std_image


class BaseHero(pygame.sprite.Sprite):
    def __init__(self, space, x, y, *groups, image=None):
        super().__init__(*groups)
        self.gamespace = space
        if image is None:
            self.image = pygame.Surface(size=(space.size_cell, space.size_cell))
            self.image.fill(pygame.color.Color('purple'))
        else:
            self.image = image

        self.true_x, self.true_y = space.size_cell * x, space.size_cell * y
        self.rect = self.image.get_rect().move(self.true_x, self.true_y)

        self.take_radius = space.size_cell

        self.mask = pygame.mask.from_surface(self.image)

        self.things = {'cur_weapon': None, 'second_weapon': None,
                       'helmet': None, 'vest': None, 'boots': None,
                       'amulet': None}
        self.sight = 'right'
        self._armor = 0  # Броня
        self.health = 100  # Здоровье
        self._sprint_speed = 2  # Скорость спринта
        self.shields = 100  # Щиты
        self.energy = 100  # Энергия
        self._strength = 1  # Сила
        self._radius = 1  # Радиус
        self._energy_efficiency = 1  # Энергоэфективность
        self._duration = 1  # Длительность

    def attack(self, pos):
        weapon = self.things.get('cur_weapon')
        if weapon is None:
            return
        else:
            weapon.attack(pos)

    def set_pos(self, x, y):  # Установка позиции
        self.rect.x, self.rect.y = self.true_x, self.true_y = (self.gamespace.size_cell * x,
                                                               self.gamespace.size_cell * y)

    def half_damage(self, damage):  # Получение урона
        damage *= (self.armor() / (self.armor() + 300))  # Истинный полученный урон
        if self.shields - damage < 0:
            damage -= self.shields
            self.shields = 0
            self.health -= damage
        else:
            self.shields -= damage

    def change_weapons(self):  # Смена оружия
        self.things['cur_weapon'], self.things['second_weapon'] = (self.things['second_weapon'],
                                                                   self.things['cur_weapon'])

    def take_thing(self, pos):
        thing = None
        for elem in self.gamespace.items_group.sprites():
            if elem.rect.collidepoint(pos):
                thing = elem
        if thing is None:
            return False
        if not ((self.rect.x - thing.rect.x) ** 2 + (self.rect.y - thing.rect.y) ** 2) ** 0.5 < self.take_radius:
            return False
        if thing.type == 'weapon':
            if self.things['cur_weapon'] is None:
                self.things['cur_weapon'] = thing
            elif self.things['second_weapon'] is None:
                self.things['second_weapon'] = thing
            else:
                self.things['cur_weapon'] = thing
        self.things[thing.type] = thing
        return True

    def armor(self):  # Кол-во брони  броня
        return sum(map(lambda key: self.things[key].armor if self.things.get(key) else 0,
                       self.things.keys())) + self._armor

    def sprint_speed(self):  # Скорость спринта
        return sum(map(lambda key: self.things[key].speed if self.things.get(key) else 0,
                       self.things.keys())) + self._sprint_speed

    def strength(self):  # Сила
        return sum(map(lambda key: self.things[key].strength if self.things.get(key) else 0,
                       self.things.keys())) + self._strength

    def radius(self):  # Радиус
        return sum(map(lambda key: self.things[key].radius if self.things.get(key) else 0,
                       self.things.keys())) + self._radius

    def energy_efficiency(self):  # Энергоэфективность
        return sum(map(lambda key: self.things[key].energy_efficiency if self.things.get(key) else 0,
                       self.things.keys())) + self._energy_efficiency

    def duration(self):  # Длительность
        return sum(map(lambda key: self.things[key].duration if self.things.get(key) else 0,
                       self.things.keys())) + self._duration

    def get_moving(self, tick):
        return tick * self.gamespace.size_cell * self.sprint_speed() / 1000


class Player(BaseHero, AnimatedSpriteForHero):
    '''
    Класс игрока
    '''
    def __init__(self, space, x, y):
        image = pygame.transform.scale(space.game.load_image('player\std.png', -1), (space.size_cell, space.size_cell))
        super().__init__(space, x, y, space.all_sprites, image=image)
        sheet = pygame.transform.scale(self.gamespace.game.load_image('player\\animation run 10x1.png', -1),
                                       (space.size_cell * 10, space.size_cell * 1))
        self.init_animation(sheet, 10, 1)
        self._sprint_speed = 2
        print(f'Player(x={x}, y={y}) create True') if DEBUG_INFO else None

    def update(self, *args):
        pressed_keys = pygame.key.get_pressed()
        move_kx = move_ky = 0
        if self.health <= 0:
            # Если здоровье падает до 0 и меньше то игра заканчивается
            self.gamespace.finish_game(message='Закончились жизни')

        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            # Движение вправо если нажата клавиша Right или D
            self.true_x += self.get_moving(args[0])  # Установка новых истенных координат
            self.rect.x = int(self.true_x)  # Установка новых координат квадрата
            # Получения списка стен с которыми игрок пересёкся
            sprite_list = pygame.sprite.spritecollide(self, self.gamespace.walls_group, False)
            if sprite_list:
                # Если было пересечение то перемещение песонажа на максимально маленькое растояние
                self.rect.x = self.true_x = sprite_list[0].rect.x - self.rect.size[0]
            move_kx += 1

        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            # Движение влево если нажата клавиша Left или A
            self.true_x -= self.get_moving(args[0])
            self.rect.x = int(self.true_x)
            sprite_list = pygame.sprite.spritecollide(self, self.gamespace.walls_group, False)
            if sprite_list:
                self.rect.x = self.true_x = sprite_list[0].rect.x + sprite_list[0].rect.size[0]
            move_kx -= 1

        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            # Движение вверх если нажата клавиша Up или W
            self.true_y -= self.get_moving(args[0])
            self.rect.y = int(self.true_y)
            sprite_list = pygame.sprite.spritecollide(self, self.gamespace.walls_group, False)
            if sprite_list:
                self.rect.y = self.true_y = sprite_list[0].rect.y + sprite_list[0].rect.size[1]
            move_ky += 1

        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            # Движение вниз если нажата клавиша Down или S
            self.true_y += self.get_moving(args[0])
            self.rect.y = int(self.true_y)
            sprite_list = pygame.sprite.spritecollide(self, self.gamespace.walls_group, False)
            if sprite_list:
                self.rect.y = self.true_y = sprite_list[0].rect.y - self.rect.size[1]
            move_ky -= 1

        self.update_animation(args[0], move_kx, move_ky, self.sprint_speed())


class Wall(pygame.sprite.Sprite):
    def __init__(self, space, x, y):
        super().__init__(space.all_sprites, space.walls_group)
        self.gamespace = space  # Подключение игрового пространства
        # Создание изображения
        self.image = pygame.transform.scale(space.game.load_image('wall\wall.jpg'), (space.size_cell, space.size_cell))
        # Создание прямоукольника
        self.rect = self.image.get_rect().move(space.size_cell * x, space.size_cell * y)
        print(f'Wall(x={x}, y={y}) create True') if DEBUG_INFO else None


class Tile(pygame.sprite.Sprite):
    def __init__(self, space, x, y):
        super().__init__(space.all_sprites, space.tiles_group)
        self.gamespace = space  # Подключение игрового пространства
        # Создание изображения
        self.image = pygame.transform.scale(space.game.load_image('tile\\tile_1.png'), (space.size_cell, space.size_cell))
        # Создание прямоугольника
        self.rect = self.image.get_rect().move(space.size_cell * x, space.size_cell * y)
        print(f'Tile(x={x}, y={y}) create True') if DEBUG_INFO else None


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, gamespace):
        self.gamespace = gamespace
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        if isinstance(obj, BaseHero):
            obj.true_x += self.dx
            obj.true_y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.gamespace.game.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.gamespace.game.height // 2)


if __name__ == '__main__':
    ex = GameExample()
    ex.mainloop()
