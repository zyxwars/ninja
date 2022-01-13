import pygame as pg

import game


class Damageable():
    def __init__(self, hp, on_damaged, on_died):
        self.hp = hp
        self.on_died = on_died
        self.on_damaged = on_damaged

    def damage(self, dmg_amount):
        self.hp -= dmg_amount

        if self.hp <= 0:
            self.on_died()
            return

        self.on_damaged()
