from typing import Tuple
import pygame as pg

from ..physics_entity import PhysicsEntity
from utils import get_path
import game

from ..collectable import Collectable


class Weapon(Collectable):
    def __init__(self, damage, attack_length_ms, name, pos=(0, 0), *args, **kwargs):
        self.image = pg.image.load(
            get_path(__file__, f'assets/{name}.png')).convert_alpha()
        super().__init__(self.image, pos, *args, **kwargs)

        self.damage = damage
        self.attack_length_ms = attack_length_ms
        self.name = name
