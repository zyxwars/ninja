import pygame as pg

from player.player import Player
from .tile import Tile


class Level:
    def __init__(self, surface):
        self.surface = surface
        self.player = pg.sprite.GroupSingle()
        self.tiles = pg.sprite.Group()

        self.setup()

    def setup(self):
        with open('./level/level.txt', encoding='utf-8') as f:
            for row_index, row in enumerate(f):
                for col_index, tile in enumerate(row):
                    if tile == '1':
                        self.tiles.add(
                            Tile((col_index * 32, row_index*32), (32, 32)))
                    if tile == '2':
                        self.player.add(
                            Player((col_index * 32, row_index*32), (64, 64)))

    def update(self):
        if self.player.sprite.rect.x > 1000 and self.player.sprite.dir.x > 0:
            self.player.sprite.speed = 0
            world_shift = -8
        elif self.player.sprite.rect.x < 200 and self.player.sprite.dir.x < 0:
            self.player.sprite.speed = 0
            world_shift = 8
        else:
            self.player.sprite.speed = 8
            world_shift = 0

        self.tiles.update(world_shift)
        self.tiles.draw(self.surface)

        self.player.sprite.update(self.tiles.sprites(), self.surface)
        self.player.draw(self.surface)
