import pygame as pg



class Tile(pg.sprite.Sprite):
    def __init__(self, pos, size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pg.image.load('./level/tile.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, shift):
        self.rect.x += shift
