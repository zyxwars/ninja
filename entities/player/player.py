import pygame as pg
import math

from .projectile_indicator import ProjectileIndicator
import config
from utils import debug
import utils
import shared_data
from ..physics_entity import PhysicsEntity


class Player(PhysicsEntity):
    def __init__(self, pos, size):
        sheet_parser = utils.SpriteSheetParser(
            __file__, 'assets/player_sheet.png')
        self.image = pg.Surface(size).convert_alpha()

        super().__init__(self.image.get_rect(topleft=pos))

        self.idle_animation = sheet_parser.load_row((0, 0), 3, (64, 64))
        self.attack_animation = sheet_parser.load_row((0, 1), 4, (64, 64))
        self.jump_animation = sheet_parser.load_row((0, 2), 1, (64, 64))
        self.fall_animation = sheet_parser.load_row((0, 3), 1, (64, 64))
        self.animation = []
        self.animation_index = 0

        self.jumped_from_wall = False
        self.projectile_indicator = pg.sprite.GroupSingle()
        self.projectile_indicator.add(ProjectileIndicator())

    def debug(self):
        debug.debug('jumped_from_wall', self.jumped_from_wall)
        debug.debug('touching_wall', self.touching_wall)
        debug.debug('is_grounded', self.is_grounded)
        debug.debug('dir', self.dir)
        debug.debug('delta_time', shared_data.delta_time)

    def update(self, tiles, surface):
        self.debug()
        self.get_input()
        self.move(tiles)
        self.animate()

        self.projectile_indicator.update(self.rect.center, tiles, surface)
        self.projectile_indicator.draw(surface)

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
        # Is on ground
        if self.is_grounded:
            self.jumped_from_wall = False
        # Is in the air
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

    def animate(self):
        # Running
        if self.is_grounded and self.dir.x != 0:
            pass
        # Jumping
        if self.dir.y < 0:
            self.animation = self.jump_animation
        # Touching wall
        elif self.touching_wall:
            if self.is_grounded:
                pass
            else:
                pass
        # Falling
        elif self.dir.y >= 0.5 and not self.is_grounded:
            self.animation = self.fall_animation
        # Idle
        else:
            self.animation = self.idle_animation

        if self.animation_index >= len(self.animation):
            self.animation_index = 0
        self.image = self.animation[math.floor(self.animation_index)]
        self.animation_index += config.PLAYER_ANIMATION_SPEED * shared_data.delta_time
