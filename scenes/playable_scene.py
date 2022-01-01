import csv
import pygame as pg
from entities import player

from entities.player.player import Player
from .tile import Tile
import config
import game
from utils import debug
import utils


class PlayableScene:
    def __init__(self, level_path):
        self.player = pg.sprite.GroupSingle()
        self.tiles = pg.sprite.Group()

        self.camera_pos = pg.math.Vector2(
            config.SCREEN_CENTER[0], config.SCREEN_CENTER[1] + 100)
        self.shift = pg.math.Vector2(0, 0)

        self.load_level(level_path)

    def load_level(self, level_path):
        with open(level_path, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            for row_index, row in enumerate(reader):
                for col_index, tile_type in enumerate(row):
                    if not tile_type.lstrip('+-').isdigit():
                        if tile_type == 'player':
                            self.player.add(
                                Player((col_index * config.TILE_SIZE, row_index * config.TILE_SIZE), (64, 64)))
                        continue
                    tile_type = int(tile_type)
                    if tile_type == 0:
                        continue
                    self.tiles.add(
                        Tile((col_index * config.TILE_SIZE, row_index * config.TILE_SIZE), tile_type))

    def update(self, screen_surface):
        screen_surface.fill('black')

        for tile in self.tiles.sprites():
            tile.draw(screen_surface, self.shift)

        # ".sprite" is needed because the function returns player_pos
        player_pos = self.player.sprite.update(
            self.tiles.sprites())
        self.player.sprite.draw(screen_surface, self.shift)

        self.shift[0] += ((self.camera_pos.x -
                           (player_pos[0] + self.shift[0])) / config.CAMERA_X_SPEED) * game.delta_time
        self.shift[1] += ((self.camera_pos.y -
                           (player_pos[1] + self.shift[1])) / config.CAMERA_Y_SPEED) * game.delta_time
