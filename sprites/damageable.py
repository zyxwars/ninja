import pygame as pg

import game


class Damageable():
    def __init__(self, hp):
        self.hp = hp

    def damage(self, dmg_amount):
        self.hp -= dmg_amount

        if self.hp <= 0:
            self.on_died()
            return

        self.on_damaged()

    def on_damaged(self):
        pass

    def on_died(self):
        pass
