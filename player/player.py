import pygame as pg

from .projectile_indicator import ProjectileIndicator
import config
from debug import debug
import pygame_data


class Player(pg.sprite.Sprite):
    def __init__(self, pos, size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pg.Surface((32, 64))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)
        self.dir = pg.math.Vector2(0, 0)
        self.speed = config.PLAYER_SPEED
        self.gravity = config.PLAYER_GRAVITY
        self.jump_speed = config.PLAYER_JUMP_SPEED
        self.jump_buffer = config.PLAYER_JUMP_BUFFER
        self.is_grounded = False
        self.jumped_from_wall = False
        self.jumped_from_right_wall = False
        self.is_touching_wall = False
        self.is_touching_right_wall = False
        self.projectile_indicator = pg.sprite.GroupSingle()
        self.projectile_indicator.add(ProjectileIndicator())

    def load_images(self, image_name, number_of_images, animation_list, size):
        for i in range(number_of_images):
            image = pg.image.load(
                f'./player/{image_name}{i+1}.png').convert_alpha()
            image = pg.transform.scale(image, size)
            animation_list.append(image)

    def update(self, tiles, surface):
        self.debug()
        self.get_input()
        self.move_horizontal(tiles)
        self.move_vertical(tiles)
        self.animate()

        self.projectile_indicator.update(self.rect.center, tiles, surface)
        self.projectile_indicator.draw(surface)

    def debug(self):
        debug.debug('jump_buffer', self.jump_buffer)
        debug.debug('is_grounded', self.is_grounded)
        debug.debug('dir', self.dir)
        debug.debug('delta_time', pygame_data.delta_time)

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

    def move_horizontal(self, tiles):
        self.rect.x += self.dir.x * self.speed
        self.is_touching_wall = False
        self.is_touching_right_wall = False

        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                if self.dir.x > 0:
                    self.rect.right = tile.rect.left
                    self.is_touching_right_wall = True
                if self.dir.x < 0:
                    self.rect.left = tile.rect.right
                self.is_touching_wall = True

    def move_vertical(self, tiles):
        self.apply_gravity()
        self.is_grounded = False
        self.jump_buffer -= 1

        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                if self.dir.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.dir.y = 0
                    self.is_grounded = True
                    self.jump_buffer = config.PLAYER_JUMP_BUFFER
                if self.dir.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.dir.y = 0

    def apply_gravity(self):
        self.dir.y += self.gravity
        self.rect.y += self.dir.y

    def jump(self):
        if self.is_grounded or self.jump_buffer > 0:
            self.dir.y = self.jump_speed
            self.jumped_from_right_wall = False
            self.jumped_from_wall = False
            self.jump_buffer = 0
        elif self.is_touching_wall:
            if self.is_touching_right_wall:
                if self.jumped_from_right_wall and self.jumped_from_wall:
                    return
                self.dir.y = self.jump_speed
                self.jumped_from_right_wall = True
            else:
                if not self.jumped_from_right_wall and self.jumped_from_wall:
                    return
                self.dir.y = self.jump_speed
                self.jumped_from_right_wall = False

            self.jumped_from_wall = True

    def animate(self):
        pass
