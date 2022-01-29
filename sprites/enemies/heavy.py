import pygame as pg
import random

from utils import debug
from .enemy import Enemy
import utils
import config


class Heavy(Enemy):
    """Heavy, stands in place until alerted by other guards"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sheet_parser = utils.SheetParser('assets/heavy_sheet.png', __file__)
        self.animations = {'idling': sheet_parser.load_images_row((0, 0), 7, (64, 64)),
                           'attacking': sheet_parser.load_images_row((0, 1), 1, (64, 64)),
                           'jumping': sheet_parser.load_images_row((0, 2), 1, (64, 64)),
                           'falling': sheet_parser.load_images_row((0, 3), 1, (64, 64)),
                           'running': sheet_parser.load_images_row((0, 4), 2, (64, 64)),
                           'pushing': sheet_parser.load_images_row((0, 5), 3, (64, 64)),
                           'wallsliding': sheet_parser.load_images_row((0, 6), 1, (64, 64))}
        self.hp = 200
        self.speed = config.SPEED * (random.randrange(500, 2000) / 10000)

    def update(self, player, *args, **kwargs):
        self.spot_player(player)

        if self.alert_timer > 0:
            if self.alert_timer < self.alert_timer_ms / 2:
                self.roam(0.001)
            else:
                self.follow(player.rect.center)

                if not self.is_attacking:
                    attack_rect = self.rect.copy()
                    attack_rect.x += 16 if self.facing_right else -16
                    if attack_rect.colliderect(player):
                        self.is_attacking = True
        else:
            self.follow((self.patrol_area[0], 0))

        super().update(player, *args, **kwargs)
