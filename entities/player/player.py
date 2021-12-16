import pygame as pg
import math

import config
from utils import debug
import utils
import shared_data
from ..animated_humanoid import AnimatedHumanoid


class Player(AnimatedHumanoid):
    def __init__(self, pos, size):
        sheet_parser = utils.SpriteSheetParser(
            __file__, 'assets/player_sheet.png')
        self.image = pg.Surface(size).convert_alpha()

        self.animations = {'idle': sheet_parser.load_row((0, 0), 3, size),
                           'attack': sheet_parser.load_row((0, 1), 4, size),
                           'jump': sheet_parser.load_row((0, 2), 1, size),
                           'fall': sheet_parser.load_row((0, 3), 1, size),
                           'run': sheet_parser.load_row((0, 4), 3, size),
                           'push': sheet_parser.load_row((0, 5), 3, size),
                           'wall_slide': sheet_parser.load_row((0, 6), 1, size)}

        super().__init__(self.image.get_rect(topleft=pos), self.animations)

    def debug(self):
        debug.debug('rect', self.rect)
        debug.debug('jumped_from_wall', self.jumped_from_wall)
        debug.debug('touching_wall', self.touching_wall)
        debug.debug('is_grounded', self.is_grounded)
        debug.debug('dir', self.dir)
        debug.debug('delta_time', shared_data.delta_time)
        debug.debug('attacking', self.is_attacking)

    def update(self, tiles):
        self.debug()
        self.get_input()
        self.move(tiles)
        self.animate()

        return self.rect.center, self.speed, self.dir.y

    def get_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.dir.x = -1
        elif keys[pg.K_d]:
            self.dir.x = 1
        else:
            self.dir.x = 0

        if keys[pg.K_SPACE]:
            self.jump()

    def jump(self):
        if self.is_grounded:
            self.jumped_from_wall = False
        elif self.touching_wall == 'right':
            if self.jumped_from_wall == 'right':
                return
            self.jumped_from_wall = 'right'

        elif self.touching_wall == 'left':
            if self.jumped_from_wall == 'left':
                return
            self.jumped_from_wall = 'left'
        else:
            return

        super().jump()
