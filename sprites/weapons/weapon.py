from typing import Tuple
import pygame as pg

from ..physics_entity import PhysicsEntity


class Weapon(PhysicsEntity):
    def __init__(self, damage, attack_length_ms, rect=None, * args, **kwargs):
        # Entity without rect holds the data for non droppable weapons such as hands
        if rect:
            super().__init__(rect, *args, **kwargs)
        self.damage = damage
        self.attack_length_ms = attack_length_ms

    def equip(self):
        self.kill()
        return self

    def unequip(self, drop_pos: Tuple):
        self.set_pos(*drop_pos)

    def update(self, terrain):
        self.move(terrain)
