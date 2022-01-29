import pygame as pg
import math

import config
from sprites.damageable import Damageable
from sprites.physics_entity import PulledByGravity, PhysicsEntity
from utils.statemachine import StateMachine
from sprites.weapons.punch import Punch
from sprites.weapons.weapon import CollectableWeapon
from utils import debug
import game
import utils
from . import states


class Player(PhysicsEntity, Damageable, StateMachine):
    def __init__(self, pos, collides_with: tuple[pg.sprite.Group, ...]):
        self.image = pg.Surface((64, 64)).convert()
        PhysicsEntity.__init__(
            self, self.image.get_rect(topleft=pos), collides_with)
        Damageable.__init__(self, 100)

        # Animation
        sheet_parser = utils.SheetParser('assets/player_sheet.png', __file__)
        attack_sheet_parse = utils.SheetParser(
            'assets/attack_sheet.png', __file__)
        self.animations = {'idle': sheet_parser.load_images_row((0, 0), 3, (64, 64)),
                           'attack': {'punch': attack_sheet_parse.load_images_row((0, 0), 4, (64, 64)),
                                      'kick': attack_sheet_parse.load_images_row((0, 1), 7, (64, 64)),
                                      'katana': attack_sheet_parse.load_images_row((0, 2), 6, (64, 64))
                                      },
                           'jump': sheet_parser.load_images_row((0, 2), 1, (64, 64)),
                           'fall': sheet_parser.load_images_row((0, 3), 1, (64, 64)),
                           'run': sheet_parser.load_images_row((0, 4), 2, (64, 64)),
                           'push': sheet_parser.load_images_row((0, 5), 3, (64, 64)),
                           'wallslide': sheet_parser.load_images_row((0, 6), 1, (64, 64))}
        self.animation = self.animations['idle']
        self.animation_index = 0
        self.animation_speed = config.ANIMATION_SPEED
        self.last_animation = self.animation

        self.weapon = Punch()
        self.jumped_from_wall = False

        self.punch_sounds = []
        for sound_name in range(1, 38):
            sound = pg.mixer.Sound(
                utils.get_path(__file__, f'assets/hits/hit{sound_name:02d}.mp3.flac'))
            sound.set_volume(0.5)
            self.punch_sounds.append(sound)

        self.equip_cooldown = 250

        StateMachine.__init__(self)
        self.add_state(states.Idling(self))
        self.add_state(states.Running(self))
        self.add_state(states.Pushing(self))
        self.add_state(states.Jumping(self))
        self.add_state(states.Falling(self))
        self.add_state(states.Wallsliding(self))
        self.set_state('idle')

    def on_died(self):
        pass

    def on_damaged(self):
        print('ouch')

    # def collect(self, collectables_group):
    #     i = self.rect.collidelist(collectables_group.sprites())
    #     if i == -1:
    #         return

    #     collectable = collectables_group.sprites()[i]

    #     if isinstance(collectable, Weapon):
    #         to_equip = collectable.collect()
    #         if to_equip:
    #             self.drop(collectables_group)
    #             self.weapon = to_equip
    #             self.equip_cooldown = 0

    # def drop(self, collectables_group):
    #     if not isinstance(self.weapon, Punch):
    #         collectables_group.add(self.weapon.drop(
    #             (self.rect.centerx + random.randint(0, 64) * (-1 if not self.facing_right else 1), self.rect.centery - 64)))
    #         self.weapon = Punch()

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
