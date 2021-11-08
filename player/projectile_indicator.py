import pygame as pg
import math

from .projectile import Projectile
import config


class ProjectileIndicator(pg.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pg.image.load(
            './player/assets/projectile_indicator.png').convert_alpha()
        self.image = pg.transform.flip(self.image, False, True)
        self.image_original = self.image
        self.rect = self.image.get_rect()
        self.projectiles = pg.sprite.Group()
        self.projectile_cooldown = config.PROJECTILE_COOLDOWN

    def update(self, player_pos, tiles, surface):
        self.animate(player_pos)

        if pg.mouse.get_pressed()[0] and self.projectile_cooldown < 0:
            self.shoot_projectile(player_pos)

        self.projectile_cooldown -= 1

        self.collide_projectiles(tiles)
        self.projectiles.update()
        self.projectiles.draw(surface)

    def animate(self, player_pos):
        distance_vector = pg.math.Vector2(
            pg.mouse.get_pos()) - pg.math.Vector2(player_pos)
        angle = math.degrees(
            math.atan2(-distance_vector.y, distance_vector.x))

        self.image = pg.transform.rotate(self.image_original, angle + 90)
        self.rect = self.image.get_rect(
            center=player_pos)

    def shoot_projectile(self, player_pos):
        self.projectiles.add(Projectile(
            player_pos, pg.mouse.get_pos()))
        self.projectile_cooldown = config.PROJECTILE_COOLDOWN

    def collide_projectiles(self, tiles):
        colliding_projectiles = pg.sprite.groupcollide(
            tiles, self.projectiles, False, True)
