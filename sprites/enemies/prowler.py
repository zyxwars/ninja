from lib2to3.pytree import Base
import pygame as pg

import utils
from .base_enemy import BaseEnemy


class Prowler(BaseEnemy):
    """Light-weight scout, low hp and damage, calls upon reinforcements when player is spotted."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hp = 50

    def update(self, *args, **kwargs):
        self.roam()
        super().update(*args, **kwargs)
