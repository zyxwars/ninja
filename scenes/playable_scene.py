import pygame as pg
import json

from sprites.player.player import Player
import config
import game
from utils import debug
from utils.sheet_parser import SheetParser
from sprites.tile import Tile


class PlayableScene:
    def __init__(self, map_path):
        self.player = pg.sprite.GroupSingle()
        self.tile_layers = {}

        self.camera_pos = pg.math.Vector2(
            config.SCREEN_CENTER[0], config.SCREEN_CENTER[1] + 100)
        self.shift = pg.math.Vector2(0, 0)
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

                        if not layer['name'] in self.tile_layers:
                            self.tile_layers[layer['name']] = pg.sprite.Group()

                        self.tile_layers[layer['name']].add(tile)
                elif layer['type'] == 'objectgroup':
                    if layer['name'] == 'entities':
                        for entity in layer['objects']:
                            if entity['name'] == 'player':
                                self.player.add(Player(
                                    (entity['x'], entity['y']), (64, 64)))

    def update(self, screen_surface):
        screen_surface.fill('black')

        for tile in self.tile_layers['bg'].sprites():
            tile.draw(screen_surface, self.shift)
        for tile in self.tile_layers['terrain'].sprites():
            tile.draw(screen_surface, self.shift)

        if self.player:
            # ".sprite" is needed because the function returns player_pos
            player_pos = self.player.sprite.update(
                self.tile_layers['terrain'].sprites())
            self.player.sprite.draw(screen_surface, self.shift)
        else:
            player_pos = (0, 0)

        for tile in self.tile_layers['fg'].sprites():
            tile.draw(screen_surface, self.shift)

        # Shift
        self.shift[0] += ((self.camera_pos.x -
                           (player_pos[0] + self.shift[0])) / config.CAMERA_X_SPEED) * game.delta_time
        self.shift[1] += ((self.camera_pos.y -
                           (player_pos[1] + self.shift[1])) / config.CAMERA_Y_SPEED) * game.delta_time
        self.shift[0] = min(self.shift[0], 0)
        self.shift[1] = min(self.shift[1], 0)

        self.last_player_pos = player_pos
