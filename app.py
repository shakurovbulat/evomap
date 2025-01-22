import pygame
from generator import main


class Town:
    def __init__(self, x, y):
        self.image = 'images/house4 (2).png'
        self.location = x, y

    def show(self, scr):
        scr.blit(pygame.image.load(self.image), (self.location[0] * 16 - 8, self.location[1] * 16 - 8))


def generate_world_map():
    main()


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
            name = f'images/{from_}-{to}.png'
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

generate_world_map()
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
image = pygame.image.load('realistic_map.png')

i_x, i_y = 0, 0
dragging = False
running = True
screen.blit(image, (0, 0))
ctrl = False
rails = []
towns = set()
creating_rail = None
# rail = Rail(0, 0, [])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = what_cell(*event.pos)
                if isinstance(mapp[y][x], Town):
                    creating_rail = Rail(mapp[y][x], None, [])
                    dragging = True
            elif event.button == 3:
                x, y = what_cell(*event.pos)
                town = Town(x, y)
                mapp[y][x] = Town(x, y)
                towns.add(town)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                x, y = what_cell(*event.pos)
                if isinstance(mapp[y][x], Town):
                    if creating_rail:
                        creating_rail.set_to(mapp[y][x])
                        if creating_rail.get_connect() not in [i.get_connect() for i in rails]:
                            rails.append(creating_rail)
                            dragging = False
                        else:
                            for x in range(100):
                                for y in range(100):
                                    if mapp.get_map_rails_elem(x, y) == creating_rail:
                                        mapp.set_map_rails(x, y, 0)
                            creating_rail = None
                            dragging = False
                    else:
                        for x in range(100):
                            for y in range(100):
                                if mapp.get_map_rails_elem(x, y) == creating_rail:
                                    mapp.set_map_rails(x, y, 0)
                        creating_rail = None
                        dragging = False
                else:
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

    if dragging:
        if what_cell_rail(*pygame.mouse.get_pos()) not in creating_rail.get_points():
            x, y = what_cell_rail(*pygame.mouse.get_pos())
            mapp.set_map_rails(x, y, creating_rail)
            creating_rail.set_point(what_cell_rail(*pygame.mouse.get_pos()))
    screen.blit(image, (0, 0))

    if creating_rail:
        creating_rail.show(screen)

    for i in rails:
        i.show(screen)

    for i in towns:
        i.show(screen)

    if ctrl:
        draw_grid(screen, screen_width, screen_height, 16)

    pygame.display.flip()

pygame.quit()
