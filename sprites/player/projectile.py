import pygame as pg

import config
import game
import utils


class Projectile(pg.sprite.Sprite):
    def __init__(self, player_pos, mouse_pos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pg.image.load(utils.get_path(
            __file__, 'assets/shuriken.png')).convert_alpha()
        self.image = pg.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect(topleft=player_pos)
        self.dir = (pg.math.Vector2(
            mouse_pos) - pg.math.Vector2(player_pos)).normalize()
        self.speed = config.PLAYER_PROJECTILE_SPEED

    def update(self):
        self.move()

    def move(self):
        self.rect.x += self.dir.x * self.speed * game.delta_time
        self.rect.y += self.dir.y * self.speed * game.delta_time
