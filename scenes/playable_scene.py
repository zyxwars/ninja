from typing import Tuple
import pygame as pg
import json
import math
from scenes.gui import Gui

from sprites.enemies.enemy import Enemy
from sprites.flag import Flag
from sprites.groups.collectable_group import CollectableGroup
from sprites.groups.shiftable_group import ShiftableGroup
from sprites.player.player import Player
import config
import game
from utils import debug, get_path, SheetParser, c_mod
from sprites.tile import Tile
from .trigger import Trigger
import sprites.enemies as enemies
import sprites.weapons as weapons


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


class Image():
    def __init__(self, image, x, y, *args, **kwargs):
        self.image = image.convert_alpha()
        # Tiled tile object shows coords as bottomleft
        self.rect = self.image.get_rect(bottomleft=(x, y))


class PlayableScene:
    def __init__(self, map_path):
        self.bg_img = make_scrollable(pg.image.load(
            get_path(__file__, 'assets/bg.png')).convert())

        self.parallax = []
        self.background = ShiftableGroup()
        # Collidable with player
        self.terrain = ShiftableGroup()
        self.enemies = ShiftableGroup()
        self.player = None
        # Collectable in the sense of being able to be picked up, the "s" signifies it is a list when used in a loop
        self.collectables = CollectableGroup()
        self.foreground = ShiftableGroup()
        self.triggers = []
        self.fg_objects = []

        self.gui = Gui()

        self.camera_pos = pg.Vector2(
            config.SCREEN_CENTER[0], config.SCREEN_HEIGHT * 0.6)
        self.shift = pg.Vector2(0, 0)
        self.last_player_pos = (0, 0)

        self.load_map(map_path)

    def load_trigger(self, trigger):
        """Override this to add extra trigger types, or change trigger behavior"""

        if trigger['name'] == 'finish':
            self.triggers.append(
                Trigger(lambda: print('finish level'), trigger['x'], trigger['y'], trigger['width'], trigger['height']))

    def load_map(self, map_path):
        with open(map_path, encoding='utf-8') as f:
            map_data = json.load(f)
            sheet_parser = SheetParser('assets/tileset.png', __file__)

            for layer in map_data['layers']:
                if layer['type'] == 'tilelayer':
                    w = layer['width']

                    for i, tile in enumerate(layer['data']):
                        if tile == 0:
                            continue

                        x = i % w * config.TILE_SIZE
                        y = i // w * config.TILE_SIZE

                        # tile - 1 >> The first tile has value of 1, but the sheet parser starts with x, y = 0, 0
                        # TODO: load the number of columns(20) from tileset.json
                        tile = Tile((x, y),
                                    sheet_parser.load_image(((tile - 1) % 20, (tile - 1) // 20)))

                        if 'fg_' in layer['name']:
                            self.foreground.add(tile)
                        elif 'bg_' in layer['name']:
                            self.background.add(tile)
                        else:
                            self.terrain.add(tile)

                elif layer['type'] == 'objectgroup':
                    # Entities
                    if layer['name'] == 'entities':
                        for entity in layer['objects']:
                            pos = (entity['x'], entity['y'])

                            # Player
                            if entity['name'] == 'player':
                                self.player = Player(
                                    pos, (self.enemies,
                                          self.terrain), self.collectables, self.enemies, self.terrain)  # To create a tuple with only one item, you have add a comma after the item, unless Python will not recognize the variable as a tuple.
                            # Enemies
                            elif entity['name'] == 'patrol':
                                self.enemies.add(enemies.Patrol(
                                    pos, (pos[0], pos[0] + entity['width'] - 64), (self.terrain, self.player), self.player))

                            # Collectables
                            elif entity['name'] == 'katana':
                                self.collectables.add(
                                    weapons.Katana(pos, (self.terrain,)))

                            elif entity['name'] == 'flag':
                                self.collectables.add(
                                    Flag(pos, (self.terrain,)))

                    elif 'trees' in layer['name']:
                        tree_sheet_parser = SheetParser(
                            'assets/trees.png', __file__)
                        for img in layer['objects']:
                            tree_layer = self.parallax if 'parallax' in layer['name'] else self.fg_objects
                            tree_layer.append(Image(tree_sheet_parser.load_image(
                                ((int(img['name'].split('_')[-1]) - 1), 0), (330, 600)), img['x'], img['y']))

                    elif layer['name'] == 'triggers':
                        for trigger in layer['objects']:
                            self.load_trigger(trigger)

    def update(self, screen_surface):
        debug.debug('shift', self.shift)

        # Static image background
        screen_surface.fill('black')

        # Clamp background vertically between zero and its height, while also having parallax effect
        screen_surface.blit(
            self.bg_img, (c_mod((self.shift[0] * 0.1), self.bg_img.get_width() / 2), min(0, max(self.shift[1] * 0.9, -self.bg_img.get_height() + config.SCREEN_HEIGHT))))

        # Parallax background
        for img in self.parallax:
            screen_surface.blit(
                img.image, (img.rect.x + self.shift[0] * 0.9, img.rect.y + self.shift[1]))

        # Background tiles
        self.background.draw(screen_surface, self.shift)
        # Collidable
        self.terrain.draw(screen_surface, self.shift)

        # Enemies
        self.enemies.update()
        self.enemies.draw(screen_surface, self.shift)
        # Player
        if self.player:
            player_pos = self.player.update()
            self.player.draw(screen_surface, self.shift)
        else:
            player_pos = (0, 0)
        # collectables
        self.collectables.update()
        self.collectables.draw(self.player.rect, screen_surface, self.shift)
        # Foreground
        self.foreground.draw(screen_surface, self.shift)
        # Triggers
        for trigger in self.triggers:
            trigger.collidepoint(player_pos[0], player_pos[1])
        # Parallax foreground
        for img in self.fg_objects:
            screen_surface.blit(
                img.image, (img.rect.x + self.shift[0], img.rect.y + self.shift[1]))

        # Gui
        self.gui.draw_equipped_weapon(self.player.weapon.image, screen_surface)
        self.gui.draw_life_essence(self.player.hp, screen_surface)
        self.gui.draw_flags_collected(
            self.player.flags_collected, screen_surface)

        # Shift
        self.shift[0] += ((self.camera_pos.x -
                           (player_pos[0] + self.shift[0])) / config.CAMERA_X_SPEED) * game.delta_time
        self.shift[1] += ((self.camera_pos.y -
                           (player_pos[1] + self.shift[1])) / config.CAMERA_Y_SPEED) * game.delta_time
        self.shift[0] = min(self.shift[0], 0)
        # The background doesn't scroll vertically so allow scrolling to negatives
        # self.shift[1] = min(self.shift[1], 0)

        self.last_player_pos = player_pos
