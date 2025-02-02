import pygame
from generator import main
import random
import sqlite3
import sys
import os

screen_width = 800
screen_height = 600

# Загрузка изображений кнопок меню
load_world_img = pygame.image.load("images/load_world.png")
continue_game_img = pygame.image.load("images/continue_game.png")
new_game_img = pygame.image.load("images/new_game.png")

# Задаём новый размер кнопки "Загрузить мир"
load_world_width = 250
load_world_height = 109  # Увеличиваем высоту для кнопки "Загрузить мир"

# Масштабируем изображение кнопки "Загрузить мир"
load_world_img = pygame.transform.scale(load_world_img, (load_world_width, load_world_height))

# Задаём размеры для других кнопок
new_button_width = 250
new_button_height = 125  # Высота для остальных кнопок

# Масштабируем изображения для других кнопок
continue_game_img = pygame.transform.scale(continue_game_img, (new_button_width, new_button_height))
new_game_img = pygame.transform.scale(new_game_img, (new_button_width, new_button_height))

# Расстояние между кнопками
spacing = 80

# Позиционируем кнопки с учётом расстояния
load_world_rect = load_world_img.get_rect(center=(screen_width // 2, screen_height // 2 - 120))
continue_game_rect = continue_game_img.get_rect(center=(screen_width // 2, load_world_rect.bottom + spacing))
new_game_rect = new_game_img.get_rect(center=(screen_width // 2, continue_game_rect.bottom + spacing - 20))


def find_save_files(directory="saves"):
    """Ищет все файлы .db в указанной папке"""
    if not os.path.exists(directory):
        os.makedirs(directory)  # Создаём папку, если её нет
    return [f for f in os.listdir(directory) if f.endswith(".db")]


def load_game_menu():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Выбор сохранения")
    font = pygame.font.Font(None, 36)

    files = find_save_files()
    if not files:
        print("Нет сохранений!")
        return None  # Если нет файлов, возврат в меню

    selected = 0  # Индекс выбранного файла

    running = True
    while running:
        screen.fill((30, 30, 30))

        for i, file in enumerate(files):
            color = (255, 255, 255) if i == selected else (180, 180, 180)
            text = font.render(file, True, color)
            screen.blit(text, (50, 50 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(files)  # Переключаем вниз
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(files)  # Переключаем вверх
                elif event.key == pygame.K_RETURN:
                    return f"saves/{files[selected]}"  # Возвращаем путь к файлу


# Функция отрисовки главного меню
def draw_menu():
    screen.fill((30, 30, 30))  # Фон
    screen.blit(load_world_img, load_world_rect)
    screen.blit(continue_game_img, continue_game_rect)
    screen.blit(new_game_img, new_game_rect)
    pygame.display.flip()


# Главное меню
def main_menu():
    while True:
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if load_world_rect.collidepoint(mouse_pos):
                    return "load_world"

                if continue_game_rect.collidepoint(mouse_pos):
                    return "continue_game"

                if new_game_rect.collidepoint(mouse_pos):
                    return "new_game"


def generate_resources_map():
    height_map = generate_world_map()
    return process_matrix([[int((j + 0.5) * 255) for j in i] for i in height_map])


def create_db():
    conn = sqlite3.connect('game_save.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS saves (
                        id INTEGER PRIMARY KEY,
                        level INTEGER,
                        score INTEGER,
                        inventory TEXT,
                        food INTEGER,
                        stone INTEGER,
                        wood INTEGER
                    )''')
    conn.commit()
    conn.close()


def calculate_kefs(x, y, resourses_map):
    x, y = what_cell_resources(x, y)
    res = resourses_map[y][x]
    mi, sr, ma = res
    k_wood, k_stone, k_food = 0, 0, 0
    if sr < 100:
       k_food = 1.5
    elif 100 <= sr <= 180:
        if mi < 100:
            if ma < 180:
                k_wood = 1.2
                k_food = 2
                k_stone = 0.8
            else:
                k_wood = 0.8
                k_food = 0.8
                k_stone = 2
        else:
            if ma < 180:
                k_wood = 2
                k_food = 2
                k_stone = 0.5
            else:
                k_wood = 0.5
                k_food = 0.3
                k_stone = 2
    else:
        k_stone = 3
    return k_wood, k_stone, k_food


def process_matrix(matrix):
    """
    Разбивает матрицу 800x800 на подматрицы 32x32 и заменяет каждую подматрицу
    на список из трёх элементов: [минимум, среднее, максимум].

    :param matrix: Исходная матрица 800x800 (список списков).
    :return: Новая матрица, где каждая подматрица 32x32 заменена на список [минимум, среднее, максимум].
    """
    # Размеры исходной матрицы и подматрицы
    matrix_size = 800
    submatrix_size = 32

    # Количество подматриц по горизонтали и вертикали
    num_submatrices = matrix_size // submatrix_size

    # Результирующая матрица
    result = []

    for i in range(num_submatrices):
        row_result = []
        for j in range(num_submatrices):
            # Выделяем подматрицу 32x32
            submatrix = [
                row[j * submatrix_size:(j + 1) * submatrix_size]
                for row in matrix[i * submatrix_size:(i + 1) * submatrix_size]
            ]

            # Преобразуем подматрицу в одномерный список для удобства
            flat_submatrix = [value for row in submatrix for value in row]

            # Вычисляем минимум, среднее и максимум
            min_value = min(flat_submatrix)
            avg_value = sum(flat_submatrix) / len(flat_submatrix)
            max_value = max(flat_submatrix)

            # Добавляем результат в строку
            row_result.append([min_value, avg_value, max_value])

        # Добавляем строку в результирующую матрицу
        result.append(row_result)

    return result


class Town:
    def __init__(self, x, y, resourses_map):
        self.image = 'images/house4 (2).png'
        self.location = x, y
        self.farm_level = 1
        self.quarry_level = 1
        self.sawmill_level = 1
        self.town_level = 1
        self.population = 100  # Начальное население
        self.food = 100  # Начальная еда
        self.k_wood, self.k_stone, self.k_food = calculate_kefs(x * 16, y * 16, resourses_map)

    def show(self, scr):
        scr.blit(pygame.image.load(self.image), (self.location[0] * 16 - 8, self.location[1] * 16 - 8))

    def upgrade_farm(self):
        self.farm_level += 1

    def set_image(self, image):
        self.image = image

    def upgrade_quarry(self):
        self.quarry_level += 1

    def upgrade_sawmill(self):
        self.sawmill_level += 1

    def upgrade_town(self):
        self.town_level += 1

    def update_population(self):
        global wood, stone
        if self.food > 0:
            if self.population + self.population // 10 < self.town_level * 100:
                self.population += self.population // 10  # Рост населения на 10%
            self.food -= self.population // 10  # Потребление еды
        else:
            self.population -= self.population // 20  # Уменьшение населения, если нет еды
        self.food += int(self.farm_level * self.k_food)
        wood += int(self.sawmill_level * self.k_wood)
        stone += int(self.quarry_level * self.k_stone)

    def upgrade_resurses(self):
        global wood, stone
        self.food += int(self.farm_level * self.k_food)
        wood += int(self.sawmill_level * self.k_wood)
        stone += int(self.quarry_level * self.k_stone)


def generate_world_map():
    return main()


def what_cell_resources(x, y):
    if 0 <= x <= 800 and 0 <= y <= 800:
        return x // 32, y // 32
    elif 0 <= x <= 800:
        if y < 0:
            return x // 32, 0
        return x // 32, 25
    else:
        if x < 0 and y < 0:
            return 0, 0
        elif x > 800 and y < 0:
            return 25, 0
        elif x < 0 and y > 800:
            return 0, 25
        return 25, 25


def what_cell(x, y):
    if 0 <= x <= 800 and 0 <= y <= 800:
        return x // 16, y // 16
    elif 0 <= x <= 800:
        if y < 0:
            return x // 16, 0
        return x // 16, 50
    else:
        if x < 0 and y < 0:
            return 0, 0
        elif x > 800 and y < 0:
            return 50, 0
        elif x < 0 and y > 800:
            return 0, 50
        return 50, 50


def what_cell_rail(x, y):
    if 0 <= x <= 800 and 0 <= y <= 800:
        return x // 8, y // 8
    elif 0 <= x <= 800:
        if y < 0:
            return x // 8, 0
        return x // 8, 100
    else:
        if x < 0 and y < 0:
            return 0, 0
        elif x > 800 and y < 0:
            return 100, 0
        elif x < 0 and y > 800:
            return 0, 100
        return 100, 100


class Map:
    def __init__(self):
        self.map = [[0] * 64 for _ in range(64)]
        self.map_rails = [[0] * 100 for _ in range(100)]

    def set_map(self, x, y, elem):
        self.map[y][x] = elem

    def get_map(self):
        return self.map

    def __getitem__(self, index):
        return self.map[index]

    def __setitem__(self, index, value):
        self.map[index] = value

    def set_map_rails(self, x, y, elem):
        self.map_rails[y][x] = elem

    def get_map_rails_elem(self, x, y):
        return self.map_rails[y][x]

    def get_map_rails(self):
        return self.map_rails


class Rail:
    def __init__(self, from_, to, points):
        self.points = points
        self.from_ = from_
        self.to = to

    def show(self, scr):
        for i in range(1, len(self.points) - 1):
            name = ''
            x_fr, y_fr = self.points[i - 1]
            x, y = self.points[i]
            x_to, y_to = self.points[i + 1]
            from_, to = '', ''
            if x_fr < x:
                from_ = 'з'
            elif x_fr > x:
                from_ = 'в'
            else:
                if y_fr < y:
                    from_ = 'с'
                else:
                    from_ = 'ю'
            if x > x_to:
                to = 'з'
            elif x < x_to:
                to = 'в'
            else:
                if y > y_to:
                    to = 'с'
                else:
                    to = 'ю'
            if from_ == to:
                continue
            if f'{from_}-{to}' not in ['в-з', 'в-с', 'в-ю', 'з-с', 'з-ю', 'с-ю', 'ю-с']:
                from_, to = to, from_
            name = f'images/rails/{from_}-{to}.png'
            scr.blit(pygame.image.load(name), (self.points[i][0] * 8 - 2, self.points[i][1] * 8 - 2))

    def get_points(self):
        return self.points

    def set_point(self, point):
        self.points.append(point)

    def get_connect(self):
        return {self.from_, self.to}

    def set_to(self, to):
        self.to = to


def draw_grid(screen, width, height, cell_size):
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, (100, 100, 100), (x, 0), (x, height), 1)
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, (100, 100, 100), (0, y), (width, y), 1)


pygame.init()

# Создаём окно сразу, чтобы меню могло его использовать
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Стратегическая игра")

# Вызов главного меню перед началом игры
game_mode = main_menu()


def save_game(level, score, inventory, towns, stone, wood, food):
    conn = sqlite3.connect('game_save.db')
    cursor = conn.cursor()

    # Сохраняем общую информацию о игре, включая ресурсы
    cursor.execute('''INSERT OR REPLACE INTO saves (id, level, score, inventory, stone, wood, food) 
                      VALUES (1, ?, ?, ?, ?, ?, ?)''', (level, score, inventory, stone, wood, food))

    # Сохраняем информацию о городах
    cursor.execute('''CREATE TABLE IF NOT EXISTS towns (
                        id INTEGER PRIMARY KEY,
                        x INTEGER,
                        y INTEGER,
                        farm_level INTEGER,
                        quarry_level INTEGER,
                        sawmill_level INTEGER,
                        town_level INTEGER,
                        population INTEGER,
                        food INTEGER
                    )''')

    # Очищаем старые данные о городах
    cursor.execute('DELETE FROM towns')

    # Сохраняем данные о каждом городе
    for town in towns:
        cursor.execute('''INSERT INTO towns (x, y, farm_level, quarry_level, sawmill_level, town_level, population, food)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (town.location[0], town.location[1], town.farm_level, town.quarry_level, town.sawmill_level,
                        town.town_level, town.population, town.food))

    conn.commit()
    conn.close()


def load_game():
    conn = sqlite3.connect('game_save.db')
    cursor = conn.cursor()

    # Загружаем общую информацию о игре, включая ресурсы
    cursor.execute('SELECT level, score, inventory, stone, wood, food FROM saves WHERE id = 1')
    result = cursor.fetchone()

    if result:
        level, score, inventory, stone, wood, food = result  # Загружаем ресурсы

        # Загружаем информацию о городах
        cursor.execute('SELECT x, y, farm_level, quarry_level, sawmill_level, town_level, population, food FROM towns')
        towns_data = cursor.fetchall()

        # Генерируем карту ресурсов
        resourses_map = generate_resources_map()

        towns = set()
        for town_data in towns_data:
            x, y, farm_level, quarry_level, sawmill_level, town_level, population, food = town_data
            town = Town(x, y, resourses_map)
            town.farm_level = farm_level
            town.quarry_level = quarry_level
            town.sawmill_level = sawmill_level
            town.town_level = town_level
            town.population = population
            town.food = food
            towns.add(town)

        conn.close()
        return level, score, inventory, towns, resourses_map, stone, wood, food
    else:
        conn.close()
        return None


if game_mode == "load_world":
    save_file = load_game_menu()  # Вызываем меню выбора файла
    if not save_file:
        print("Файл не выбран. Возврат в меню.")
        sys.exit()

    conn = sqlite3.connect(save_file)
    cursor = conn.cursor()

    # Загружаем данные из сохранения
    cursor.execute('SELECT level, score, inventory, stone, wood, food FROM saves WHERE id = 1')
    result = cursor.fetchone()

    if result:
        level, score, inventory, stone, wood, food = result

        cursor.execute('SELECT x, y, farm_level, quarry_level, sawmill_level, town_level, population, food FROM towns')
        towns_data = cursor.fetchall()

        resourses_map = generate_resources_map()
        towns = set()
        for town_data in towns_data:
            x, y, farm_level, quarry_level, sawmill_level, town_level, population, food = town_data
            town = Town(x, y, resourses_map)
            town.farm_level = farm_level
            town.quarry_level = quarry_level
            town.sawmill_level = sawmill_level
            town.town_level = town_level
            town.population = population
            town.food = food
            towns.add(town)

        conn.close()

        print(f"Игра загружена из {save_file}: уровень {level}, очки {score}, камни: {stone}, дерево: {wood}, еда: {food}")

        # Запускаем игровой процесс
        mapp = Map()
        for town in towns:
            mapp[town.location[1]][town.location[0]] = town

    else:
        conn.close()
        print("Ошибка: сохранение повреждено или пустое.")
        sys.exit()

elif game_mode == "new_game":
    print("Начало новой игры...")
    mapp = Map()
    resourses_map = generate_resources_map()
    towns = set()  # Создаём пустой список городов для новой игры
    stone = 100
    wood = 100
    food = 100
    # Размещение начального города
    start_x, start_y = random.randint(0, 15), random.randint(0, 15)
    start_town = Town(start_x, start_y, resourses_map)
    mapp[start_y][start_x] = start_town
    towns.add(start_town)

if game_mode == "continue_game":
    saved_game = load_game()
    if saved_game:
        level, score, inventory, towns, resourses_map, stone, wood, food = saved_game  # Загружаем ресурсы
        print(f"Продолжение игры: уровень {level}, очки {score}, инвентарь: {inventory}, камни: {stone}, дерево: {wood}, еда: {food}")

        # Восстанавливаем состояние игры
        mapp = Map()

        # Восстанавливаем города на карте
        for town in towns:
            mapp[town.location[1]][town.location[0]] = town

    else:
        print("Нет сохранений, начинайте новую игру.")
        sys.exit()

# Продолжение настройки игры
screen_width, screen_height = 800, 800
expanded_width = 1000  # Новая ширина окна при расширении
screen = pygame.display.set_mode((screen_width, screen_height))
image = pygame.image.load('realistic_map.png')
i_x, i_y = 0, 0
dragging = False
running = True
screen.blit(image, (0, 0))
rails = []


selected_town = None
ctrl = False
creating_rail = None

# Кнопки улучшений
button_font = pygame.font.SysFont(None, 24)
buttons = [
    {"text": "Ферма", "rect": pygame.Rect(820, 10, 160, 30), "action": "farm"},
    {"text": "Шахта", "rect": pygame.Rect(820, 50, 160, 30), "action": "quarry"},
    {"text": "Лесопилка", "rect": pygame.Rect(820, 90, 160, 30), "action": "sawmill"},
    {"text": "Уровень города", "rect": pygame.Rect(820, 130, 160, 30), "action": "town"}
]

# Таймер для обновления населения и еды
UPDATE_INTERVAL = 10000
UPDATE_RES_INTERVAL = 2000 # Интерва\л в миллисекундах (10 секунд)
last_update_time = pygame.time.get_ticks()
last_update_res_time = pygame.time.get_ticks()

while running:
    current_time = pygame.time.get_ticks()
    res_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:  # Сохраняем игру по нажатию F5
                create_db()
                save_game(1, 0, "inventory", towns, stone, wood, food)  # Теперь передаём ресурсы
                print("Игра сохранена!")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x1, y1 = event.pos
                x, y = what_cell(*event.pos)
                f = True
                if selected_town:
                    for button in buttons:
                        if button["rect"].collidepoint(event.pos):
                            f = False
                            if button["action"] == "farm" and stone >= 10 * selected_town.farm_level and wood >= 20 * selected_town.farm_level:
                                stone -= 10 * selected_town.farm_level
                                wood -= 20 * selected_town.farm_level
                                selected_town.upgrade_farm()
                            elif button["action"] == "quarry" and stone >= 10 * selected_town.farm_level and wood >= 20 * selected_town.farm_level:
                                stone -= 10 * selected_town.farm_level
                                wood -= 20 * selected_town.farm_level
                                selected_town.upgrade_quarry()
                            elif button["action"] == "sawmill" and stone >= 10 * selected_town.farm_level and wood >= 20 * selected_town.farm_level:
                                stone -= 10 * selected_town.farm_level
                                wood -= 20 * selected_town.farm_level
                                selected_town.upgrade_sawmill()
                            elif button["action"] == "town" and stone >= 30 * selected_town.farm_level and wood >= 30 * selected_town.farm_level:
                                stone -= 30 * selected_town.farm_level
                                wood -= 30 * selected_town.farm_level
                                selected_town.upgrade_town()
                if isinstance(mapp[y][x], Town):
                    f = False
                    selected_town = mapp[y][x]
                    screen = pygame.display.set_mode((expanded_width, screen_height))
                if f and 0 <= x1 <= 800 and 0 <= y1 <= 800:
                    selected_town = None
                    screen = pygame.display.set_mode((screen_width, screen_height))
            elif event.button == 3:
                if selected_town:
                    if selected_town.population >= 100 and selected_town.food >= 100 and stone >= 50 and wood >= 50:
                        x, y = what_cell(*event.pos)
                        if mapp[y][x] == 0:
                            wood, stone = wood - 50, stone - 50
                            selected_town.population -= 100
                            selected_town.food -= 100
                            town = Town(x, y)
                            mapp[y][x] = Town(x, y)
                            towns.add(town)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                x, y = what_cell(*event.pos)
                f = True
                if isinstance(mapp[y][x], Town):
                    if creating_rail:
                        creating_rail.set_to(mapp[y][x])
                        if creating_rail.get_connect() not in [i.get_connect() for i in rails]:
                            f = False
                            rails.append(creating_rail)
                            dragging = False
                if f:
                    for x in range(100):
                        for y in range(100):
                            if mapp.get_map_rails_elem(x, y) == creating_rail:
                                mapp.set_map_rails(x, y, 0)
                    creating_rail = None
                    dragging = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                ctrl = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                ctrl = False

    for town in towns:
        town.set_image('images/house4 (2).png')

    x, y = what_cell(*pygame.mouse.get_pos())
    if isinstance(mapp[y][x], Town):
        for town in towns:
            if town.location == mapp[y][x].location:
                town.set_image('images/selected/house4 (2).png')
                break

    if dragging:
        if what_cell_rail(*pygame.mouse.get_pos()) not in creating_rail.get_points():
            x, y = what_cell_rail(*pygame.mouse.get_pos())
            mapp.set_map_rails(x, y, creating_rail)
            creating_rail.set_point(what_cell_rail(*pygame.mouse.get_pos()))

    # Обновление населения и еды раз в 10 секунд
    if current_time - last_update_time >= UPDATE_INTERVAL:
        for town in towns:
            town.update_population()
        last_update_time = current_time  # Обновляем время последнего обновления

    # Обновление населения и еды раз в 10 секунд
    if res_time - last_update_res_time >= UPDATE_RES_INTERVAL:
        for town in towns:
            town.upgrade_resurses()
        last_update_res_time = res_time  # Обновляем время последнего обновления

    screen.blit(image, (0, 0))
    if creating_rail:
        creating_rail.show(screen)
    for i in rails:
        i.show(screen)
    for i in towns:
        i.show(screen)
    screen.blit(button_font.render(f'wood: {wood}                 stone: {stone}', True, (255, 255, 255)), (10, 750))

    if selected_town:
        for town in towns:
            if town.location == selected_town.location:
                selected_town = town
        pygame.draw.rect(screen, (50, 50, 50), (800, 0, 200, 800))  # Фон панели
        info_text = [
            f"Ферма: {selected_town.farm_level}",
            f"Шахта: {selected_town.quarry_level}",
            f"Лесопилка: {selected_town.sawmill_level}",
            f"Уровень города: {selected_town.town_level}",
            f"Население: {selected_town.population}",
            f"Еда: {selected_town.food}",
            f'kefs: {selected_town.k_wood, selected_town.k_stone, selected_town.k_food}'
        ]
        for idx, text in enumerate(info_text):
            info_surface = button_font.render(text, True, (255, 255, 255))
            screen.blit(info_surface, (810, 170 + idx * 30))


        # Отрисовка кнопок улучшений
        for button in buttons:
            pygame.draw.rect(screen, (0, 128, 255), button["rect"])
            text_surface = button_font.render(button["text"], True, (255, 255, 255))
            screen.blit(text_surface, (button["rect"].x + 10, button["rect"].y + 5))

    if ctrl:
        draw_grid(screen, screen_width, screen_height, 16)

    pygame.display.flip()

pygame.quit()