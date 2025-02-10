import pygame
from tools import *


class Button:
    def __init__(self, x, y, width, height, text, hover_color, main_color, font, action, screen):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        self.hover_color = hover_color
        self.main_color = main_color
        self.font = font
        self.screen = screen

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.main_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 2, border_radius=8)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and self.action:
                self.action(self.screen)


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


class Town:
    def __init__(self, x, y, resourses_map):
        self.image = 'images/town.png'
        self.location = x, y
        self.farm_level = 1
        self.quarry_level = 1
        self.sawmill_level = 1
        self.town_level = 1
        self.population = 100  # Начальное население
        self.food = 100  # Начальная еда
        self.k_wood, self.k_stone, self.k_food = calculate_kefs(x * 16, y * 16, resourses_map)
        self.resourses_map = resourses_map

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
        if self.food > 0:
            if self.population + self.population // 10 < self.town_level * 100:
                self.population += self.population // 10
            self.food -= self.population // 10
        else:
            self.population -= self.population // 20

    def upgrade_resurses(self):
        self.food += int(self.farm_level * self.k_food)
        wood = int(self.sawmill_level * self.k_wood)
        stone = int(self.quarry_level * self.k_stone)
        return wood, stone


class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        self.parent.setdefault(x, x)
        self.parent.setdefault(y, y)
        fx, fy = self.find(x), self.find(y)
        if fx != fy:
            self.parent[fy] = fx