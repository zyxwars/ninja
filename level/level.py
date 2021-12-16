import pygame as pg

from entities.player.player import Player
from .tile import Tile
import config


class Level:
    def __init__(self, surface):
        self.surface = surface
        self.player = pg.sprite.GroupSingle()
        self.tiles = pg.sprite.Group()

        self.shift = pg.math.Vector2(0, 0)

        self.setup()

    def setup(self):
        with open('./level/level.txt', encoding='utf-8') as f:
            for row_index, row in enumerate(f):
                for col_index, tile in enumerate(row):
                    if tile == '1':
                        self.tiles.add(
                            Tile((col_index * config.TILE_SIZE, row_index, config.TILE_SIZE)))
                    if tile == '2':
                        self.player.add(
                            Player((col_index * config.TILE_SIZE, row_index, config.TILE_SIZE), (64, 64)))

    def update(self):
        self.tiles.draw(self.surface)

        player_pos = self.player.sprite.update(
            self.tiles.sprites(), self.surface)
        self.player.draw(self.surface)
