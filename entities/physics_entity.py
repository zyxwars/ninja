import pygame as pg

import config
import shared_data
from utils import debug


class PhysicsEntity(pg.sprite.Sprite):
    def __init__(self, rect, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pos = pg.math.Vector2(rect.x, rect.y)
        self.rect = rect
        self.dir = pg.math.Vector2(0, 0)
        self.speed = config.SPEED
        self.jump_force = config.JUMP_FORCE
        self.gravity = config.GRAVITY
        self.is_grounded = False
        self.touching_wall = False

    # https://www.py4u.net/discuss/247960
    # Add movement precision
    # Rounding rect values caused movement to the left and up to be faster
    def set_x(self, x):
        self.pos.x = x
        self.rect.x = round(self.pos.x)

    def set_y(self, y):
        self.pos.y = y
        self.rect.y = round(self.pos.y)

    def move(self, tiles):
        debug.debug('rect', self.rect)
        debug.debug('pos', self.pos)

        self.set_x(self.pos.x + self.dir.x *
                   self.speed * shared_data.delta_time)
        self.collide_horizontal(tiles)

        self.apply_gravity()
        # Jump force and gravity are directly added to the y dir
        y_speed = self.dir.y * shared_data.delta_time
        # FIXME: If delta time is large enough it is possible for y to be bigger than the tile height
        # making the player phase through it
        # 32(tile height) - 1 (added in collision check)
        self.set_y(self.pos.y + y_speed if y_speed <= 31 else 31)
        self.collide_vertical(tiles)

    def collide_horizontal(self, tiles):
        self.touching_wall = False
        self.is_touching_right_wall = False

        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                if self.dir.x > 0:
                    self.rect.right = tile.rect.left
                    self.touching_wall = 'right'
                if self.dir.x < 0:
                    self.rect.left = tile.rect.right
                    self.touching_wall = 'left'

                self.set_x(self.rect.x)

    def collide_vertical(self, tiles):
        self.is_grounded = False

        # Check collision 1 pixel below the actual position
        # This prevents collision not being detected when apply_gravity() moves less than 1 pixel every frame
        temp_rect = self.rect.copy()
        temp_rect.y += 1

        for tile in tiles:
            if tile.rect.colliderect(temp_rect):
                # Falling
                if self.dir.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.is_grounded = True
                # Jumping
                if self.dir.y < 0:
                    self.rect.top = tile.rect.bottom

                self.set_y(self.rect.y)
                self.dir.y = 0

    def apply_gravity(self):
        self.dir.y += self.gravity * shared_data.delta_time

    def jump(self):
        # Jump force is a positive number, so we need to subtract is from self.dir.y
        self.dir.y = -self.jump_force
