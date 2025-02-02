import pygame
from generator import main
import random


def draw_table(surface, x, y, n1, n2, n3, screen_width=800, screen_height=800):
    """
    Рисует табличку с коэффициентами, всегда остающуюся в пределах экрана.
    """
    # Создаём текстовые поверхности
    text1 = font.render(f"Кэф_дерева: {n1:.2f}", True, (255, 255, 255))
    text2 = font.render(f"Кэф_камня: {n2:.2f}", True, (255, 255, 255))
    text3 = font.render(f"Кэф_еды: {n3:.2f}", True, (255, 255, 255))

    # Рассчитываем размеры таблицы
    padding = 10
    text_height = text1.get_height()
    table_width = max(text1.get_width(), text2.get_width(), text3.get_width()) + 2*padding
    table_height = 3*text_height + 4*padding

    # Начальная позиция (над курсором)
    table_x = x
    table_y = y - table_height - 10  # Смещение вверх

    # Корректировка позиции по горизонтали
    if table_x + table_width > screen_width:
        table_x = screen_width - table_width - 10  # Правая граница
    elif table_x < 0:
        table_x = 10  # Левая граница

    # Корректировка позиции по вертикали
    if table_y < 0:
        table_y = y + 20  # Если не влезает сверху, показываем снизу
    elif table_y + table_height > screen_height:
        table_y = screen_height - table_height - 10  # Нижняя граница

    # Рисуем фон
    pygame.draw.rect(surface, (100, 100, 100), (table_x, table_y, table_width, table_height))
    pygame.draw.rect(surface, (0, 0, 0), (table_x, table_y, table_width, table_height), 2)

    # Располагаем текст
    y_offset = padding
    for text in [text1, text2, text3]:
        surface.blit(text, (table_x + padding, table_y + y_offset))
        y_offset += text_height + padding


def calculate_kefs(x, y):
    x, y = what_cell_resources(x, y)
    res = resourses_map[y][x]
    mi, sr, ma = res
    k_wood, k_stone, k_food = 0, 0, 0
    res_color = (0, 0, 100)
    k_wood = 3 * (1 - max(50 - mi, 0) / 50) * (1 - abs(sr - 100) / 80) * (1 - max(ma - 180, 0) / 75)
    k_wood = max(0, min(k_wood, 3))
    k_stone = 3 * (max(sr - 100, 0) / 80) * (max(ma - 100, 0) / 80) * max((200 - mi) / 100, 0)
    k_stone = max(0, min(k_stone, 3))
    k_food = 3 * (1 - abs(sr - 150) / 100) * (1 - max(100 - mi, 0) / 100) * (1 - max(ma - 200, 0) / 55)
    k_food = max(0, min(k_food, 3))
    return round(k_wood, 1), round(k_stone, 1), round(k_food, 1)


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
    def __init__(self, x, y):
        self.image = 'images/house4 (2).png'
        self.location = x, y
        self.farm_level = 1
        self.quarry_level = 1
        self.sawmill_level = 1
        self.town_level = 1
        self.population = 100  # Начальное население
        self.food = 100  # Начальная еда
        self.k_wood, self.k_stone, self.k_food = calculate_kefs(x * 16, y * 16)

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
            if f'{from_}-{to}' not in ['в-з', 'в-с', 'в-ю', 'з-с', 'з-ю', 'с-ю']:
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
mapp = Map()
height_map = generate_world_map()
resourses_map = process_matrix([[int((j + 0.5) * 255) for j in i] for i in height_map])
screen_width, screen_height = 800, 900
expanded_width = 1000  # Новая ширина окна при расширении
screen = pygame.display.set_mode((screen_width, screen_height))
image = pygame.image.load('realistic_map.png')
i_x, i_y = 0, 0
dragging = False
running = True
building_town = False
screen.blit(image, (0, 0))
rails = []
towns = set()

# Начальные ресурсы игрока
stone = 100
wood = 100
food = 100  # Начальная еда

# Размещение начального города
start_x, start_y = random.randint(0, 49), random.randint(0, 49)
start_town = Town(start_x, start_y)
mapp[start_y][start_x] = start_town
towns.add(start_town)
molot_image = pygame.image.load('images/molot.png')
resurses = pygame.image.load('images/resurses.png')
molot_image_x = range(802, 834)
molot_image_y = range(768, 800)
build_rails = pygame.image.load('images/build_rails.png')
build_rails_x = range(802, 834)
build_rails_y = range(736, 768)
font = pygame.font.Font(None, 24)
FOOD_UPDATE_INTERVAL = 100  # 10 секунд
last_food_update = pygame.time.get_ticks()

