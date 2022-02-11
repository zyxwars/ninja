from typing import Tuple
import pygame as pg
import random
import math
from sprites import enemies

from sprites.damageable import Damageable

import config
from sprites.physics_entity import PhysicsEntity
from sprites.player.player import Player
from sprites.weapons.punch import Punch
from sprites.weapons.weapon import Weapon
import utils
import game
from utils import debug


class Enemy(PhysicsEntity, Damageable):
    def __init__(self, pos, patrol_area: Tuple, collidables, player, animations):
        self.image = pg.Surface((64, 64)).convert()
        super().__init__(self.image.get_rect(topleft=pos), collidables)
        self.player = player

        self.speed = config.SPEED * (random.randrange(2000, 4000) / 10000)
        self.attack_length = 500
        self.alert_time = 5000
        self.alert_timer = 0
        self.last_alert_timer = self.alert_timer
        self.patrol_area = patrol_area
        self.player_spotted_pos = [0, 0]
        self.last_dir = self.dir
        self.damage_amount = 25
        self.weapon: Weapon = Punch()

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

    def alert(self, pos: Tuple):
        self.alert_timer = self.alert_time
        self.player_spotted_pos = pos

    def animate(self):
        if self.animation_index >= len(self.animation) or self.last_animation != self.animation:
            self.animation_index = 0

        # flip_x = !facing_right, flip image only when not facing right
        self.image = pg.transform.flip(self.animation[math.floor(
            self.animation_index)], not self.facing_right, False)

        self.animation_index += self.animation_speed * game.delta_time

        self.last_animation = self.animation

    def update(self):
        self.current_state.update()
        self.animate()
        self.last_alert_timer = self.alert_timer
        self.alert_timer -= game.delta_time
