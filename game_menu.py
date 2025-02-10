import pygame
import sys
from classes import Button, Town
import main_menu as mm
from params import *
import save
import game_running
import json


DARK_GRAY = (47, 47, 47)
WHITE = (255, 255, 255)
HOVER_COLOR = (70, 70, 70)
BUTTON_BORDER = (100, 100, 100)
WIDTH = 800
HEIGHT = 1000


def continue_game():
    pass


def quit_game(screen):
    pygame.quit()
    sys.exit()


def save_game(screen):
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    name_for_save = data['name_for_save']
    stone = data['stone']
    wood = data['wood']
    food = data['food']
    towns = []
    for town_data in data["towns"]:
        town = {i: town_data[i] for i in town_data}
        towns.append(town)
    rails = []
    for rail_data in data["rails"]:
        rail = {i: rail_data[i] for i in rail_data}
        rails.append(rail)
    print()
    save.save_game(name_for_save, towns, stone, wood, food, rails)


def return_to_main_menu(screen):
    mm.main(screen)


def create_menu(font, button_font, screen):
    buttons = []

    # Создаем кнопки
    button_width = 300
    button_height = 50
    spacing = 5
    start_y = (HEIGHT - (4 * button_height + 3 * spacing)) // 2
    buttons.append(Button((WIDTH - button_width) // 2, start_y + 2 * (button_height + spacing),
                          button_width, button_height,
                          "Выйти в главное меню", HOVER_COLOR, DARK_GRAY, button_font, return_to_main_menu, screen))

    buttons.append(Button((WIDTH - button_width) // 2, start_y + 3 * (button_height + spacing),
                          button_width, button_height,
                          "Сохранить игру", HOVER_COLOR, DARK_GRAY, button_font, save_game, screen))

    buttons.append(Button((WIDTH - button_width) // 2, start_y + 4 * (button_height + spacing),
                          button_width, button_height,
                          "Выход из игры", HOVER_COLOR, DARK_GRAY, button_font, quit_game, screen))

    return buttons


def main_menu(screen):
    pygame.display.set_mode((800, 900))
    buttons = create_menu(font, button_font, screen)
    running = True

    while running:
        screen.fill(DARK_GRAY)

        # Рисуем заголовок
        title = font.render("Главное меню", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(title, title_rect)

        # Обработка событий и отрисовка кнопок
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            for button in buttons:
                button.handle_event(event)

        # Отрисовка кнопок
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

    pygame.quit()