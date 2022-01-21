import pygame as pg
import random
import math

from sprites.damageable import Damageable

import config
from sprites.physics_entity import PhysicsEntity
import utils
import game
from utils import debug


class BaseEnemy(PhysicsEntity, Damageable):
    def __init__(self, pos, patrol_area):
        self.image = pg.Surface((64, 64)).convert()
        super().__init__(self.image.get_rect(topleft=pos))

        self.hp = 100
        self.speed = config.SPEED * 0.5
        self.patrol_area = patrol_area
        self.is_alert = False
        self.attack_cooldown_ms = 500
        self.attack_cooldown = 0

    def on_died(self):
        pg.mixer.Sound(
            utils.get_path(__file__, 'assets/death.mp3')).play()
        self.kill()

    def on_damaged(self):
        print(self.hp)
        self.add_x(5)

    # def patrol(self):
    #     if self.touching_wall and self.is_grounded:
    #         self.jump()

    #     if self.dir.x == 0:
    #         self.dir.x = random.randint(-1, 1)
    #         return

    #     # Reverse direction
    #     if self.pos.x < self.patrol_route[0] or self.pos.x > self.patrol_route[1]:
    #         self.dir.x = - self.dir.x

    def follow(self, pos):
        if self.touching_wall and self.is_grounded:
            self.jump()

        if self.rect.centerx > pos[0]:
            self.dir.x = -1
        elif self.rect.centerx < pos[0]:
            self.dir.x = 1
        else:
            self.dir.x = 0

    def roam(self):
        if self.touching_wall and self.is_grounded:
            # Sometimes turn and sometimes jump over obstacles
            if random.random() < 0.5:
                self.jump()
            else:
                self.dir.x = -self.dir.x

            return

        if self.dir.x == 0:
            self.dir.x = random.randint(-1, 1)
            return

        # Reverse direction if border is reached
        if self.pos.x < self.patrol_area[0]:
            self.dir.x = 1
            return
        if self.pos.x > self.patrol_area[1]:
            self.dir.x = -1
            return

        # Make the chance equal with different fps > delta_time
        if random.random() < 0.0005 * game.delta_time:
            self.dir.x = -self.dir.x

    def spot_player(self, player):
        if 0 > player.rect.x - self.rect.x > -128 and not self.facing_right:
            self.is_alert = True
        elif 0 < player.rect.x - self.rect.x < 128 and self.facing_right:
            self.is_alert = True
        else:
            self.is_alert = False

    def attack(self, entity):
        if not self.attack_cooldown > self.attack_cooldown_ms:
            return

        is_hit = False
        self.attack_cooldown = 0

        attack_rect = self.rect.copy()
        attack_rect.x += 8 if self.facing_right else -8

        if attack_rect.colliderect(entity.rect):
            if isinstance(entity, Damageable):
                entity.damage(25)
                is_hit = True

    def update(self, tiles):
        self.move(tiles)
        self.attack_cooldown += game.delta_time
