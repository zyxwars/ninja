import pygame as pg


def outline(image):
    mask = pg.mask.from_surface(image)
    outline_image = pg.Surface(image.get_size()).convert_alpha()
    outline_image.fill((0, 0, 0, 0))
    for point in mask.outline():
        outline_image.set_at(point, 'white')
    return outline_image
