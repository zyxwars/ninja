import pygame as pg

from utils import get_path
import config


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, tile_type,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tile_type = tile_type

        # Load image
        try:
            # Tile is foreground if tile_type is positive, otherwise it is in the background
            self.image = pg.image.load(
                get_path(__file__, f'assets/tile/{abs(tile_type) if  isinstance(tile_type, int) else tile_type}.png')).convert_alpha()
        except FileNotFoundError:
            self.image = pg.Surface((config.TILE_SIZE, config.TILE_SIZE))
            self.image.fill('#ff00ff')

        self.rect = self.image.get_rect(topleft=pos)

    def set_type(self, tile_type):
        self.tile_type = tile_type

    def colliderect(self, rect):
        # Return false if tile is part of the background
        if self.tile_type < 0:
            return False

        return self.rect.colliderect(rect)
