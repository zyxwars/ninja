import pygame as pg
from .get_path import get_path


def load_animation(script_path, base_name, number_of_images, size=None):
    output_list = []
    for i in range(number_of_images):
        image = pg.image.load(
            get_path(script_path, f'{base_name}{i+1}.png')).convert_alpha()
        if size:
            image = pg.transform.scale(image, size)
        output_list.append(image)

    return output_list