selected_town = None
ctrl = False
creating_rail = None
choicing_town = False

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x1, y1 = event.pos
                x, y = what_cell(*event.pos)
                f = True
                if choicing_town:
                    creating_rail = Rail(selected_town, None, [])
                    dragging = True
                    choicing_town = False
                if building_town:
                    if mapp[y][x] == 0 and stone > 50 and wood > 50 and selected_town.population and 0 <= x < 50 and 0 <= y < 50:
                        selected_town.population -= 50
                        stone -= 50
                        wood -= 50
                        town = Town(x, y)
                        mapp[y][x] = Town(x, y)
                        towns.add(town)
                    building_town = False
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
                    x2, y2 = event.pos
                    if x2 in molot_image_x and y2 in molot_image_y:
                        building_town = True
                    if x2 in build_rails_x and y2 in build_rails_y:
                        choicing_town = True
                if isinstance(mapp[y][x], Town):
                    f = False
                    selected_town = mapp[y][x]
                    screen = pygame.display.set_mode((expanded_width, screen_height))
                if f and 0 <= x1 <= 800 and 0 <= y1 <= 800:
                    selected_town = None
                    screen = pygame.display.set_mode((screen_width, screen_height))
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

    if current_time - last_food_update >= FOOD_UPDATE_INTERVAL:
        networks = []
        for rail in rails:
            connected = False
            for network in networks:
                if rail.from_ in network or rail.to in network:
                    network.update({rail.from_, rail.to})
                    connected = True
                    break
            if not connected:
                networks.append({rail.from_, rail.to})

        for network in networks:
            total_food = sum(town.food for town in network)
            avg_food = total_food / len(network)
            for town in network:
                town.food = int(avg_food)

        last_food_update = current_time

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

    print([town.food for town in towns])

    screen.blit(image, (0, 0))
    if creating_rail:
        creating_rail.show(screen)
    for i in rails:
        i.show(screen)
    for i in towns:
        i.show(screen)
    screen.blit(resurses, (0, 800))
    screen.blit(button_font.render(str(stone), True, (255, 255, 255)), (120, 840))
    screen.blit(button_font.render(str(wood), True, (255, 255, 255)), (550, 840))
    if building_town:
        x, y = pygame.mouse.get_pos()
        if 0 <= x < 800 and 0 <= y < 800:
            draw_table(screen, x, y, *calculate_kefs(x, y))

    if selected_town:
        for town in towns:
            if town.location == selected_town.location:
                selected_town = town
        pygame.draw.rect(screen, (50, 50, 50), (800, 0, 200, 800))
        pygame.draw.line(screen, (185, 122, 87), (800, 0), (800, 802), width=2)
        pygame.draw.line(screen, (185, 122, 87), (800, 0), (1000, 0), width=2)
        pygame.draw.line(screen, (185, 122, 87), (997, 0), (997, 802), width=2)
        info_text = [
            f"Ферма: {selected_town.farm_level}",
            f"Шахта: {selected_town.quarry_level}",
            f"Лесопилка: {selected_town.sawmill_level}",
            f"Уровень города: {selected_town.town_level}",
            f"Население: {selected_town.population}",
            f"Еда: {selected_town.food}",
            f'Кэф_дерево: {selected_town.k_wood}',
            f'Кэф_камень: {selected_town.k_stone}',
            f'Кэф_еда: {selected_town.k_food}'
        ]
        for idx, text in enumerate(info_text):
            info_surface = button_font.render(text, True, (255, 255, 255))
            screen.blit(info_surface, (830, 170 + idx * 30))


        # Отрисовка кнопок улучшений
        for button in buttons:
            pygame.draw.rect(screen, (0, 128, 255), button["rect"])
            text_surface = button_font.render(button["text"], True, (255, 255, 255))
            screen.blit(text_surface, (button["rect"].x + 10, button["rect"].y + 5))

        screen.blit(molot_image, (802, 768))
        screen.blit(build_rails, (802, 736))

    if ctrl:
        draw_grid(screen, screen_width, screen_height, 32)

    pygame.display.flip()

pygame.quit()