import pygame as pg

import config
import game
from utils import debug, groups_to_sprites
from utils.statemachine import State, StateMachine


class Colliding(State):
    def __init__(self, name, physics_entity: 'PhysicsEntity', *args, **kwargs):
        self.name = name
        self._sm = physics_entity

    def update(self):
        self._sm.add_x(self._sm.dir.x * self._sm.speed * game.delta_time)
        self._sm.rect.x = int(self._sm.pos.x)
        self._sm.collide_horizontal()

        self._sm.add_y(self._sm.dir.y * game.delta_time)
        self._sm.rect.y = int(self._sm.pos.y)
        self._sm.collide_vertical()

        # If dir.x = 0 keep facing in the last direction
        if self._sm.dir.x > 0:
            self._sm.facing_right = True
        elif self._sm.dir.x < 0:
            self._sm.facing_right = False


class PulledByGravity(Colliding):
    def __init__(self, *args, **kwargs):
        super().__init__('pulled_by_gravity', *args, **kwargs)

    def update(self):
        self._sm.apply_gravity()

        super().update()


class PhysicsEntity(pg.sprite.Sprite, StateMachine):
    """PhysicsEntity class by itself doesn't work as you're expected to define your own states and update method
    """

    def __init__(self, rect, collidables: tuple[pg.sprite.Group, ...], *args, **kwargs):
        super().__init__(*args, **kwargs)
        StateMachine.__init__(self)
        self.collidables = collidables
        self.rect = rect
        self.pos = pg.Vector2(rect.x, rect.y)

        self.dir = pg.Vector2(0, 0)
        self.speed = config.SPEED
        self.jump_force = config.JUMP_FORCE
        self.gravity = config.GRAVITY
        self.is_grounded = False
        self.touching_wall = False
        self.facing_right = True

    def set_pos(self, x=None, y=None):
        self.pos.x = x if x is not None else self.pos.x
        self.pos.y = y if y is not None else self.pos.y

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

    def collide_horizontal(self):
        self.touching_wall = False
        self.is_touching_right_wall = False

        for collidable in groups_to_sprites(self.collidables):
            if collidable.rect.colliderect(self.rect):
                if self.dir.x > 0:
                    self.rect.right = collidable.rect.left
                    self.touching_wall = 'right'
                if self.dir.x < 0:
                    self.rect.left = collidable.rect.right
                    self.touching_wall = 'left'

                self.pos.x = self.rect.x

    def collide_vertical(self):
        self.is_grounded = False

        # Check collision 1 pixel below the actual position
        # This prevents collision not being detected when apply_gravity() moves less than 1 pixel every frame

        # Lowering the rect causes head collision to be confused with horizontal collision
        # Inflating the rect instead of moving it seems to work for now
        temp_rect = self.rect.copy()
        temp_rect = temp_rect.inflate(0, 1)

        for collidable in groups_to_sprites(self.collidables):
            if collidable.rect.colliderect(temp_rect):
                # Falling
                if self.dir.y > 0:
                    self.rect.bottom = collidable.rect.top
                    self.is_grounded = True
                # Jumping
                if self.dir.y < 0:
                    self.rect.top = collidable.rect.bottom

                self.dir.y = 0
                self.pos.y = self.rect.y

    def apply_gravity(self):
        # Limit max gravity momentum, "terminal velocity"
        if self.dir.y < 1.5:
            self.dir.y += self.gravity * game.delta_time

    def jump(self):
        # Jump force is a positive number, so to jump we need its opposite
        self.dir.y = -self.jump_force
