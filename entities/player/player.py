import pygame as pg
import math

from .crosshair import Crosshair
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

        self.idle_animation = sheet_parser.load_row((0, 0), 3, size)
        self.attack_animation = sheet_parser.load_row((0, 1), 4, size)
        self.attacking = 0
        self.jump_animation = sheet_parser.load_row((0, 2), 1, size)
        self.fall_animation = sheet_parser.load_row((0, 3), 1, size)
        self.run_animation = sheet_parser.load_row((0, 4), 3, size)
        self.animation = []
        self.animation_index = 0

        self.jumped_from_wall = False
        self.crosshair = pg.sprite.GroupSingle(Crosshair())

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

        self.crosshair.update(self.rect.center, tiles, surface)
        self.crosshair.draw(surface)

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

        mouse = pg.mouse.get_pressed()

        if mouse[0]:
            if self.crosshair.sprite.shoot(self.rect.center):
                self.attacking = True

    def jump(self):
        # If player is touching wall when jumping from ground count it as wall jumping
        if self.touching_wall == 'right':
            if self.jumped_from_wall == 'right':
                return
            self.jumped_from_wall = 'right'

        elif self.touching_wall == 'left':
            if self.jumped_from_wall == 'left':
                return
            self.jumped_from_wall = 'left'
        elif self.is_grounded:
            self.jumped_from_wall = False
        else:
            return

        super().jump()

    def animate(self):
        # Attacking
        if self.attacking:
            self.animation = self.attack_animation
        # Running
        elif self.is_grounded and self.dir.x != 0:
            self.animation = self.run_animation
        # Jumping
        elif self.dir.y < 0:
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
            # End attack animation after it played once
            if self.attacking:
                self.attacking = False

        # flip_x = !facing_right, flip image only when not facing right
        self.image = pg.transform.flip(
            self.animation[math.floor(self.animation_index)], not self.facing_right, False)

        self.animation_index += config.PLAYER_ANIMATION_SPEED * shared_data.delta_time
