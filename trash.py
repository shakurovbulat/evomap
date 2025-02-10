# def get_filename_input():
#     pygame.init()
#     screen = pygame.display.set_mode((600, 200))
#     pygame.display.set_caption("Введите имя сохранения")
#     font = pygame.font.Font(None, 36)
#
#     input_text = ""
#     running = True
#     while running:
#         screen.fill((30, 30, 30))
#         text_surface = font.render("Введите имя сохранения: " + input_text, True, (255, 255, 255))
#         screen.blit(text_surface, (20, 80))
#         pygame.display.flip()
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN:
#                     return input_text  # Возвращаем введённое имя
#                 elif event.key == pygame.K_BACKSPACE:
#                     input_text = input_text[:-1]  # Удаление символа
#                 elif event.unicode.isalnum():
#                     input_text += event.unicode  # Добавляем букву/цифру
#
#
# def find_save_files(directory="saves"):
#     """Ищет все файлы .db в указанной папке"""
#     if not os.path.exists(directory):
#         os.makedirs(directory)  # Создаём папку, если её нет
#     return [f for f in os.listdir(directory) if f.endswith(".json")]
#
#
# def load_game_menu():
#     pygame.init()
#     screen = pygame.display.set_mode((600, 400))
#     pygame.display.set_caption("Выбор сохранения")
#     font = pygame.font.Font(None, 36)
#
#     files = [f[:-5] for f in os.listdir("saves") if f.endswith(".json")]
#     if not files:
#         print("Нет сохранений!")
#         return None
#
#     selected = 0
#
#     running = True
#     while running:
#         screen.fill((30, 30, 30))
#
#         for i, file in enumerate(files):
#             color = (255, 255, 255) if i == selected else (180, 180, 180)
#             text = font.render(file, True, color)
#             screen.blit(text, (50, 50 + i * 40))
#
#         pygame.display.flip()
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_DOWN:
#                     selected = (selected + 1) % len(files)
#                 elif event.key == pygame.K_UP:
#                     selected = (selected - 1) % len(files)
#                 elif event.key == pygame.K_RETURN:
#                     return files[selected]  # Возвращаем имя файла без .json
#
#
# # Функция отрисовки главного меню
# def draw_menu():
#     screen.fill((30, 30, 30))  # Фон
#     screen.blit(load_world_img, load_world_rect)
#     screen.blit(continue_game_img, continue_game_rect)
#     screen.blit(new_game_img, new_game_rect)
#     pygame.display.flip()
#
#
# # Главное меню
# def main_menu():
#     while True:
#         draw_menu()
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_pos = pygame.mouse.get_pos()
#
#                 if load_world_rect.collidepoint(mouse_pos):
#                     return "load_world"
#
#                 if continue_game_rect.collidepoint(mouse_pos):
#                     return "continue_game"
#
#                 if new_game_rect.collidepoint(mouse_pos):
#                     return "new_game"
#
#
# pygame.init()
# load_world_img = pygame.image.load("images/load_world.png")
# continue_game_img = pygame.image.load("images/continue_game.png")
# new_game_img = pygame.image.load("images/new_game.png")
# screen_width, screen_height = 800, 900
# expanded_width = 1000
#
# # Задаём новый размер кнопки "Загрузить мир"
# load_world_width = 250
# load_world_height = 109  # Увеличиваем высоту для кнопки "Загрузить мир"
#
# # Масштабируем изображение кнопки "Загрузить мир"
# load_world_img = pygame.transform.scale(load_world_img, (load_world_width, load_world_height))
#
# # Задаём размеры для других кнопок
# new_button_width = 250
# new_button_height = 125  # Высота для остальных кнопок
#
# # Масштабируем изображения для других кнопок
# continue_game_img = pygame.transform.scale(continue_game_img, (new_button_width, new_button_height))
# new_game_img = pygame.transform.scale(new_game_img, (new_button_width, new_button_height))
#
# # Расстояние между кнопками
# spacing = 80
#
# # Позиционируем кнопки с учётом расстояния
# load_world_rect = load_world_img.get_rect(center=(screen_width // 2, screen_height // 2 - 120))
# continue_game_rect = continue_game_img.get_rect(center=(screen_width // 2, load_world_rect.bottom + spacing))
# new_game_rect = new_game_img.get_rect(center=(screen_width // 2, continue_game_rect.bottom + spacing - 20))

mapp = Map()
height_map = generate_world_map()
resourses_map = process_matrix([[int((j + 0.5) * 255) for j in i] for i in height_map])
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
game_mode = main_menu()

