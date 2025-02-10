import pygame
import os
import sys
import json
from PIL import Image
from classes import Town, Rail


def load_game_menu(screen):
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 900
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    BLUE = (0, 128, 255)
    font = pygame.font.Font(None, 36)
    saves_folder = "saves"
    if not os.path.exists(saves_folder):
        os.makedirs(saves_folder)
    files = [f for f in os.listdir(saves_folder)]
    if not files:
        files = ["(Нет сохранений)"]

    def draw_buttons(file_list, selected_index):
        screen.fill(WHITE)
        button_height = 50
        button_margin = 10
        total_height = len(file_list) * (button_height + button_margin)
        start_y = (SCREEN_HEIGHT - total_height) // 2
        for i, file_name in enumerate(file_list):
            button_rect = pygame.Rect(
                SCREEN_WIDTH // 4,
                start_y + i * (button_height + button_margin),
                SCREEN_WIDTH // 2,
                button_height
            )
            color = BLUE if i == selected_index else GRAY
            pygame.draw.rect(screen, color, button_rect)
            text = font.render(file_name, True, BLACK)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)

    selected_index = 0
    running = True
    while running:
        draw_buttons(files, selected_index)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(files)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(files)
                elif event.key == pygame.K_RETURN:  # Выбор файла
                    selected_file = files[selected_index]
                    if selected_file != "(Нет сохранений)":
                        return selected_file  # Возвращаем выбранное имя файла
                    else:
                        print("Нет доступных файлов для выбора.")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    mouse_x, mouse_y = event.pos
                    button_height = 50
                    button_margin = 10
                    total_height = len(files) * (button_height + button_margin)
                    start_y = (SCREEN_HEIGHT - total_height) // 2
                    for i, file_name in enumerate(files):
                        button_rect = pygame.Rect(
                            SCREEN_WIDTH // 4,
                            start_y + i * (button_height + button_margin),
                            SCREEN_WIDTH // 2,
                            button_height
                        )
                        if button_rect.collidepoint(mouse_x, mouse_y):
                            if file_name != "(Нет сохранений)":
                                return file_name  # Возвращаем выбранное имя файла
                            else:
                                print("Нет доступных файлов для выбора.")


def load_game(filename):
    filename = filename.replace('.json', '')
    try:
        with open(f"saves/{filename}.json", "r", encoding="utf-8") as f:
            save_data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename}.json не найден.")
        return None

    stone = save_data["resources"]["stone"]
    wood = save_data["resources"]["wood"]
    food = save_data["resources"]["food"]
    towns = set()
    rails = []
    for town_data in save_data["towns"]:
        x, y, resourses_map = town_data["x"], town_data["y"], town_data['resourses_map']
        town = Town(x, y, resourses_map)
        town.farm_level = town_data["farm_level"]
        town.quarry_level = town_data["quarry_level"]
        town.sawmill_level = town_data["sawmill_level"]
        town.town_level = town_data["town_level"]
        town.population = town_data["population"]
        town.food = town_data["food"]
        towns.add(town)

    for rail_data in save_data["rails"]:
        from_, to, points = rail_data["from_"], rail_data["to"], rail_data["points"]
        for town in towns:
            if list(town.location) == from_:
                from_ = town
                break
        for town in towns:
            if list(town.location) == to:
                to = town
                break
        rail = Rail(from_, to, points)
        rails.append(rail)

    return towns, stone, wood, food, rails


def save_game(filename, towns, stone, wood, food, rails):
    if not os.path.isdir(f'saves/{filename}'):
        os.mkdir(f'saves/{filename}')
    img = Image.open('realistic_map.png')
    img.save(f'saves/{filename}/{filename}.png')
    save_data = {
        "resources": {
            "stone": stone,
            "wood": wood,
            "food": food
        },
        "towns": towns,
        "rails": rails
    }
    os.makedirs("saves", exist_ok=True)  # Создаём папку saves, если её нет
    with open(f"saves/{filename}/{filename}.json", "w", encoding="utf-8") as f:
        json.dump(save_data, f, indent=4)

    print(f"Игра сохранена в {filename}.json")