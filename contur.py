from PIL import Image


def outline_image(input_path, output_path):
    # Открываем изображение и преобразуем его в формат RGBA
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()

    width, height = img.size

    # Создаем список для хранения координат пикселей, которые нужно закрасить
    to_paint = set()  # Используем set для исключения дубликатов

    # Проходим по всем пикселям изображения
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]

            # Проверяем, является ли текущий пиксель непрозрачным
            if a != 0:  # Непрозрачный пиксель
                # Проверяем всех соседей (включая диагонали)
                neighbors = [
                    (x - 1, y), (x + 1, y),  # слева и справа
                    (x, y - 1), (x, y + 1),  # сверху и снизу
                    (x - 1, y - 1), (x + 1, y - 1),  # диагонали
                    (x - 1, y + 1), (x + 1, y + 1)
                ]

                for nx, ny in neighbors:
                    # Проверяем, находится ли соседний пиксель в пределах изображения
                    if 0 <= nx < width and 0 <= ny < height:
                        nr, ng, nb, na = pixels[nx, ny]
                        if na == 0:  # Если соседний пиксель прозрачный
                            to_paint.add((nx, ny))

    # Закрашиваем найденные пиксели нужным цветом
    outline_color = (255, 255, 254, 255)  # Цвет обводки
    for x, y in to_paint:
        pixels[x, y] = outline_color

    # Сохраняем результат
    img.save(output_path)


# Пример использования
input_image_path = 'images/stone.png'  # Путь к исходному изображению
output_image_path = 'images/selected/stone.png'  # Путь к выходному изображению

outline_image(input_image_path, output_image_path)