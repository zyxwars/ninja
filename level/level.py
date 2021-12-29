import csv
import pygame as pg

from entities.player.player import Player
from .tile import Tile
import config
import game
from utils import debug
import utils


class Level:
    def __init__(self, level_path):
        self.player = pg.sprite.GroupSingle()
        self.tiles = pg.sprite.Group()
        self.sprites = []

        self.shift = pg.math.Vector2(0, 0)

        self.wind_sound = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/wind1.wav'))

        self.setup(level_path)

    def setup(self, level_path):
        # TODO: set length to infinite
        self.wind_sound.set_volume(0.5)
        self.wind_sound.play(-1)

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

        for tile in self.tiles:
            self.sprites.append(tile)
        self.sprites.append(self.player.sprite)

        for sprite in self.sprites:
            sprite.rect.x += -2000
            sprite.rect.y += 500

    def update(self, screen_surface):
        screen_surface.fill('black')

        self.tiles.draw(screen_surface)

        # sprite is needed because the function returns player_pos
        player_pos, player_speed_x, player_speed_y = self.player.sprite.update(
            self.tiles.sprites())
        self.player.draw(screen_surface)

        if player_pos[0] > config.SCREEN_CENTER[0]:
            if player_pos[0] - config.SCREEN_CENTER[0] / 2 > config.SCREEN_CENTER[0]:
                # Don't allow the player to go out of frame
                # Make the camera catch up
                self.shift.x = -player_speed_x
            else:
                self.shift.x = -0.2
        elif player_pos[0] < config.SCREEN_CENTER[0]:
            if player_pos[0] + config.SCREEN_CENTER[0] / 2 < config.SCREEN_CENTER[0]:
                self.shift.x = player_speed_x
            else:
                self.shift.x = 0.2
        else:
            self.shift.x = 0

        # Center the player in the lower part of the screen
        offset_y = player_pos[1] - config.SCREEN_CENTER[1] / 4
        if offset_y > config.SCREEN_CENTER[1]:
            if offset_y - config.SCREEN_CENTER[1] / 2 > config.SCREEN_CENTER[1]:
                self.shift.y = -abs(player_speed_y) or -0.5
            else:
                self.shift.y = -0.2
        # Only move the camera if the jump is high enough
        elif offset_y + config.SCREEN_CENTER[1] / 4 < config.SCREEN_CENTER[1]:
            if offset_y + config.SCREEN_CENTER[1] < config.SCREEN_CENTER[1]:
                self.shift.y = abs(player_speed_y) or 0.5
            else:
                self.shift.y = 0.2
        else:
            self.shift.y = 0

        for sprite in self.sprites:
            sprite.rect.x += round(self.shift.x * game.delta_time)
            sprite.rect.y += round(self.shift.y * game.delta_time)
