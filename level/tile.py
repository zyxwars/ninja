import pygame as pg

from utils import get_path
import config


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, tile_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.image = pg.image.load(
                get_path(__file__, f'assets/tile{tile_type}.png')).convert_alpha()
        except FileNotFoundError:
            self.image = pg.Surface((config.TILE_SIZE, config.TILE_SIZE))
            self.image.fill('#ff00ff')

        self.rect = self.image.get_rect(topleft=pos)
