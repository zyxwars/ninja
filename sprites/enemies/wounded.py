import pygame as pg

from utils import debug
from .enemy import Enemy
import utils


class Wounded(Enemy):
    def __init__(self, pos, *args, **kwargs):
        super().__init__(pos, (0, 0), *args, **kwargs)
        # Animation
        sheet_parser = utils.SheetParser('assets/wounded_sheet.png', __file__)
        self.animations['idling'] = sheet_parser.load_images_row(
            (0, 0), 4, (64, 64))
        self.hp = 1

    def update(self, player, terrain):
        self.move([*terrain, player])
        self.animate(player)
