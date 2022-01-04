import csv
import math
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
        self.background = pg.image.load(
            utils.get_path(__file__, 'assets/bg.png')).convert_alpha()
        self.background = self._make_scrollable(
            self.background, scale_by_x=False)

        self.background2 = pg.image.load(
            utils.get_path(__file__, 'assets/trees.png')).convert_alpha()
        self.background2 = self._make_scrollable(self.background2)

        self.camera_pos = pg.math.Vector2(
            config.SCREEN_CENTER[0], config.SCREEN_CENTER[1] + 100)
        self.shift = pg.math.Vector2(0, 0)
        self.last_player_pos = (0, 0)

        self.load_level(level_path)

    @staticmethod
    def _make_scrollable(surface: pg.surface.Surface, scale_by_x=True):
        new_surface = pg.Surface(
            (surface.get_width() * 2, surface.get_height()), pg.SRCALPHA)
        new_surface.blit(surface, (0, 0))
        new_surface.blit(surface, (math.ceil(new_surface.get_width() / 2), 0))

        w = new_surface.get_width()
        h = new_surface.get_height()

        w_scale = math.ceil(config.SCREEN_WIDTH / (w / 2))
        h_scale = math.ceil(config.SCREEN_HEIGHT / h)

        scale = w_scale
        if not scale_by_x:
            scale = max(w_scale, h_scale)

        print(scale)

        return pg.transform.smoothscale(new_surface, (w * scale, h * scale))

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

        # Python modulo returns -12 % 7 as 2, c_mod returns -5
        # The scrolling doesn't work when shift is positive
        screen_surface.blit(
            self.background, (0 + utils.c_mod((self.shift[0] * 0.2), self.background.get_width() / 2), -100))

        screen_surface.blit(
            self.background2, (0 + utils.c_mod((self.shift[0] * 0.3), self.background2.get_width() / 2), 0))

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
        self.shift[0] = min(self.shift[0], 0)
        self.shift[1] = min(self.shift[1], 0)

        debug.debug('shift', self.shift)
        self.last_player_pos = player_pos
