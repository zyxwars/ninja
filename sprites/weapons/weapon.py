import random
import pygame as pg

from ..physics_entity import PhysicsEntity
from utils import get_path
import game

from ..collectable import Collectable


class Weapon:
    sounds: list[pg.mixer.Sound] = []

    def __init__(self, damage, attack_length_ms, name):
        self.image = pg.image.load(
            get_path(__file__, f'assets/{name}.png')).convert_alpha()
        self.damage = damage
        self.attack_length_ms = attack_length_ms
        self.name = name

    def play_sound(self):
        if len(self.sounds) == 0:
            return

        sound = random.choice(self.sounds)

        sound.play()


class CollectableWeapon(Weapon, Collectable):
    def __init__(self, damage, attack_length_ms, name, *args, pos, **kwargs):
        Weapon.__init__(self, damage, attack_length_ms, name)
        if pos:
            Collectable.__init__(self, self.image, pos, *args, **kwargs)
