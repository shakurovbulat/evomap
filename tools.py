from generator import main
import json
from params import *
import os


def get_name_for_save(save_folder="saves"):
    # Проверяем, существует ли папка saves
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)  # Создаем папку, если её нет
        return "game1"  # Если папка пустая, возвращаем game1

    # Получаем список файлов в папке
    files = os.listdir(save_folder)

    # Ищем файлы, начинающиеся с "game" и имеющие числовой суффикс
    max_number = 0
    for file in files:
        file = file.replace('.json', '')
        if file.startswith("game") and file[4:].isdigit():
            number = int(file[4:])  # Извлекаем число из имени файла
            if number > max_number:
                max_number = number

    # Возвращаем следующее имя
    return f"game{max_number + 1}"


def draw_table(surface, x, y, n1, n2, n3, screen_width=800, screen_height=800):
    # Создаём текстовые поверхности
    text1 = font.render(f"Кэф_дерева: {n1:.2f}", True, (255, 255, 255))
    text2 = font.render(f"Кэф_камня: {n2:.2f}", True, (255, 255, 255))
    text3 = font.render(f"Кэф_еды: {n3:.2f}", True, (255, 255, 255))

    # Рассчитываем размеры таблицы
    padding = 10
    text_height = text1.get_height()
    table_width = max(text1.get_width(), text2.get_width(), text3.get_width()) + 2*padding
    table_height = 3*text_height + 4*padding

    # Начальная позиция (над курсором)
    table_x = x
    table_y = y - table_height - 10  # Смещение вверх

    # Корректировка позиции по горизонтали
    if table_x + table_width > screen_width:
        table_x = screen_width - table_width - 10  # Правая граница
    elif table_x < 0:
        table_x = 10  # Левая граница

    # Корректировка позиции по вертикали
    if table_y < 0:
        table_y = y + 20  # Если не влезает сверху, показываем снизу
    elif table_y + table_height > screen_height:
        table_y = screen_height - table_height - 10  # Нижняя граница

    # Рисуем фон
    pygame.draw.rect(surface, (100, 100, 100), (table_x, table_y, table_width, table_height))
    pygame.draw.rect(surface, (0, 0, 0), (table_x, table_y, table_width, table_height), 2)

    # Располагаем текст
    y_offset = padding
    for text in [text1, text2, text3]:
        surface.blit(text, (table_x + padding, table_y + y_offset))
        y_offset += text_height + padding


def calculate_kefs(x, y, resourses_map):
    x, y = what_cell_resources(x, y)
    res = resourses_map[y][x]
    mi, sr, ma = res
    k_wood, k_stone, k_food = 0, 0, 0
    res_color = (0, 0, 100)
    k_wood = 3 * (1 - max(50 - mi, 0) / 50) * (1 - abs(sr - 100) / 80) * (1 - max(ma - 180, 0) / 75)
    k_wood = max(0, min(k_wood, 3))
    k_stone = 3 * (max(sr - 100, 0) / 80) * (max(ma - 100, 0) / 80) * max((200 - mi) / 100, 0)
    k_stone = max(0, min(k_stone, 3))
    k_food = 3 * (1 - abs(sr - 150) / 100) * (1 - max(100 - mi, 0) / 100) * (1 - max(ma - 200, 0) / 55)
    k_food = max(0, min(k_food, 3))
    return round(k_wood, 1), round(k_stone, 1), round(k_food, 1)


def process_matrix(matrix):
    # Размеры исходной матрицы и подматрицы
    matrix_size = 800
    submatrix_size = 32

    # Количество подматриц по горизонтали и вертикали
    num_submatrices = matrix_size // submatrix_size

    # Результирующая матрица
    result = []

    for i in range(num_submatrices):
        row_result = []
        for j in range(num_submatrices):
            # Выделяем подматрицу 32x32
            submatrix = [
                row[j * submatrix_size:(j + 1) * submatrix_size]
                for row in matrix[i * submatrix_size:(i + 1) * submatrix_size]
            ]

            # Преобразуем подматрицу в одномерный список для удобства
            flat_submatrix = [value for row in submatrix for value in row]

            # Вычисляем минимум, среднее и максимум
            min_value = min(flat_submatrix)
            avg_value = sum(flat_submatrix) / len(flat_submatrix)
            max_value = max(flat_submatrix)

            # Добавляем результат в строку
            row_result.append([min_value, avg_value, max_value])

        # Добавляем строку в результирующую матрицу
        result.append(row_result)

    return result


def generate_world_map():
    return main()


def what_cell_resources(x, y):
    if 0 <= x <= 800 and 0 <= y <= 800:
        return x // 32, y // 32
    elif 0 <= x <= 800:
        if y < 0:
            return x // 32, 0
        return x // 32, 25
    else:
        if x < 0 and y < 0:
            return 0, 0
        elif x > 800 and y < 0:
            return 25, 0
        elif x < 0 and y > 800:
            return 0, 25
        return 25, 25


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


def draw_grid(screen, width, height, cell_size):
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, (100, 100, 100), (x, 0), (x, height), 1)
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, (100, 100, 100), (0, y), (width, y), 1)
