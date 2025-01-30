import numpy as np
from PIL import Image
import noise
from random import choice, randrange


width, height = 800, 800
scale = 100.0
octaves = 10
persistence = 0.5
lacunarity = 2.4
n = randrange(-200, 200)


def close(num):
    return choice([num + i * j for i in [-1, 1] for j in range(7)])


def generate_height_map(width, height, scale, octaves, persistence, lacunarity):
    height_map = np.zeros((width, height))
    for y in range(height):
        for x in range(width):
            height_map[x][y] = noise.pnoise2(x / scale,
                                             y / scale,
                                             octaves=octaves,
                                             persistence=persistence,
                                             lacunarity=lacunarity,
                                             repeatx=1024,
                                             repeaty=1024,
                                             base=n)
    return height_map


def height_map_to_image(height_map):
    image = Image.new('RGB', (width, height))
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            value = int((height_map[x][y] + 0.5) * 255)
            if value < 60:
                pixels[x, y] = tuple([close(i) for i in [3, 40, 252]])  # Темно-синий (глубокая вода)
            elif value < 80:
                pixels[x, y] = tuple([close(i) for i in [3, 98, 252]])  # Темно-зеленый (низкие равнины)
            elif value < 100:
                pixels[x, y] = tuple([close(i) for i in [3, 132, 252]])  # Оливково-зеленый (высокие равнины)
            elif value < 105:
                pixels[x, y] = tuple([close(i) for i in [255, 235, 105]])
            elif value < 130:
                pixels[x, y] = tuple([close(i) for i in [34, 139, 34]])  # Темно-зеленый (низкие горы)
            elif value < 160:
                pixels[x, y] = tuple([close(i) for i in [0, 128, 0]])  # Очень темно-зеленый (средние горы)
            elif value < 180:
                pixels[x, y] = tuple([close(i) for i in [0, 100, 0]])  # Серый (высокие горы)
            elif value < 200:
                pixels[x, y] = tuple([close(i) for i in [0, 80, 0]])  # Светло-серый (очень высокие горы)
            elif value < 230:
                pixels[x, y] = tuple([close(i) for i in [47, 69, 56]])  # Очень светло-серый (пики гор)
            else:
                pixels[x, y] = tuple([close(i) for i in [187, 191, 188]])  # Белый (снежные вершины)
    return image


def main():
    height_map = generate_height_map(width, height, scale, octaves, persistence, lacunarity)
    image = height_map_to_image(height_map)
    image.save('realistic_map.png')
    return height_map
