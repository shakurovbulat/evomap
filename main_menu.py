import pygame
import start_game
from classes import *
from tools import *
import random
import save
import sys


def draw_menu(screen, load_world_img, new_game_img, load_world_rect, new_game_rect):
    screen.fill((30, 30, 30))  # Фон
    screen.blit(load_world_img, load_world_rect)
    screen.blit(new_game_img, new_game_rect)
    pygame.display.flip()


def main_menu(screen, load_world_img, new_game_img, load_world_rect, new_game_rect):
    while True:
        draw_menu(screen, load_world_img, new_game_img, load_world_rect, new_game_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if load_world_rect.collidepoint(mouse_pos):
                    return "load"

                if new_game_rect.collidepoint(mouse_pos):
                    return "new"


def main(screen):
    pygame.display.set_mode((800, 900))
    load_world_img = pygame.image.load("images/load_world.png")
    new_game_img = pygame.image.load("images/new_game.png")
    screen_width, screen_height = 800, 900

    # AmoNGUS AMONGUS"
    load_world_width = 250
    load_world_height = 109  # Увеличиваем высоту для кнопки "Загрузить мир"

    # AmoNGUS AMONGUS"
    load_world_img = pygame.transform.scale(load_world_img, (load_world_width, load_world_height))

    # AmoNGUS AMONGUS
    new_button_width = 250
    new_button_height = 125  # Высота для остальных кнопок

    # AmoNGUS AMONGUS
    new_game_img = pygame.transform.scale(new_game_img, (new_button_width, new_button_height))

    # AmoNGUS AMONGUS
    spacing = 80

    # Позиционируем кнопки с учётом расстояния
    load_world_rect = load_world_img.get_rect(center=(screen_width // 2, screen_height // 2 - 120))
    new_game_rect = new_game_img.get_rect(center=(screen_width // 2, load_world_rect.bottom + spacing - 20))
    game_mode = main_menu(screen, load_world_img, new_game_img, load_world_rect, new_game_rect)

    if game_mode == "load":
        save_file = save.load_game_menu(screen)
        if not save_file:
            sys.exit()
        filename = save_file
        save_file = f'{save_file}/{save_file}'
        saved_game = save.load_game(save_file)
        if saved_game:
            towns, stone, wood, food, rails = saved_game

            mapp = Map()
            for town in towns:
                mapp[town.location[1]][town.location[0]] = town
                resourses_map = town.resourses_map
            image = f'saves/{save_file}.png'
            start_game.main(screen, mapp, resourses_map, stone, wood, food, towns, rails, image,
                            filename)
    elif game_mode == "new":
        mapp = Map()
        height_map = generate_world_map()
        resourses_map = process_matrix([[int((j + 0.5) * 255) for j in i] for i in height_map])
        image = 'realistic_map.png'
        towns = set()

        stone = 100
        wood = 100
        food = 100

        start_x, start_y = random.randint(0, 15), random.randint(0, 15)
        start_town = Town(start_x, start_y, resourses_map)
        mapp[start_y][start_x] = start_town
        towns.add(start_town)
        rails = []
        start_game.main(screen, mapp, resourses_map, stone, wood, food, towns, rails, image, get_name_for_save())