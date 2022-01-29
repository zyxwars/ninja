import pygame as pg
import math

import config
from sprites.damageable import Damageable
from sprites.groups.collectable_group import CollectableGroup
from sprites.physics_entity import PulledByGravity, PhysicsEntity
from utils.statemachine import StateMachine
from sprites.weapons.punch import Punch
from sprites.weapons.weapon import CollectableWeapon, Weapon
from utils import debug
import game
import utils


class Player(PhysicsEntity, Damageable, StateMachine):
    def __init__(self, pos, collidables: tuple[pg.sprite.Group, ...], collectables: CollectableGroup):
        # Avoid circular import
        from . import states

        self.image = pg.Surface((64, 64)).convert()
        PhysicsEntity.__init__(
            self, self.image.get_rect(topleft=pos), collidables)
        Damageable.__init__(self, 100)
        self.collectables = collectables

        # Animation
        sheet_parser = utils.SheetParser('assets/player_sheet.png', __file__)
        attack_sheet_parse = utils.SheetParser(
            'assets/attack_sheet.png', __file__)
        self.animations = {'idling': sheet_parser.load_images_row((0, 0), 3, (64, 64)),
                           'attacking':
                           # Attacks reflect the weapon class name not the "ing" state
                           {'punch': attack_sheet_parse.load_images_row((0, 0), 4, (64, 64)),
                            'kick': attack_sheet_parse.load_images_row((0, 1), 7, (64, 64)),
                            'katana': attack_sheet_parse.load_images_row((0, 2), 6, (64, 64))
                            },
                           'jumping': sheet_parser.load_images_row((0, 2), 1, (64, 64)),
                           'falling': sheet_parser.load_images_row((0, 3), 1, (64, 64)),
                           'running': sheet_parser.load_images_row((0, 4), 2, (64, 64)),
                           'pushing': sheet_parser.load_images_row((0, 5), 3, (64, 64)),
                           'wallsliding': sheet_parser.load_images_row((0, 6), 1, (64, 64))}
        self.animation = self.animations['idling']
        self.animation_index = 0
        self.animation_speed = config.ANIMATION_SPEED
        self.last_animation = self.animation

        self.weapon: Weapon = Punch()
        self.jumped_from_wall = False

        self.punch_sounds = []
        for sound_name in range(1, 38):
            sound = pg.mixer.Sound(
                utils.get_path(__file__, f'assets/hits/hit{sound_name:02d}.mp3.flac'))
            sound.set_volume(0.5)
            self.punch_sounds.append(sound)

        StateMachine.__init__(self)
        self.add_state(states.Idling(self))
        self.add_state(states.Running(self))
        self.add_state(states.Pushing(self))
        self.add_state(states.Jumping(self))
        self.add_state(states.Falling(self))
        self.add_state(states.Wallsliding(self))
        self.add_state(states.Collecting(self))
        self.add_state(states.Dropping(self))
        self.set_state('idling')

    def on_died(self):
        pass

    def on_damaged(self):
        print('ouch')

    def animate(self):
        if self.animation_index >= len(self.animation) or self.last_animation != self.animation:
            self.animation_index = 0

        # flip_x = !facing_right, flip image only when not facing right
        self.image = pg.transform.flip(self.animation[math.floor(
            self.animation_index)], not self.facing_right, False)

        self.animation_index += self.animation_speed * game.delta_time

        self.last_animation = self.animation

    def update(self):
        debug.debug('rect', self.rect)
        debug.debug('jumped_from_wall', self.jumped_from_wall)
        debug.debug('touching_wall', self.touching_wall)
        debug.debug('is_grounded', self.is_grounded)
        debug.debug('dir', self.dir)
        debug.debug('state', self.current_state.name)

        self.current_state.update()
        self.animate()

        return self.rect.center

    def draw(self, screen, shift: pg.Vector2):
        screen.blit(self.image, (self.rect.x +
                    int(shift.x), self.rect.y + int(shift.y)))
