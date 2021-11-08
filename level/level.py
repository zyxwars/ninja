import pygame as pg

from player.player import Player
from .tile import Tile
import config


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
        world_shift = self.move_camera()

        self.tiles.update(world_shift)
        self.tiles.draw(self.surface)

        self.player.sprite.update(self.tiles.sprites(), self.surface)
        self.player.draw(self.surface)

    def move_camera(self):
        if self.player.sprite.rect.x > config.SCREEN_WIDTH * 0.8 and self.player.sprite.dir.x > 0:
            self.player.sprite.speed = 0
            world_shift = -1 * config.X_WORLD_SHIFT_SPEED
        elif self.player.sprite.rect.x < config.SCREEN_WIDTH * 0.2 and self.player.sprite.dir.x < 0:
            self.player.sprite.speed = 0
            world_shift = config.X_WORLD_SHIFT_SPEED
        else:
            self.player.sprite.speed = config.PLAYER_SPEED
            world_shift = 0

        return world_shift
