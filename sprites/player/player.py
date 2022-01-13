import pygame as pg

import config
from sprites.damageable import Damageable
from utils import debug
import utils
import game
from ..animated_humanoid import AnimatedHumanoid
import utils


class Player(AnimatedHumanoid, Damageable):
    def __init__(self, pos, scale):
        sheet_parser = utils.SheetParser(
            __file__, 'assets/player_sheet.png')
        self.image = pg.Surface(scale).convert_alpha()

        self.animations = {'idle': sheet_parser.load_images_row((0, 0), 3, scale),
                           'attack': sheet_parser.load_images_row((0, 1), 4, scale),
                           'jump': sheet_parser.load_images_row((0, 2), 1, scale),
                           'fall': sheet_parser.load_images_row((0, 3), 1, scale),
                           'run': sheet_parser.load_images_row((0, 4), 2, scale),
                           'push': sheet_parser.load_images_row((0, 5), 3, scale),
                           'wall_slide': sheet_parser.load_images_row((0, 6), 1, scale)}

        self.jump_sound = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/jump.wav'))
        self.jump_sound.set_volume(0.5)
        self.last_jumped = 1000

        self.land_sound = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/land.wav'))
        self.land_sound.set_volume(0.1)
        self.last_grounded = False
        self.last_gravity = 0

        AnimatedHumanoid.__init__(
            self, self.image.get_rect(topleft=pos), self.animations)
        Damageable.__init__(self, 100, lambda: print(
            f'damaged {self}'), lambda: print('oof'))

    def debug(self):
        debug.debug('rect', self.rect)
        debug.debug('jumped_from_wall', self.jumped_from_wall)
        debug.debug('touching_wall', self.touching_wall)
        debug.debug('is_grounded', self.is_grounded)
        debug.debug('dir', self.dir)
        debug.debug('attacking', self.is_attacking)

    def draw(self, screen, shift: pg.Vector2):
        screen.blit(self.image, (self.rect.x +
                    int(shift.x), self.rect.y + int(shift.y)))

    def update(self, tiles, entities):
        self.debug()
        self.get_input(entities)
        self.move(tiles)
        self.animate()

        # Play land sound logic
        self.last_jumped += game.delta_time

        if self.is_grounded != self.last_grounded:
            if self.is_grounded and self.last_gravity > 1:
                self.land_sound.play()
        self.last_grounded = self.is_grounded
        self.last_gravity = self.dir.y

        return self.rect.center

    def get_input(self, entities):
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()

        if keys[pg.K_a]:
            self.dir.x = -1
        elif keys[pg.K_d]:
            self.dir.x = 1
        else:
            self.dir.x = 0

        if keys[pg.K_SPACE]:
            self.jump()

        if mouse[0]:
            self.attack(entities)

    def jump(self):
        if self.is_grounded:
            self.jumped_from_wall = False
        elif self.touching_wall == 'right':
            if self.jumped_from_wall == 'right':
                return
            self.jumped_from_wall = 'right'

        elif self.touching_wall == 'left':
            if self.jumped_from_wall == 'left':
                return
            self.jumped_from_wall = 'left'
        else:
            return

        if self.last_jumped > 300:
            self.jump_sound.play()
            self.last_jumped = 0

        super().jump()

    def attack(self, entities):
        if self.is_attacking:
            return

        self.is_attacking = True

        for entity in entities:
            if entity is self:
                continue

            # TODO: use collidelist
            temp_rect = self.rect.copy()
            temp_rect.x += 32 if self.facing_right else -32

            if temp_rect.colliderect(entity.rect):
                if isinstance(entity, Damageable):
                    entity.damage(50)
