from typing import Tuple
import pygame as pg

from ..physics_entity import PhysicsEntity
from utils import get_path
import game


class Weapon(PhysicsEntity):
    def __init__(self, damage, attack_length_ms, name, pos=(0, 0), *args, **kwargs):
        self.image = pg.image.load(
            get_path(__file__, f'assets/{name}.png')).convert_alpha()
        super().__init__(self.image.get_rect(topleft=pos), *args, **kwargs)
        self.damage = damage
        self.attack_length_ms = attack_length_ms
        self.name = name
        self.equip_cooldown = 500

    def equip(self):
        if self.equip_cooldown < 500:
            return

        self.kill()
        return self

    def unequip(self, drop_pos: Tuple):
        self.set_pos(*drop_pos)
        self.equip_cooldown = 0
        return self

    def update(self, terrain):
        self.move(terrain)
        self.equip_cooldown += game.delta_time
