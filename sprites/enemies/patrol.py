import pygame as pg

from utils import debug
from .enemy import Enemy
import utils
from . import states


class Patrol(Enemy):
    """Semi-heavy class, usually patrols single route until alerted"""

    def __init__(self, pos, patrol_area, collidables, player):

        sheet_parser = utils.SheetParser('assets/patrol_sheet.png', __file__)
        animations = {'idling': sheet_parser.load_images_row((0, 0), 3, (64, 64)),
                      'attacking': sheet_parser.load_images_row((0, 1), 4, (64, 64)),
                      'jumping': sheet_parser.load_images_row((0, 2), 1, (64, 64)),
                      'falling': sheet_parser.load_images_row((0, 3), 1, (64, 64)),
                      'walking': sheet_parser.load_images_row((0, 4), 2, (64, 64)),
                      'pushing': sheet_parser.load_images_row((0, 5), 3, (64, 64)),
                      'wallsliding': sheet_parser.load_images_row((0, 6), 1, (64, 64)),
                      'running': sheet_parser.load_images_row((0, 7), 2, (64, 64)), }

        super().__init__(pos, patrol_area, collidables, player, animations)
        self.hp = 100
        self.attack_length = 250

        self.add_state(states.Patrolling(self))
        self.add_state(states.Attacking(self))
        self.add_state(states.Jumping(self))
        self.add_state(states.Falling(self))
        self.add_state(states.Chasing(self))
        self.add_state(states.Searching(self))
        self.add_state(states.Idling(self))
        self.set_state('patrolling')
