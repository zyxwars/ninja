import pygame as pg
import math

from ..animated_humanoid import AnimatedHumanoid
import config
import utils
import game


class BaseEnemy(AnimatedHumanoid):
    def __init__(self, pos, size):
        sheet_parser = utils.SheetParser(
            __file__, 'assets/enemy_sheet.png')
        self.image = pg.Surface(size).convert_alpha()

        self.animations = {'idle': sheet_parser.load_images_row((0, 0), 3, size),
                           'attack': sheet_parser.load_images_row((0, 1), 4, size),
                           'jump': sheet_parser.load_images_row((0, 2), 1, size),
                           'fall': sheet_parser.load_images_row((0, 3), 1, size),
                           'run': sheet_parser.load_images_row((0, 4), 3, size),
                           'push': sheet_parser.load_images_row((0, 5), 3, size),
                           'wall_slide': sheet_parser.load_images_row((0, 6), 1, size)}

        super().__init__(self.image.get_rect(topleft=pos), self.animations)

        self.speed = config.ENEMY_SPEED

    def update(self, tiles, player_pos):
        self.dir.x = 0

        if self.rect.centerx > player_pos[0]:
            self.dir.x = -1
        elif self.rect.centerx < player_pos[0]:
            self.dir.x = 1

        if self.touching_wall and self.is_grounded:
            self.dir.y = -1.5

        self.move(tiles)
        self.animate()
