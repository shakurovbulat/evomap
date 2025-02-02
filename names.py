import os


def list_files_in_directory(directory_path):
    try:
        # Получаем список всех элементов в папке
        files = os.listdir(directory_path)

        # Фильтруем только файлы (исключаем папки)
        files = [f.replace('.png', '') for f in files if os.path.isfile(os.path.join(directory_path, f))]

        # Выводим список файлов
        if files:
            print(f"Файлы в папке '{directory_path}':")
            print(files)
        else:
            print(f"В папке '{directory_path}' нет файлов.")
    except FileNotFoundError:
        print(f"Папка '{directory_path}' не найдена.")
    except PermissionError:
        print(f"Нет доступа к папке '{directory_path}'.")


# Укажите путь к папке
directory_path = "images/rails"

# Вызов функции
list_files_in_directory(directory_path)