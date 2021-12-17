import pygame as pg
import math

import config
from utils import debug
import utils
import shared_data
from ..animated_humanoid import AnimatedHumanoid
import utils


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

        self.jump_sound = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/jump.wav'))
        self.jump_sound.set_volume(0.5)
        self.last_jumped = 1000

        self.land_sound = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/land.wav'))
        self.land_sound.set_volume(0.1)
        self.last_grounded = False
        self.last_gravity = 0

        super().__init__(self.image.get_rect(topleft=pos), self.animations)

    def debug(self):
        debug.debug('rect', self.rect)
        debug.debug('jumped_from_wall', self.jumped_from_wall)
        debug.debug('touching_wall', self.touching_wall)
        debug.debug('is_grounded', self.is_grounded)
        debug.debug('dir', self.dir)
        debug.debug('delta_time', shared_data.delta_time)
        debug.debug('attacking', self.is_attacking)
        debug.debug('last_jumped', self.last_jumped)

    def update(self, tiles):
        self.debug()
        self.get_input()
        self.move(tiles)
        self.animate()

        self.last_jumped += shared_data.delta_time

        if self.is_grounded != self.last_grounded:
            if self.is_grounded and self.last_gravity > 1:
                self.land_sound.play()
        self.last_grounded = self.is_grounded
        self.last_gravity = self.dir.y

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

        if self.last_jumped > 300:
            self.jump_sound.play()
            self.last_jumped = 0

        super().jump()
