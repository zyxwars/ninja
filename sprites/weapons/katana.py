import pygame as pg

from .weapon import Weapon


class Katana(Weapon):
    def __init__(self, pos, *args, **kwargs):
        self.image = pg.Surface((32, 32))
        self.image.fill('orange')
        super().__init__(100, 500, self.image.get_rect(topleft=pos), *args, **kwargs)