# # Размещение начального города
# def save_game(filename, towns, stone, wood, food):
#     """Сохраняет игру в JSON-файл."""
#     save_data = {
#         "resources": {
#             "stone": stone,
#             "wood": wood,
#             "food": food
#         },
#         "towns": []
#     }
#
#     for town in towns:
#         save_data["towns"].append({
#             "x": town.location[0],
#             "y": town.location[1],
#             "farm_level": town.farm_level,
#             "quarry_level": town.quarry_level,
#             "sawmill_level": town.sawmill_level,
#             "town_level": town.town_level,
#             "population": town.population,
#             "food": town.food
#         })
#
#     os.makedirs("saves", exist_ok=True)  # Создаём папку saves, если её нет
#     with open(f"saves/{filename}.json", "w", encoding="utf-8") as f:
#         json.dump(save_data, f, indent=4)
#
#     print(f"Игра сохранена в {filename}.json")
#
#
# def load_game(filename):
#     """Загружает игру из JSON-файла."""
#     try:
#         with open(f"saves/{filename}.json", "r", encoding="utf-8") as f:
#             save_data = json.load(f)
#     except FileNotFoundError:
#         print(f"Ошибка: Файл {filename}.json не найден.")
#         return None
#
#     stone = save_data["resources"]["stone"]
#     wood = save_data["resources"]["wood"]
#     food = save_data["resources"]["food"]
#
#     height_map = generate_world_map()
#     resourses_map = process_matrix([[int((j + 0.5) * 255) for j in i] for i in height_map])
#     towns = set()
#     for town_data in save_data["towns"]:
#         x, y = town_data["x"], town_data["y"]
#         town = Town(x, y)
#         town.farm_level = town_data["farm_level"]
#         town.quarry_level = town_data["quarry_level"]
#         town.sawmill_level = town_data["sawmill_level"]
#         town.town_level = town_data["town_level"]
#         town.population = town_data["population"]
#         town.food = town_data["food"]
#         towns.add(town)
#
#     print(f"Игра загружена из {filename}.json")
#     return towns, resourses_map, stone, wood, food
#
#
# if game_mode == "load_world":
#     save_file = load_game_menu()
#     if not save_file:
#         print("Файл не выбран. Возврат в меню.")
#         sys.exit()
#
#     saved_game = load_game(save_file)
#     if saved_game:
#         towns, resourses_map, stone, wood, food = saved_game
#
#         print(f"Игра загружена: камни: {stone}, дерево: {wood}, еда: {food}")
#
#         # Запускаем игровой процесс
#         mapp = Map()
#         for town in towns:
#             mapp[town.location[1]][town.location[0]] = town
#
#     else:
#         print("Ошибка: сохранение повреждено.")
#         sys.exit()
# elif game_mode == "new_game":
#     print("Начало новой игры...")
#     mapp = Map()
#     height_map = generate_world_map()
#     resourses_map = process_matrix([[int((j + 0.5) * 255) for j in i] for i in height_map])
#     towns = set()  # Создаём пустой список городов для новой игры
#     stone = 100
#     wood = 100
#     food = 100
#     # Размещение начального города
#     start_x, start_y = random.randint(0, 15), random.randint(0, 15)
#     start_town = Town(start_x, start_y)
#     mapp[start_y][start_x] = start_town
#     towns.add(start_town)
#
# if game_mode == "continue_game":
#     save_file = "autosave"
#
#     saved_game = load_game(save_file)
#     if saved_game:
#         towns, resourses_map, stone, wood, food = saved_game
#         print(f"Продолжение игры: камни: {stone}, дерево: {wood}, еда: {food}")
#
#         # Восстанавливаем игровую карту
#         mapp = Map()
#         for town in towns:
#             mapp[town.location[1]][town.location[0]] = town
#     else:
#         print("Нет автосохранения. Начинаем новую игру.")
#         mapp = Map()
#         resourses_map = generate_resources_map()
#         towns = set()  # Создаём пустой список городов для новой игры
#         stone = 100
#         wood = 100
#         food = 100
#         # Размещение начального города
#         start_x, start_y = random.randint(0, 15), random.randint(0, 15)
#         start_town = Town(start_x, start_y, resourses_map)
#         mapp[start_y][start_x] = start_town
#         towns.add(start_town)
molot_image = pygame.image.load('images/molot.png')
resurses = pygame.image.load('images/resurses.png')
molot_image_x = range(802, 834)
molot_image_y = range(768, 800)
build_rails = pygame.image.load('images/build_rails.png')
build_rails_x = range(802, 834)
build_rails_y = range(736, 768)
font = pygame.font.Font(None, 24)
FOOD_UPDATE_INTERVAL = 4000  # 10 секунд
last_food_update = pygame.time.get_ticks()

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