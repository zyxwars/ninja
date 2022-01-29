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
    def __init__(self, pos, patrol_area):
        self.image = pg.Surface((64, 64)).convert()
        super().__init__(self.image.get_rect(topleft=pos))

        self.hp = 100
        self.speed = config.SPEED * (random.randrange(2000, 4000) / 10000)
        self.run_speed = self.speed * 2
        self.patrol_area = patrol_area
        self.alert_timer_ms = 4000
        self.alert_timer = 0
        self.animation = 'idling'
        self.animation_index = 0
        self.animation_speed = config.ANIMATION_SPEED
        self.attack_speed_ms = 80
        self.is_touching_player = False
        self.last_touched_player = False
        self.is_attacking = False

    def on_died(self):
        pg.mixer.Sound(
            utils.get_path(__file__, 'assets/death.mp3')).play()
        self.kill()

    def on_damaged(self):
        print(self.hp)

    def update(self, player, terrain):
        self.move([*terrain, player])
        self.animate()
