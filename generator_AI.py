import sys
import json
import pygame

import game_menu
from tools import *
from classes import *
from params import *
import main_menu


def main(
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
        name_for_save):
    dragging = False
    running = True
    building_town = False
    selected_town = None
    ctrl = False
    creating_rail = None
    choicing_town = False
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
                            town = Town(x, y, resourses_map)
                            mapp[y][x] = town
                            towns.add(town)
                        building_town = False
                    if selected_town:
                        for button in buttons:
                            if button["rect"].collidepoint(event.pos):
                                f = False
                                if button[
                                    "action"] == "farm" and stone >= 10 * selected_town.farm_level and wood >= 20 * selected_town.farm_level:
                                    stone -= 10 * selected_town.farm_level
                                    wood -= 20 * selected_town.farm_level
                                    selected_town.upgrade_farm()
                                elif button[
                                    "action"] == "quarry" and stone >= 10 * selected_town.farm_level and wood >= 20 * selected_town.farm_level:
                                    stone -= 10 * selected_town.farm_level
                                    wood -= 20 * selected_town.farm_level
                                    selected_town.upgrade_quarry()
                                elif button[
                                    "action"] == "sawmill" and stone >= 10 * selected_town.farm_level and wood >= 20 * selected_town.farm_level:
                                    stone -= 10 * selected_town.farm_level
                                    wood -= 20 * selected_town.farm_level
                                    selected_town.upgrade_sawmill()
                                elif button[
                                    "action"] == "town" and stone >= 30 * selected_town.farm_level and wood >= 30 * selected_town.farm_level:
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
                elif event.key == pygame.K_ESCAPE:
                    game_menu.main_menu(screen)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    ctrl = False

        for town in towns:
            town.set_image('images/town.png')

        if current_time - last_food_update >= FOOD_UPDATE_INTERVAL:
            if rails:
                # Создаем группы связанных городов
                networks = []
                for rail in rails:
                    connected = False
                    # Ищем сети, связанные с текущими городами рельсов
                    for net in networks:
                        if rail.from_ in net or rail.to in net:
                            net.update({rail.from_, rail.to})
                            connected = True
                            break
                    if not connected:
                        networks.append({rail.from_, rail.to})

                # Объединяем пересекающиеся сети
                merged = True
                while merged:
                    merged = False
                    for i in range(len(networks)):
                        for j in range(i + 1, len(networks)):
                            if networks[i] & networks[j]:  # Если есть общие города
                                networks[i] |= networks[j]
                                del networks[j]
                                merged = True
                                break

                # Обновляем еду в каждой сети
                for net in networks:
                    total = sum(town.food for town in net)
                    avg = total // len(net)
                    for town in net:
                        town.food = avg

                last_food_update = current_time

        x, y = what_cell(*pygame.mouse.get_pos())
        if isinstance(mapp[y][x], Town):
            for town in towns:
                if town.location == mapp[y][x].location:
                    town.set_image('images/selected/town.png')
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
                plus_wood, plus_stone = town.upgrade_resurses()
                wood += plus_wood
                stone += plus_stone
            last_update_res_time = res_time  # Обновляем время последнего обновления

        save_data = {
            "name_for_save": name_for_save,
            "stone": stone,
            "wood": wood,
            "food": food,
            "towns": [],
            "rails": []
        }

        for town in towns:
            save_data["towns"].append({
                "x": town.location[0],
                "y": town.location[1],
                "farm_level": town.farm_level,
                "quarry_level": town.quarry_level,
                "sawmill_level": town.sawmill_level,
                "town_level": town.town_level,
                "population": town.population,
                "food": town.food,
                "resourses_map": town.resourses_map
            })
        for rail in rails:
            save_data["rails"].append({
                "from_": rail.from_.location,
                "to": rail.to.location,
                "points": rail.points
            })

        with open(f"data.json", "w") as f:
            json.dump(save_data, f, indent=4, ensure_ascii=False)

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
                draw_table(screen, x, y, *calculate_kefs(x, y, resourses_map))

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

            screen.blit(button_font.render('Строить город', True, (255, 255, 255)), (834, 780))
            screen.blit(button_font.render('Строить пути', True, (255, 255, 255)), (834, 752))

            screen.blit(molot_image, (802, 768))
            screen.blit(build_rails, (802, 736))

        if ctrl:
            draw_grid(screen, screen_width, screen_height, 32)

        pygame.display.flip()
