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
        self.alert_timer_ms = 4000
        self.alert_timer = 0
        self.attack_cooldown_ms = 500
        self.attack_cooldown = 0

    def on_died(self):
        pg.mixer.Sound(
            utils.get_path(__file__, 'assets/death.mp3')).play()
        self.kill()

    def on_damaged(self):
        print(self.hp)
        self.add_x(5)

    def patrol(self):
        self.image.fill('black')
        if self.touching_wall and self.is_grounded:
            self.jump()

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

    def follow(self, pos):
        self.image.fill('red')
        if self.touching_wall and self.is_grounded:
            self.jump()

        if self.rect.centerx > pos[0]:
            self.dir.x = -1
        elif self.rect.centerx < pos[0]:
            self.dir.x = 1
        else:
            self.dir.x = 0

    def roam(self, change_chance=0.0005):
        self.image.fill('orange')
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
        if random.random() < change_chance * game.delta_time:
            self.dir.x = -self.dir.x

    def spot_player(self, player):
        if abs(player.rect.centery - self.rect.centery) > 32:
            return

        if 0 > player.rect.centerx - self.rect.centerx > -300 and not self.facing_right:
            self.alert(player.rect.center)
        elif 0 < player.rect.centerx - self.rect.centerx < 300 and self.facing_right:
            self.alert(player.rect.center)

    def alert(self, alert_others=True):
        self.alert_timer = self.alert_timer_ms

        if not alert_others:
            return

        for enemy in self.groups()[0] or []:
            if enemy is self:
                continue

            if abs(enemy.rect.centerx - self.rect.centerx) > 800:
                continue

            enemy.alert(alert_others=False)

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
        self.alert_timer -= game.delta_time
        self.attack_cooldown += game.delta_time
        self.move(tiles)
