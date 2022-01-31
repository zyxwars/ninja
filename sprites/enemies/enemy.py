import pygame as pg
import random
import math
from sprites import enemies

from sprites.damageable import Damageable

import config
from sprites.physics_entity import PhysicsEntity
from sprites.player.player import Player
import utils
import game
from utils import debug


class Enemy(PhysicsEntity, Damageable):
    def __init__(self, pos, patrol_area, collidables, player, animations):
        self.image = pg.Surface((64, 64)).convert()
        super().__init__(self.image.get_rect(topleft=pos), collidables)
        self.player = player

        self.speed = config.SPEED * (random.randrange(2000, 4000) / 10000)

        self.patrol_area = patrol_area

        self.animations = animations
        self.animation = self.animations['idling']
        self.last_animation = self.animation
        self.animation_index = 0
        self.animation_speed = config.ANIMATION_SPEED

    def on_died(self):
        pg.mixer.Sound(
            utils.get_path(__file__, 'assets/death.mp3')).play()
        self.kill()

    def on_damaged(self):
        print(self.hp)

    def animate(self):
        if self.animation_index >= len(self.animation) or self.last_animation != self.animation:
            self.animation_index = 0

        # flip_x = !facing_right, flip image only when not facing right
        self.image = pg.transform.flip(self.animation[math.floor(
            self.animation_index)], not self.facing_right, False)

        self.animation_index += self.animation_speed * game.delta_time

        self.last_animation = self.animation
