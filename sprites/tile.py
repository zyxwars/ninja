import pygame as pg


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
