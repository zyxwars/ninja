from distutils.log import debug
from lib2to3.pytree import Base
import pygame as pg

from utils import debug
from .base_enemy import BaseEnemy


class Prowler(BaseEnemy):
    """Light-weight scout, low hp and damage, calls upon reinforcements when player is spotted."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hp = 50

    def update(self, player, *args, **kwargs):
        self.spot_player(player)

        if self.is_alert:
            self.follow(player.rect)
            self.attack(player)
        else:
            self.roam()
        super().update(*args, **kwargs)