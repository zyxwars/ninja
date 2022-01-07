import pygame as pg
import json
import math

from sprites.player.player import Player
import config
import game
from utils import debug
from utils.get_path import get_path
from utils.sheet_parser import SheetParser
from sprites.tile import Tile
from utils import ShiftableGroup
import utils


def make_scrollable(surface: pg.surface.Surface, scale_by_x=True):
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

    return pg.transform.smoothscale(new_surface, (w * scale, h * scale))


class PlayableScene:
    def __init__(self, map_path):
        self.bg_img = make_scrollable(pg.image.load(
            get_path(__file__, 'assets/bg.png')))

        self.background = ShiftableGroup()
        # Collidable with player
        self.terrain = ShiftableGroup()
        self.player = None
        self.foreground = ShiftableGroup()

        self.camera_pos = pg.Vector2(
            config.SCREEN_CENTER[0], config.SCREEN_CENTER[1] + 100)
        self.shift = pg.Vector2(0, 0)
        self.last_player_pos = (0, 0)

        self.load_map(map_path)

    def load_map(self, map_path):
        with open(map_path, encoding='utf-8') as f:
            map_data = json.load(f)
            sheet_parser = SheetParser(__file__, 'assets/tileset.png')

            for layer in map_data['layers']:
                if layer['type'] == 'tilelayer':
                    w = layer['width']

                    for i, tile in enumerate(layer['data']):
                        if tile == 0:
                            continue

                        x = i % w * config.TILE_SIZE
                        y = i // w * config.TILE_SIZE

                        # The first tile is 1, but the sheet parser starts with x, y = 0, 0
                        tile = Tile((x, y),
                                    sheet_parser.load_image(((tile - 1) % 10, (tile - 1) // 10)))

                        if 'fg_' in layer['name']:
                            self.foreground.add(tile)
                        elif 'bg_' in layer['name']:
                            self.background.add(tile)
                        else:
                            self.terrain.add(tile)

                elif layer['type'] == 'objectgroup':
                    if layer['name'] == 'entities':
                        for entity in layer['objects']:
                            if entity['name'] == 'player':
                                self.player = Player(
                                    (entity['x'], entity['y']), (64, 64))

    def update(self, screen_surface):
        screen_surface.fill('black')
        screen_surface.blit(
            self.bg_img, (0 + utils.c_mod((self.shift[0] * 0.1), self.bg_img.get_width() / 2), 0))

        # Background
        self.background.draw(screen_surface, self.shift)
        # Collidable
        self.terrain.draw(screen_surface, self.shift)
        # Player
        if self.player:
            player_pos = self.player.update(
                self.terrain.sprites())
            self.player.draw(screen_surface, self.shift)
        else:
            player_pos = (0, 0)
        # Foreground
        self.foreground.draw(screen_surface, self.shift)

        # Shift
        self.shift[0] += ((self.camera_pos.x -
                           (player_pos[0] + self.shift[0])) / config.CAMERA_X_SPEED) * game.delta_time
        self.shift[1] += ((self.camera_pos.y -
                           (player_pos[1] + self.shift[1])) / config.CAMERA_Y_SPEED) * game.delta_time
        self.shift[0] = min(self.shift[0], 0)
        self.shift[1] = min(self.shift[1], 0)

        self.last_player_pos = player_pos
