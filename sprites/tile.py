import pygame as pg

from utils.shiftable_sprite import ShiftableSprite


class Tile(ShiftableSprite):
    def __init__(self, pos, image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
