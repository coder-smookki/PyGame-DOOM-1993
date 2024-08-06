import os
import pygame

"""
Загрузка и отображение картинки
"""


def load_image(file_name, name, color_key=-1):
    fullname = os.path.join(file_name, name)
    image = pygame.image.load(fullname)

    if color_key == -1:
        color_key = image.get_at((0, 0))

    image.set_colorkey(color_key)
    return image
