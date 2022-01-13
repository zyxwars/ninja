import pygame as pg
import random
import math

from sprites.damageable import Damageable

from ..animated_humanoid import AnimatedHumanoid
import config
import utils
import game


class BaseEnemy(AnimatedHumanoid, Damageable):
    def __init__(self, pos, size):
        sheet_parser = utils.SheetParser(
            __file__, 'assets/enemy_sheet.png')
        self.image = pg.Surface(size).convert_alpha()

        self.animations = {'idle': sheet_parser.load_images_row((0, 0), 3, size),
                           'attack': sheet_parser.load_images_row((0, 1), 4, size),
                           'jump': sheet_parser.load_images_row((0, 2), 1, size),
                           'fall': sheet_parser.load_images_row((0, 3), 1, size),
                           'run': sheet_parser.load_images_row((0, 4), 2, size),
                           'push': sheet_parser.load_images_row((0, 5), 3, size),
                           'wall_slide': sheet_parser.load_images_row((0, 6), 1, size)}

        super().__init__(self.image.get_rect(topleft=pos), self.animations)
        Damageable.__init__(self, 100, lambda: print(
            f'damaged {self.rect.topleft}'), self.kill)

        self.speed = config.SPEED * 0.5
        self.patrol_route = [600, 1000]
        self.roam_route = [10, 1000]

    def patrol(self):
        if self.touching_wall and self.is_grounded:
            self.jump()

        if self.dir.x == 0:
            self.dir.x = random.randint(-1, 1)
            return

        # Reverse direction
        if self.pos.x < self.patrol_route[0] or self.pos.x > self.patrol_route[1]:
            self.dir.x = - self.dir.x

    def follow(self, pos):
        if self.touching_wall and self.is_grounded:
            self.jump()

        if self.rect.centerx > pos[0]:
            self.dir.x = -1
        elif self.rect.centerx < pos[0]:
            self.dir.x = 1
        else:
            self.dir.x = 0

    def roam(self):
        if self.touching_wall and self.is_grounded:
            # Sometimes turn and sometimes jump over obstacles
            if random.random() < 0.5:
                self.jump()
            else:
                self.dir.x = -self.dir.x

            return

        if self.dir.x == 0:
            self.dir.x = random.randint(-1, 1)
            return

        # Reverse direction
        if self.pos.x < self.roam_route[0] or self.pos.x > self.roam_route[1]:
            self.dir.x = - self.dir.x

        # Make the chance equal with different fps > delta_time
        if random.random() < 0.001 * game.delta_time:
            self.dir.x = -self.dir.x

    def update(self, tiles):
        self.move(tiles)
        self.animate()
