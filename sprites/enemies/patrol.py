import pygame as pg

from utils import debug
from .base_enemy import BaseEnemy


class Patrol(BaseEnemy):
    """Light-weight scout, low hp and damage, calls upon reinforcements when player is spotted."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hp = 100

    def update(self, player, *args, **kwargs):
        self.spot_player(player)

        if self.alert_timer > 0:
            if self.alert_timer < self.alert_timer_ms / 2:
                self.roam(0.001)
            else:
                self.follow(player.rect.center)
                self.attack(player)
        else:
            self.patrol()

        super().update(*args, **kwargs)
