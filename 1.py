from PIL import Image
import os

# Путь к папке с изображениями
folder_path = 'images'

# Перебираем все файлы в папке
for filename in os.listdir(folder_path):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # Открываем изображение
        img_path = os.path.join(folder_path, filename)
        img = Image.open(img_path)

        # Преобразуем изображение в режим RGBA, если оно не в этом режиме
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # Получаем данные пикселей
        datas = img.getdata()

        new_data = []
        for item in datas:
            # Заменяем белые пиксели на прозрачные
            if item[:3] == (255, 255, 255):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)

        # Обновляем изображение с новыми данными
        img.putdata(new_data)

        # Сохраняем изображение
        img.save(img_path, 'PNG')

print("Обработка завершена.")
