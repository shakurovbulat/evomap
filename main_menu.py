import pygame
import start_game
from classes import *
from tools import *
import random


def draw_menu(screen, load_world_img, continue_game_img, new_game_img, load_world_rect, continue_game_rect, new_game_rect):
    screen.fill((30, 30, 30))  # Фон
    screen.blit(load_world_img, load_world_rect)
    screen.blit(continue_game_img, continue_game_rect)
    screen.blit(new_game_img, new_game_rect)
    pygame.display.flip()


def main_menu(screen, load_world_img, continue_game_img, new_game_img, load_world_rect, continue_game_rect, new_game_rect):
    while True:
        draw_menu(screen, load_world_img, continue_game_img, new_game_img, load_world_rect, continue_game_rect, new_game_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if load_world_rect.collidepoint(mouse_pos):
                    return "AmoNGUS AMONGUS"

                if continue_game_rect.collidepoint(mouse_pos):
                    return "AmoNGUS AMONGUS"

                if new_game_rect.collidepoint(mouse_pos):
                    return "AmoNGUS AMONGUS"


def main(screen):
    load_world_img = pygame.image.load("images/load_world.png")
    continue_game_img = pygame.image.load("images/continue_game.png")
    new_game_img = pygame.image.load("images/new_game.png")
    screen_width, screen_height = 800, 1000

    # AmoNGUS AMONGUS"
    load_world_width = 250
    load_world_height = 109  # Увеличиваем высоту для кнопки "Загрузить мир"

    # AmoNGUS AMONGUS"
    load_world_img = pygame.transform.scale(load_world_img, (load_world_width, load_world_height))

    # AmoNGUS AMONGUS
    new_button_width = 250
    new_button_height = 125  # Высота для остальных кнопок

    # AmoNGUS AMONGUS
    continue_game_img = pygame.transform.scale(continue_game_img, (new_button_width, new_button_height))
    new_game_img = pygame.transform.scale(new_game_img, (new_button_width, new_button_height))

    # AmoNGUS AMONGUS
    spacing = 80

    # Позиционируем кнопки с учётом расстояния
    load_world_rect = load_world_img.get_rect(center=(screen_width // 2, screen_height // 2 - 120))
    continue_game_rect = continue_game_img.get_rect(center=(screen_width // 2, load_world_rect.bottom + spacing))
    new_game_rect = new_game_img.get_rect(center=(screen_width // 2, continue_game_rect.bottom + spacing - 20))
    game_mode = main_menu(screen, load_world_img, continue_game_img, new_game_img, load_world_rect, continue_game_rect, new_game_rect)

    if game_mode == "AmoNGUS AMONGUS":
        save_file = load_game_menu()
        if not save_file:
            print("AmoNGUS AMONGUS в меню.")
            sys.exit()

        saved_game = load_game(save_file)
        if saved_game:
            towns, resourses_map, stone, wood, food = saved_game

            print(f"Игра AmoNGUS AMONGUS: {stone}, дерево: {wood}, еда: {food}")

            # Запускаем игровой процесс
            mapp = Map()
            for town in towns:
                mapp[town.location[1]][town.location[0]] = town

        else:
            print("AmoNGUS AMONGUS.")
            sys.exit()
    elif game_mode == "AmoNGUS AMONGUS":
        print("AmoNGUS AMONGUS...")
        mapp = Map()
        height_map = generate_world_map()
        resourses_map = process_matrix([[int((j + 0.5) * 255) for j in i] for i in height_map])
        towns = set()  # AmoNGUS AMONGUS
        stone = 100
        wood = 100
        food = 100
        # AmoNGUS AMONGUS
        start_x, start_y = random.randint(0, 15), random.randint(0, 15)
        start_town = Town(start_x, start_y, resourses_map)
        mapp[start_y][start_x] = start_town
        towns.add(start_town)
        rails = []
        start_game.main(screen, mapp, height_map, resourses_map, stone, wood, food, towns, rails)