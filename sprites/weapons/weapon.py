from typing import Tuple
import pygame as pg

from ..physics_entity import PhysicsEntity
from utils import get_path
import game

from ..collectable import Collectable


class Weapon:
    def __init__(self, damage, attack_length_ms, name):
        self.image = pg.image.load(
            get_path(__file__, f'assets/{name}.png')).convert_alpha()
        self.damage = damage
        self.attack_length_ms = attack_length_ms
        self.name = name


class CollectableWeapon(Weapon, Collectable):
    def __init__(self, damage, attack_length_ms, name, *args, pos=(0, 0), **kwargs):
        Weapon.__init__(self, damage, attack_length_ms, name)
        Collectable.__init__(self, self.image, pos, *args, **kwargs)
