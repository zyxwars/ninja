import pygame as pg


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pg.image.load('./level/assets/tile.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
