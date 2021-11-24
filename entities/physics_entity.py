import pygame as pg

import config
import shared_data


class PhysicsEntity(pg.sprite.Sprite):
    def __init__(self, rect, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rect = rect
        self.dir = pg.math.Vector2(0, 0)
        self.speed = config.SPEED
        self.jump_force = config.JUMP_FORCE
        self.gravity = config.GRAVITY
        self.is_grounded = False
        self.touching_wall = False

    def move(self, tiles):
        self.rect.x += self.dir.x * self.speed * shared_data.delta_time
        self.collide_horizontal(tiles)

        self.apply_gravity()
        # Jump force and gravity are directly added to the y dir
        self.rect.y += self.dir.y * shared_data.delta_time
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
                self.dir.y = 0

    def apply_gravity(self):
        self.dir.y += self.gravity * shared_data.delta_time

    def jump(self):
        # Jump force is a positive number, so we need to subtract is from self.dir.y
        self.dir.y -= self.jump_force
