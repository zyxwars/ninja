import pygame as pg

from utils import debug
from .enemy import Enemy
import utils


class Patrol(Enemy):
    """Light-weight scout, low hp and damage, calls upon reinforcements when player is spotted."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sheet_parser = utils.SheetParser('assets/patrol_sheet.png', __file__)
        self.animations = {'idle': sheet_parser.load_images_row((0, 0), 3, (64, 64)),
                           'attack': sheet_parser.load_images_row((0, 1), 4, (64, 64)),
                           'jump': sheet_parser.load_images_row((0, 2), 1, (64, 64)),
                           'fall': sheet_parser.load_images_row((0, 3), 1, (64, 64)),
                           'run': sheet_parser.load_images_row((0, 4), 2, (64, 64)),
                           'push': sheet_parser.load_images_row((0, 5), 3, (64, 64)),
                           'wallslide': sheet_parser.load_images_row((0, 6), 1, (64, 64))}
        self.hp = 100

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
            self.patrol()

        super().update(player, *args, **kwargs)
