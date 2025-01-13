import pygame
pygame.init()

# Размеры экрана
screen_width, screen_height = 1000, 1000
screen = pygame.display.set_mode((screen_width, screen_height))

# Загрузка изображения
image = pygame.image.load('realistic_map.png')
image_width, image_height = image.get_width(), image.get_height()

# Начальная позиция изображения
i_x, i_y = 0, 0

# Флаг для перетаскивания
dragging = False

# Главный цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                dragging = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                offset_x = mouse_x - i_x
                offset_y = mouse_y - i_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Левая кнопка мыши
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Обновляем позицию изображения с учётом смещения
                new_x = mouse_x - offset_x
                new_y = mouse_y - offset_y

                # Ограничиваем движение изображения в пределах экрана
                new_x = max(min(new_x, 0), screen_width - image_width)
                new_y = max(min(new_y, 0), screen_height - image_height)

                # Обновляем координаты
                i_x, i_y = new_x, new_y

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Отрисовка изображения на новой позиции
    screen.blit(image, (i_x, i_y))

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
