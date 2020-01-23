import pygame
import os
import sys
from win32api import GetSystemMetrics
from random import randint as rd
from settings_launcher import SettingsWindow, QApplication

# Флаги режимов MODE_MENU, MODE_GAME, MODE_SETTINGS
MODE_MENU, MODE_GAME = 0, 1
DEBUG_INFO = False  # Флаг доп. информации в консоли


class GameExample:
    '''
    Главный класс игры
    '''

    def __init__(self):
        '''Инициализация'''
        print('init Game') if DEBUG_INFO else None
        pygame.init()

        # Создание переменной с функцианалом для музыки
        self.music = pygame.mixer.music

        # Загрузка данных настроек и их обновление
        # Они включают первичную установку режима (полноэкранный или оконный),
        # размеров экрана, загрузку меню и игрового пространства,
        # установка громкости звука
        self.update_settings()

        # Установка титульного имени окна
        pygame.display.set_caption('Knights')

        # Установка иконки
        pygame.display.set_icon(self.load_image('icon.png'))

        # Скрытие курсора
        pygame.mouse.set_visible(False)

        # Некоторые переменныне в игре
        self.mode = None  # Режим окна
        self.image_arrow = pygame.transform.scale(self.load_image('arrow.png', -1), (22, 22))  # Картинка курсора

        self.open_menu()

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
                # Обновление игрового пространства
                self.game_space.update()
                # Рисование ирового пространства
                self.game_space.render(self.main_screen)
            if pygame.mouse.get_focused():
                # Отрисовка курсора
                self.main_screen.blit(self.image_arrow, (pygame.mouse.get_pos()))

            # Обновление дисплея
            pygame.display.flip()

    def update_settings(self):
        print(f'{self.__class__}.update_settings()') if DEBUG_INFO else None
        # Загрузка настроек
        self.data_settings = self.load_settings()

        # Установка громкости музыки
        self.music.set_volume(self.data_settings['volume'])

        # Инициализация разрешения окна
        self.size = self.width, self.height = self.data_settings['matrix']

        # Инициализация режима экрана и главного кадра игры
        self.set_mode_display(self.size, self.data_settings['fullscreen'])

        # Загрузка меню
        self.load_menu()

        # Загруска игрового пространства
        self.load_game_space()

    @staticmethod
    def load_settings():
        result = {}
        with open('data\settings data', encoding='utf8') as file:
            data = file.readlines()
        for elem in data:
            key, val = elem.split()
            if key == 'matrix':
                result[key] = tuple(map(int, val.split('x')))
            elif key == 'fullscreen':
                result[key] = val == 'true'
            elif key == 'volume':
                result[key] = float(val)
        return result

    @staticmethod
    def load_image(name, colorkey=None):
        '''
        Возвращает картинку с именем name. Если есть colorkey, то у картинки делается фон прозрачным.
        Если colorkey == -1 то берётся цвет из самого верхнего угла картинки, иначе ...
        '''
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

        # Создание меню
        self.menu = Menu(self)

        # fonts = ['consolas', 'cuprum', 'gabriola', ''] # Красивые шрифты
        # Пункты меню
        self.menu = Menu(self)  # Создание меню

        # Надпись названия игры
        label_title = Punkt(text='Soul Knight Demo', pos=(int(self.width * 0.5), int(self.height * 0.45)), size=-1,
                            show_background=False, color_text=_Color('white'), number=0,
                            font=_SysFont('gabriola', self.height // 10), bolden=False)
        # Кнопка "Играть"
        btn_play = Punkt(text='Играть', pos=(int(self.width * 0.05), int(self.height * 0.8)), size=-1,
                         show_background=False, color_text=_Color('green'), number=1,
                         font=_SysFont('gabriola', self.height // 20), func=self.start_game)
        # Кнопка "Настройки"
        btn_settings = Punkt(text='Настройки', pos=(int(self.width * 0.3), int(self.height * 0.8)), size=-1,
                             show_background=False, color_text=_Color('white'), number=2,
                             font=_SysFont('gabriola', self.height // 20), func=self.open_settings)
        # Кнопка "Руководство"
        btn_guide = Punkt(text='Руководство', pos=(int(self.width * 0.55), int(self.height * 0.8)), size=-1,
                          show_background=False, color_text=_Color('white'), number=3,
                          font=_SysFont('gabriola', self.height // 20), func=self.open_guide)
        # Кнопка "Выход"
        btn_exit = Punkt(text='Выйти', pos=(int(self.width * 0.8), int(self.height * 0.8)), size=-1,
                         show_background=False, color_text=_Color('red'), number=4,
                         font=_SysFont('gabriola', self.height // 20), func=self.terminate)

        # Добавление пунктов в меню
        self.menu.add_punkts(label_title, btn_play, btn_settings, btn_guide, btn_exit)  # Добавление пунктов

    def load_game_space(self):
        '''Загрузка ирового пространства'''
        print('\tinit game space:\n') if DEBUG_INFO else None
        # Сокращение некоторых функций
        _Font = pygame.font.Font
        _SysFont = pygame.font.SysFont
        _Color = pygame.Color

        # Создание игрового пространства
        self.game_space = GameSpace(self)

        # Кнопка "Exit"
        btn_exit = Punkt(text='Exit', pos=(int(self.width * 0.01), int(self.height * 0.01)), size=-1,
                         show_background=False, color_text=_Color('yellow'), number=5,
                         font=_SysFont('gabriola', self.height // 20), func=self.open_menu)
        # Кнопка "Pause"
        btn_pause = Punkt(text='Pause', pos=(int(self.width * 0.01), int(self.height * 0.07)), size=-1,
                          show_background=False, color_text=_Color('yellow'), number=6,
                          font=_SysFont('gabriola', self.height // 20), func=self.set_pause)
        # Изображение "PAUSE"
        label_pause = Punkt(text='PAUSE', pos=(int(self.width * 0.2), int(self.height * 0.4)), size=-1,
                            show_background=False, color_text=_Color('blue'), number=7, bolden=False,
                            font=_SysFont(None, self.height // 2))
        label_pause.hide()

        # Размеры Punkt у элементов отображения текущего и вторичного оружия
        size = tuple([int(self.height * 0.14)] * 2)

        # Изображение текущего оружия
        label_cur_weapon = Punkt(text='test', pos=(int(self.width * 0.05), int(self.height * 0.6)),
                                 size=size, show_background=False,
                                 number=8)  # func=self.game_space.player.change_weapons  # Привязывается после new_game
        # Изображение второго оружия
        label_second_weapon = Punkt(text='test2', pos=(int(self.width * 0.05), int(self.height * 0.75)),
                                    size=size, show_background=False,
                                    number=9)  # func=self.game_space.player.change_weapons

        # Размеры полосок здоровья и щитов
        size = (int(self.width * 0.2), int(self.height * 0.05))
        # Полоска здоровья
        label_health = Punkt(text='Health: 000', pos=(int(self.width * 0.78), int(self.height * 0.8)), size=size,
                             font=_SysFont('gabriola', int(self.height * 0.05)), bolden=False,
                             color_text=_Color('white'), color=(60, 60, 60),
                             show_background=False, number=10)
        label_health.max_health = 0
        # Полоска щитов
        label_shields = Punkt(text='Shields: 000', pos=(int(self.width * 0.78), int(self.height * 0.8) + size[1]),
                              size=size, font=_SysFont('gabriola', int(self.height * 0.05)), bolden=False,
                              color_text=_Color('white'), color=(60, 60, 60),
                              show_background=False, number=11)
        label_shields.max_shields = 0
        # Полоска энергии
        label_enegy = Punkt(text='Energy: 000', pos=(int(self.width * 0.78), int(self.height * 0.8) + size[1] * 2),
                            size=(size[0], size[1] // 2), color=(60, 60, 60), color_text=_Color('black'),
                            show_background=False, number=12, bolden=False)
        label_enegy.max_energy = 0
        # Показатель брони
        label_armor = Punkt(text='Armor: 00000', pos=(int(self.width * 0.85), int(self.width * 0.05)), size=-1,
                            font=_SysFont('gabriola', int(self.height * 0.05)), bolden=False, show_background=False,
                            number=13, color_text=_Color('white'))
        # Показатель скорости бега
        label_sprint_speed = Punkt(text='Sprint: 0000', font=_SysFont('gabriola', int(self.height * 0.05)),
                                   pos=(int(self.width * 0.85), int(self.width * 0.05 + label_armor.get_size()[1])),
                                   bolden=False, show_background=False, number=14, color_text=_Color('white'))

        self.game_space.add_punkts(btn_exit, btn_pause, label_pause, label_cur_weapon,
                                   label_armor, label_enegy, label_sprint_speed,
                                   label_second_weapon, label_health, label_shields)  # Добавление пунктов

    def mouse_press_event(self, event):
        '''События мыши'''
        print(f'{self.__class__}.mouse_press_event()') if DEBUG_INFO else None
        if self.mode == MODE_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Проверяет элементы после нажатия мышкой кнопкой "1"
                self.menu.check_on_press_punkts(event.pos)

        if self.mode == MODE_GAME:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Проверяет элементы после нажатия мышкой кнопкой "1"
                if self.game_space.check_on_press_punkts(event.pos):
                    # Проверка на нажатие punkt
                    pass
                elif self.game_space.pause_status:
                    # Если пауза то убрать её и больше ничего не делать
                    self.unset_pause()
                elif self.game_space.player.take_thing(event.pos):
                    # Проверка на поднятие вещи в позиции event.pos
                    pass
                else:
                    # Начать атаку позиции event.pos
                    self.game_space.player.attack(event.pos)

    def key_press_event(self, event):
        '''События клавиатуры'''
        print(f'{self.__class__}.key_press_event()') if DEBUG_INFO else None
        if self.mode == MODE_GAME:
            if event.key == pygame.K_p:
                # Установка и убирание паузы при нажатии клавиши P
                if self.game_space.pause_status:
                    self.unset_pause()
                else:
                    self.set_pause()
            elif event.key == pygame.K_ESCAPE:
                # Открытие меню при нажатии на Escape
                self.open_menu()
            elif event.key == pygame.K_f:
                self.game_space.player.change_weapons()

    def start_game(self):
        '''Начать игру'''
        print('GameExample.start_game()') if DEBUG_INFO else None
        self.mode = MODE_GAME  # Установка режима MODE_GAME
        self.game_space.new_game()  # Начало новой игры в game_space
        self.unset_pause()  # Убирание паузы
        self.music.pause()  # Остановка музыки

    def open_menu(self):
        '''Открывает меню'''
        print('GameExample.open_menu()') if DEBUG_INFO else None
        self.mode = MODE_MENU  # Установка режима MODE_MENU
        self.set_pause()  # Установка паузы
        self.music.load('data\music\main_menu.mp3')
        self.music.play(-1)

    def open_settings(self):
        '''Открывает настройки'''
        print(f'{self.__class__}.open_settings()') if DEBUG_INFO else None
        # os.startfile('settings launcher.exe')
        # self.music.pause()
        app = QApplication(sys.argv)
        settings_window = SettingsWindow(self)
        app.exec_()
        for _ in pygame.event.get():
            pass
        if not pygame.display.get_active():
            pygame.display.iconify()
        self.update_settings()
        # self.music.unpause()

    def open_guide(self):
        '''Открывает руководство'''
        print(f'{self.__class__}.open_guide()') if DEBUG_INFO else None

    def set_mode_display(self, size, bool_full_screen):
        '''Устанавливает полноэкранный и неполноэкранный режим'''
        if bool_full_screen:
            self.main_screen = pygame.display.set_mode(size,
                                                       pygame.HWSURFACE |
                                                       pygame.DOUBLEBUF |
                                                       pygame.FULLSCREEN)
        else:
            self.main_screen = pygame.display.set_mode(size)

    def set_pause(self):
        '''Устанавливает паузу в GameSpace'''
        print(f'{self.__class__}.set_pause()') if DEBUG_INFO else None
        self.game_space.pause_status = True
        self.game_space.get_punkt(5).hide()
        self.game_space.get_punkt(6).hide()
        self.game_space.get_punkt(7).show()

    def unset_pause(self):
        '''Убирает паузу в GameSpace'''
        print(f'{self.__class__}.unset_pause()') if DEBUG_INFO else None
        self.game_space.pause_status = False
        self.game_space.get_punkt(5).show()
        self.game_space.get_punkt(6).show()
        self.game_space.get_punkt(7).hide()

    def start_screen_opening(self):
        '''Зашрузочная заставка'''
        print(f'{self.__class__}.start_screen_opening()') if DEBUG_INFO else None
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.main_screen.fill(pygame.color.Color('black'))
            pygame.display.flip()

    @staticmethod
    def terminate():
        '''Выход из игры, и завершение главного цикла'''
        print('terminate()') if DEBUG_INFO else None
        pygame.quit()
        print('-----Game closed-----') if DEBUG_INFO else None
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
        '''Добавление 1 пункта'''
        self.punkts.append(punkt)

    def add_punkts(self, *punkts):
        '''Добавление нескольких пунктов'''
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
        self.size_cell = int(self.game.height * 0.2)

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
        '''Добавляет 1 пункт'''
        self.punkts.append(punkt)

    def add_punkts(self, *punkts):
        '''Добавляет несколько пунктов'''
        self.punkts += list(punkts)

    def check_on_press_punkts(self, pos):
        '''Проверяет пункты на нажатиe'''
        for punkt in self.punkts:
            if punkt.on_click(pos):
                return True
        return False

    def new_game(self):
        '''Сбрасывает предыдущий прогресс и данные'''
        print(f'{self.__class__}.new_game()') if DEBUG_INFO else None

        self.levels.clear()
        self.load_levels('test')
        self.player = Player(self, 0, 0)

        # Подключение функций персонажа и его показателей к пунктам:
        cur_weapon_punkt = self.get_punkt(8)  # Текущее оружие
        cur_weapon_punkt.connect(self.player.change_weapons)

        second_weapon_punkt = self.get_punkt(9)  # Второе оружие
        second_weapon_punkt.connect(self.player.change_weapons)

        health_punkt = self.get_punkt(10)  # Полоска здоровья
        health_punkt.max_health = self.player.health

        shield_punkt = self.get_punkt(11)  # Полоска щитов
        shield_punkt.max_shields = self.player.shields

        energy_punkt = self.get_punkt(12)  # Полоска энергии
        energy_punkt.max_energy = self.player.energy

        self.update_interface()  # Обновление интерфейса

        self.level_x, level_y = self.generate_level(self.get_next_level())
        self.clock = pygame.time.Clock()

    def get_next_level(self):
        '''Получение следующего уровня'''
        try:
            return self.levels.pop(0)
        except IndexError:
            return None

    def finish_game(self, message=None):
        '''Заканчивает игру'''
        print(f'{self.__class__}.finish_game()') if DEBUG_INFO else None
        self.game.open_menu()

    def update_interface(self):
        '''обновление боевого интерфейса'''
        # Текущее оружие
        cur_weapon_punkt = self.get_punkt(8)
        cur_weapon = self.player.things['cur_weapon']
        if cur_weapon is not None:
            image_cur_weapon = pygame.Surface(size=cur_weapon_punkt.get_size())
            pygame.draw.rect(image_cur_weapon, pygame.color.Color('green'), (0, 0, *cur_weapon_punkt.get_size()), 2)
            image_cur_weapon.blit(cur_weapon.image)
            cur_weapon_punkt.set_image(image_cur_weapon)
            cur_weapon_punkt.show()
        else:
            cur_weapon_punkt.hide()

        # Второе оружие
        second_weapon_punkt = self.get_punkt(9)
        second_weapon = self.player.things['second_weapon']
        if second_weapon is not None:
            image_second_weapon = pygame.Surface(size=second_weapon_punkt.get_size())
            pygame.draw.rect(image_second_weapon, pygame.color.Color('gray'), (0, 0, *second_weapon_punkt.get_size()),
                             2)
            image_second_weapon.blit(second_weapon.image)
            second_weapon_punkt.set_image(image_second_weapon)
            second_weapon_punkt.show()
        else:
            second_weapon_punkt.hide()

        # Полоска здоровья
        health_punkt = self.get_punkt(10)
        image_health = pygame.Surface(size=health_punkt.get_size())
        image_health.fill(pygame.color.Color('#800000'))
        pygame.draw.rect(image_health, pygame.color.Color('#FF0000'),
                         (0, 0, image_health.get_width() * (self.player.health / health_punkt.max_health),
                          image_health.get_height()))
        health_punkt.set_image(image_health)
        health_punkt.set_text(f'Health: {round(self.player.health)}')

        # Полоска щитов
        shields_punkt = self.get_punkt(11)
        image_shields = pygame.Surface(size=shields_punkt.get_size())
        image_shields.fill(pygame.color.Color('#000080'))
        pygame.draw.rect(image_shields, pygame.color.Color('#0000FF'),
                         (0, 0, image_shields.get_width() * (self.player.shields / shields_punkt.max_shields),
                          image_shields.get_height()))
        shields_punkt.set_image(image_shields)
        shields_punkt.set_text(f'Shields: {round(self.player.shields)}')

        # Полоска энергии
        energy_punkt = self.get_punkt(12)
        image_energy = pygame.Surface(size=energy_punkt.get_size())
        image_energy.fill(pygame.color.Color('#008080'))
        pygame.draw.rect(image_energy, pygame.color.Color('#00FFFF'),
                         (0, 0, image_energy.get_width() * (self.player.energy / energy_punkt.max_energy),
                          image_energy.get_height()))
        energy_punkt.set_image(image_energy)
        energy_punkt.set_text(f'Energy: {round(self.player.energy)}')

        # Показатель брони
        armor_punkt = self.get_punkt(13)
        armor_punkt.set_text(f'Armor: {round(self.player.armor())}')

        sprint_punkt = self.get_punkt(14)
        sprint_punkt.set_text(f'Sprint: {round(self.player.sprint_speed())}')

    def update(self):
        '''Обновляет данные игры'''
        if self.pause_status is True:
            return

        tick = self.clock.tick()  # Получения момента времени
        self.player_group.update(tick)  # Обновление персонажа

        self.update_interface()  # Обновление интерфейса
        # Обновление камеры
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

        print('\tFinish generate level') if DEBUG_INFO else None
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
            [print([print(row) for row in level]) for level in self.levels] if DEBUG_INFO else None

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

    def __init__(self, text=None, pos=(0, 0), size=-1, font=None, color=(100, 100, 100), show_background=True,
                 color_active=(0, 255, 255), color_text=(0, 0, 0), func=None, number=0, bolden=True):
        '''Инициализация'''
        print(f'\t\tinit punct text: "{text}"", number: "{number}" : ', end='') if DEBUG_INFO else None

        self.set_text(text)  # Установка текста
        self.set_font(font)  # Установка шрифта
        self.connect(func)  # Подключение функции

        self.set_color(color, color_active, color_text)  # Установка цветов элементов

        self.show_background = show_background  # Заливка
        self.bolden = bolden  # Флаг выделения при наведении курсора
        self.number = number  # Установка номера

        self.set_pos(*pos)  # Установка позиции
        # Установка размера виджета. Если указан size == -1, то размер установится
        # минимальным возможным для отображения надписи
        self.resize(self.get_size_text() if size == -1 else size)

        self.set_image(None)  # Установка картинки
        self.show()  # Отображение

        print('True\n', end='') if DEBUG_INFO else None

    def get_size(self):
        '''Возвращает размеры'''
        return self.size

    def get_size_text(self):
        '''Возвращает размеры текста'''
        self.font.set_bold(True) if self.bolden else None
        size = self.font.size(self.text)
        self.font.set_bold(False) if self.bolden else None
        return size

    def set_text(self, text):
        '''Устанавливает текст'''
        self.text = text

    def set_font(self, font):
        '''Устанавливает шрифт'''
        self.font = pygame.font.Font(None, 16) if font is None else font

    def set_image(self, image):
        '''Устанавливает картинку'''
        self.image = image

    def set_color(self, color=None, color_active=None, color_text=None):
        '''Устанавливает цвета элементов'''
        if color is not None:
            # Цвет неактивного фона
            self.color = color
        if color_active is not None:
            # Цвет активного фона
            self.color_active = color_active
        if color_text is not None:
            # Цвет текста
            self.color_text = color_text

    def set_pos(self, x, y):
        '''Устанавливает координаты пункта'''
        self.pos = self.x, self.y = x, y

    def resize(self, size):
        '''Меняет размеры'''
        self.size = self.width, self.height = size

    def show(self):
        '''Показать виджет'''
        self.isshowed = True

    def hide(self):
        '''Скрыть виджет'''
        self.isshowed = False

    def connect(self, func):
        '''Подключить функцию'''
        self.func = func

    def draw(self, screen, ispressed=False):
        '''Рисует кнопку на screen'''
        if not self.isshowed:
            # Не рисует если пункт скрыт
            return
        surface = pygame.Surface(size=self.get_size())
        if self.show_background:  # Заливка области
            color_background = self.color if not ispressed or not self.bolden else self.color_active
            surface.fill(color_background)
        else:  # Преобразование в прозрачный фон
            surface.fill((1, 0, 0))
            surface.set_colorkey((1, 0, 0))
            surface.convert_alpha()

        if self.image is not None:  # наложение картинки если есть она
            surface.blit(self.image, (0, 0))

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
        # Картинка персонажа в положении покоя
        self.std_image = self.image
        # Список изображений для анимации бега
        self.frames_run = self.cut_sheet(sheet, columns, rows)
        # Текущий кадр
        self.cur_frame_run = 0

    def cut_sheet(self, sheet, columns, rows):
        '''Разделение доски анимации и возвращение списка кадров'''
        listen = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                listen.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return listen

    def update_animation(self, *args):
        '''Обновление анимации'''
        if args[1] == 1 or (args[1] == 0 and args[2] == 1):
            self.cur_frame_run = (self.cur_frame_run + 5.7 * args[0] / 1000 * args[3] *
                                  len(self.frames_run) / 10) % len(self.frames_run)
            self.image = self.frames_run[int(self.cur_frame_run)]
        elif args[1] == -1 or (args[1] == 0 and args[2] == -1):
            self.cur_frame_run = (self.cur_frame_run + 5.7 * args[0] / 1000 * args[3] *
                                  len(self.frames_run) / 10) % len(self.frames_run)
            self.image = pygame.transform.flip(self.frames_run[int(self.cur_frame_run)], True, False)
        else:
            self.cur_frame_run = 0
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
        # Радиус подбора предметов
        self.take_radius = space.size_cell
        # Маска
        self.mask = pygame.mask.from_surface(self.image)
        # Предметы персонажа
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

        print(f'create {self.__class__.__name__}(x={x}, y={y})') if DEBUG_INFO else None

    def attack(self, pos):
        '''Атака из текущего оружия'''
        print(f'{self.__class__.__name__}().attack(pos={pos})') if DEBUG_INFO else None
        weapon = self.things.get('cur_weapon')
        if weapon is None:
            return
        else:
            weapon.attack(pos)

    def set_pos(self, x, y):
        '''Установка позиции'''
        print(f'{self.__class__}.set_pos(x={x}, y={y})') if DEBUG_INFO else None
        self.rect.x, self.rect.y = self.true_x, self.true_y = (self.gamespace.size_cell * x,
                                                               self.gamespace.size_cell * y)

    def half_damage(self, damage):
        '''Получение урона'''
        print(f'{self.__class__}.half_damge(damage={damage}, ', end='') if DEBUG_INFO else None
        damage -= damage * (self.armor() / (self.armor() + 300))  # Истинный полученный урон
        print(f'true_damage={damage})') if DEBUG_INFO else None
        if self.shields - damage < 0:
            damage -= self.shields
            self.shields = 0
            self.health -= damage
        else:
            self.shields -= damage

    def change_weapons(self):
        '''Смена оружия'''
        print(f'{self.__class__}.change_weapons()') if DEBUG_INFO else None
        self.things['cur_weapon'], self.things['second_weapon'] = (self.things['second_weapon'],
                                                                   self.things['cur_weapon'])

    def take_thing(self, pos):
        '''Подбор вещи'''
        print(f'{self.__class__}.take_thing(pos={pos})') if DEBUG_INFO else None
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

    def get_moving(self, tick):  # Перемещение
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
        print(f'create Wall(x={x}, y={y})') if DEBUG_INFO else None


class Tile(pygame.sprite.Sprite):
    def __init__(self, space, x, y):
        super().__init__(space.all_sprites, space.tiles_group)
        self.gamespace = space  # Подключение игрового пространства
        # Создание изображения
        self.image = pygame.transform.scale(space.game.load_image('tile\\tile_1.png'),
                                            (space.size_cell, space.size_cell))
        # Создание прямоугольника
        self.rect = self.image.get_rect().move(space.size_cell * x, space.size_cell * y)
        print(f'create Tile(x={x}, y={y})') if DEBUG_INFO else None


class Item:
    pass


class Weapon(Item):
    pass


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
