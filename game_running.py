import sys
import json
import pygame
import game_menu
from tools import *
from classes import *
from params import *
import main_menu


def main(screen,
        mapp,
        towns,
        rails,
        last_update_res_time,
        image,
        stone,
        food,
        wood,
        resourses_map,
        name_for_save):
    ui_elements = {
        'buttons': [
            {
                'rect': pygame.Rect(810, 100, 180, 40),
                'text': 'Upgrade Farm',
                'action': 'upgrade_farm'
            },
            {
                'rect': pygame.Rect(810, 150, 180, 40),
                'text': 'Upgrade Quarry',
                'action': 'upgrade_quarry'
            },
            {
                'rect': pygame.Rect(810, 200, 180, 40),
                'text': 'Upgrade Sawmill',
                'action': 'upgrade_sawmill'
            }
        ]
    }

    game_assets = {
        'background': image,
        'town_image': pygame.image.load('images/town.png'),
    }

    game_state = {
        'towns': towns,  # Множество всех городов
        'rails': rails,     # Список всех рельсов
        'wood': wood,     # Начальное количество дерева
        'stone': stone,    # Начальное количество камня
        'food': food,     # Начальное количество еды
        'last_update_time': pygame.time.get_ticks(),  # Время последнего обновления населения
        'last_update_res_time': pygame.time.get_ticks(),  # Время последнего обновления ресурсов
        'last_food_update': pygame.time.get_ticks(),  # Время последнего обновления еды
        'map': mapp,  # Игровая карта (например, список списков)
    }

    # Инициализация состояний
    state = {
        'dragging': False,
        'running': True,
        'building_town': False,
        'selected_town': None,
        'ctrl_pressed': False,
        'creating_rail': None,
        'choicing_town': False
    }

    while state['running']:
        handle_events(state, game_state, ui_elements)
        update_game_state(state, game_state)
        render_game(screen, state, game_assets, game_state, ui_elements)
        pygame.display.flip()


def handle_events(state, game_state, ui_elements):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state['running'] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_down(event, state, game_state, ui_elements)
        elif event.type == pygame.MOUSEBUTTONUP:
            handle_mouse_up(event, state, game_state)
        elif event.type == pygame.KEYDOWN:
            handle_key_down(event, state)
        elif event.type == pygame.KEYUP:
            handle_key_up(event, state)


def handle_mouse_down(event, state, game_state, ui_elements):
    if event.button == 1:
        pos = pygame.mouse.get_pos()
        cell = get_cell(pos)

        if state['choicing_town']:
            start_rail_creation(state, game_state)
            return

        if try_handle_ui_click(pos, state, game_state, ui_elements):
            return

        if try_select_town(cell, state, game_state):
            return

        handle_map_click(cell, state, game_state)


def handle_mouse_up(event, state, game_state):
    if event.button == 1 and state['creating_rail']:
        finalize_rail_creation(event.pos, state, game_state)


def handle_key_down(event, state):
    if event.key == pygame.K_LCTRL:
        state['ctrl_pressed'] = True
    elif event.key == pygame.K_ESCAPE:
        show_game_menu()


def handle_key_up(event, state):
    if event.key == pygame.K_LCTRL:
        state['ctrl_pressed'] = False


def update_game_state(state, game_state):
    current_time = pygame.time.get_ticks()

    # Обновление ресурсов
    if current_time - game_state['last_update_res_time'] >= UPDATE_RES_INTERVAL:
        update_resources(game_state)
        game_state['last_update_res_time'] = current_time

    # Обновление населения
    if current_time - game_state['last_update_time'] >= UPDATE_INTERVAL:
        update_population(game_state)
        game_state['last_update_time'] = current_time

    # Обновление сетей городов
    if current_time - game_state['last_food_update'] >= FOOD_UPDATE_INTERVAL:
        update_food_distribution(game_state)
        game_state['last_food_update'] = current_time


def render_game(screen, state, game_assets, game_state, ui_elements):
    screen.blit(game_assets['background'], (0, 0))

    # Отрисовка игровых объектов
    draw_rails(screen, game_state['rails'])
    draw_towns(screen, game_state['towns'])

    # Отрисовка интерфейса
    draw_ui(screen, game_assets, game_state, state)

    # Отрисовка временных объектов
    if state['creating_rail']:
        draw_temp_rail(screen, state['creating_rail'])

    if state['building_town']:
        draw_building_preview(screen, game_state)


def update_resources(game_state):
    for town in game_state['towns']:
        wood, stone = town.calculate_production()
        game_state['wood'] += wood
        game_state['stone'] += stone


def update_food_distribution(game_state):
    networks = create_city_networks(game_state['rails'])
    for network in networks:
        distribute_food(network)


def create_city_networks(rails):
    networks = []
    for rail in rails:
        merged = False
        for net in networks:
            if rail.connects_to(net):
                net.add_rail(rail)
                merged = True
                break
        if not merged:
            networks.append(CityNetwork(rail))
    return networks


class CityNetwork:
    def __init__(self, initial_rail):
        self.towns = {initial_rail.from_town, initial_rail.to_town}
        self.rails = [initial_rail]

    def connects_to(self, rail):
        return rail.from_town in self.towns or rail.to_town in self.towns

    def add_rail(self, rail):
        self.towns.update({rail.from_town, rail.to_town})
        self.rails.append(rail)


def distribute_food(network):
    total_food = sum(town.food for town in network.towns)
    average_food = total_food // len(network.towns)
    for town in network.towns:
        town.food = average_food

# Остальные вспомогательные функции и классы должны быть реализованы аналогичным образом
