import pygame as pg

import config
import game
from utils import debug


class PhysicsEntity(pg.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.pos = pg.Vector2(rect.x, rect.y)
        self.rect = rect
        self.dir = pg.Vector2(0, 0)
        self.speed = config.SPEED
        self.jump_force = config.JUMP_FORCE
        self.gravity = config.GRAVITY
        self.is_grounded = False
        self.touching_wall = False
        self.facing_right = True

    def set_pos(self, x=None, y=None):
        # FIXME: Can't set pos of 0, might not ever be needed
        self.pos.x = x or self.pos.x
        self.pos.y = y or self.pos.y

    def add_x(self, x):
        # If delta time is large enough it is possible for add pos to be bigger than the tile
        # making the player phase through it
        if abs(abs(self.pos.x) - abs(self.pos.x + x)) >= config.TILE_SIZE:
            x = (config.TILE_SIZE - 1) * (x/abs(x))

        self.pos.x += x

    def add_y(self, y):
        if abs(abs(self.pos.y) - abs(self.pos.y + y)) >= config.TILE_SIZE:
            y = (config.TILE_SIZE - 1) * (y/abs(y))

        self.pos.y += y

    def move(self, terrain):
        self.add_x(self.dir.x * self.speed * game.delta_time)
        self.rect.x = int(self.pos.x)
        self.collide_horizontal(terrain)

        # Jump force and gravity are directly added to the y dir
        self.apply_gravity()
        self.add_y(self.dir.y * game.delta_time)
        self.rect.y = int(self.pos.y)
        self.collide_vertical(terrain)

        # If dir.x = 0 keep facing in the last direction
        if self.dir.x > 0:
            self.facing_right = True
        elif self.dir.x < 0:
            self.facing_right = False

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

                self.pos.x = self.rect.x

    def collide_vertical(self, tiles):
        self.is_grounded = False

        # Check collision 1 pixel below the actual position
        # This prevents collision not being detected when apply_gravity() moves less than 1 pixel every frame

        # Lowering the rect causes head collision to be confused with horizontal collision
        # Inflating the rect instead of moving it seems to work for now
        temp_rect = self.rect.copy()
        temp_rect = temp_rect.inflate(0, 1)

        for tile in tiles:
            if tile.rect.colliderect(temp_rect):
                # Falling
                if self.dir.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.is_grounded = True
                # Jumping
                if self.dir.y < 0:
                    self.rect.top = tile.rect.bottom

                self.dir.y = 0
                self.pos.y = self.rect.y

    def apply_gravity(self):
        # Limit max gravity momentum
        if self.dir.y < 2:
            self.dir.y += self.gravity * game.delta_time

    def jump(self):
        # Jump force is a positive number, so to jump we need its opposite
        self.dir.y = -self.jump_force
