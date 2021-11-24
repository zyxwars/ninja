import pygame as pg


def load_images(base_name, number_of_images, size, output_list):
    for i in range(number_of_images):
        image = pg.image.load(
            f'./player/{base_name}{i+1}.png').convert_alpha()
        image = pg.transform.scale(image, size)
        output_list.append(image)
