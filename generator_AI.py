import numpy as np
from PIL import Image
import noise
from random import randrange

# Параметры карты
width, height = 800, 800
scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0
n = randrange(-400, 400)

# Генерация карты высот
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

# Генерация температурной карты
def generate_temperature_map(width, height):
    temperature_map = np.zeros((width, height))
    for y in range(height):
        for x in range(width):
            # Температура зависит от широты (y) и шума
            temperature_map[x][y] = (1.0 - (y / height)) + 0.1 * noise.pnoise2(x / scale,
                                                                               y / scale,
                                                                               octaves=2,
                                                                               base=n + 1000)
    return temperature_map

# Генерация карты влажности
def generate_humidity_map(width, height):
    humidity_map = np.zeros((width, height))
    for y in range(height):
        for x in range(width):
            # Влажность зависит от шума
            humidity_map[x][y] = noise.pnoise2(x / scale,
                                               y / scale,
                                               octaves=4,
                                               persistence=0.6,
                                               lacunarity=2.0,
                                               base=n + 2000)
    return humidity_map

# Определение биома (как в Minecraft)
def get_biome(temperature, humidity):
    if temperature < 0.2:
        if humidity < 0.3:
            return "Snowy Tundra"  # Снежная тундра
        else:
            return "Taiga"  # Тайга
    elif temperature < 0.5:
        if humidity < 0.4:
            return "Plains"  # Равнины
        else:
            return "Forest"  # Лес
    elif temperature < 0.8:
        if humidity < 0.3:
            return "Desert"  # Пустыня
        else:
            return "Jungle"  # Джунгли
    else:
        if humidity < 0.5:
            return "Savanna"  # Саванна
        else:
            return "Swamp"  # Болото

# Цвета биомов (как в Minecraft)
biome_colors = {
    "Snowy Tundra": (255, 255, 255),  # Белый (снег)
    "Taiga": (34, 139, 34),           # Темно-зеленый (тайга)
    "Plains": (154, 205, 50),         # Светло-зеленый (равнины)
    "Forest": (0, 100, 0),            # Зеленый (лес)
    "Desert": (255, 230, 150),        # Песочный (пустыня)
    "Jungle": (0, 128, 0),            # Темно-зеленый (джунгли)
    "Savanna": (210, 180, 140),       # Бежевый (саванна)
    "Swamp": (47, 79, 79),            # Темно-серый (болото)
}

# Создание изображения
def height_map_to_image(height_map, temperature_map, humidity_map):
    image = Image.new('RGB', (width, height))
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            height_value = (height_map[x][y] + 1) / 2  # Нормализация высоты
            temperature_value = (temperature_map[x][y] + 1) / 2  # Нормализация температуры
            humidity_value = (humidity_map[x][y] + 1) / 2  # Нормализация влажности

            # Определяем биом
            biome = get_biome(temperature_value, humidity_value)

            # Если высота ниже уровня воды, то это вода
            if height_value < 0.4:
                pixels[x, y] = (0, 0, 255)  # Синий (вода)
            else:
                pixels[x, y] = biome_colors[biome]  # Цвет биома
    return image

# Основная функция
def main():
    height_map = generate_height_map(width, height, scale, octaves, persistence, lacunarity)
    temperature_map = generate_temperature_map(width, height)
    humidity_map = generate_humidity_map(width, height)
    image = height_map_to_image(height_map, temperature_map, humidity_map)
    image.save('minecraft_like_map.png')

if __name__ == "__main__":
    main()