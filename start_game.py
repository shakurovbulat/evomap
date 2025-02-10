import pygame
import game_running
from tools import *


def main(screen, mapp, resourses_map, stone, wood, food, towns, rails, image, name_for_save):
    image = pygame.image.load(image)
    screen.blit(image, (0, 0))
    molot_image = pygame.image.load('images/molot.png')
    resurses = pygame.image.load('images/resurses.png')
    molot_image_x = range(802, 834)
    molot_image_y = range(768, 800)
    build_rails = pygame.image.load('images/build_rails.png')
    build_rails_x = range(802, 834)
    build_rails_y = range(736, 768)
    font = pygame.font.Font(None, 24)
    last_food_update = pygame.time.get_ticks()
    button_font = pygame.font.SysFont(None, 24)
    buttons = [
        {"text": "Ферма", "rect": pygame.Rect(820, 10, 160, 30), "action": "farm"},
        {"text": "Шахта", "rect": pygame.Rect(820, 50, 160, 30), "action": "quarry"},
        {"text": "Лесопилка", "rect": pygame.Rect(820, 90, 160, 30), "action": "sawmill"},
        {"text": "Уровень города", "rect": pygame.Rect(820, 130, 160, 30), "action": "town"}
    ]
    last_update_time = pygame.time.get_ticks()
    last_update_res_time = pygame.time.get_ticks()
    game_running.main(
        screen,
        molot_image,
        resurses,
        molot_image_x,
        molot_image_y,
        build_rails,
        build_rails_x,
        build_rails_y,
        font,
        last_food_update,
        button_font,
        buttons,
        last_update_time,
        mapp,
        towns,
        rails,
        last_update_res_time,
        image,
        stone,
        food,
        wood,
        resourses_map,
        name_for_save)