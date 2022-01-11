import pygame as pg

import game


class Damageable():
    def __init__(self, hp, on_damaged, on_died, damage_cooldown=500):
        self.hp = hp
        self.on_died = on_died
        self.on_damaged = on_damaged
        self.damage_cooldown = damage_cooldown
        self.damage_cooldown_timer = 0

    def damage(self, dmg_amount):
        if self.damage_cooldown_timer > 0:
            self.damage_cooldown_timer -= game.delta_time
            return

        self.damage_cooldown_timer = self.damage_cooldown
        self.hp -= dmg_amount

        if self.hp <= 0:
            self.on_died()
            return

        self.on_damaged()
