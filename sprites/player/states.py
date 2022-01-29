import pygame as pg

import utils
from sprites.damageable import Damageable
from sprites.physics_entity import PulledByGravity, PhysicsEntity
from sprites.weapons.punch import Punch
from sprites.weapons.weapon import CollectableWeapon
from utils import debug
from utils.statemachine import StateMachine
from .player import Player


class Moving(PulledByGravity):
    def __init__(self, name, player: Player):
        self.name = name
        self._sm = player

    def update(self):
        mouse = pg.mouse.get_pressed()
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self._sm.dir.x = -1
        elif keys[pg.K_d]:
            self._sm.dir.x = 1
        else:
            self._sm.dir.x = 0

        if mouse[0]:
            self._sm.set_state('attack')
            return

        super().update()


class Idling(Moving):
    def __init__(self, *args, **kwargs):
        super().__init__('idle', *args, **kwargs)

    def enter(self):
        self._sm.animation = self._sm.animations['idle']
        self._sm.dir.x = 0

    def update(self):
        super().update()

        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE]:
            self._sm.set_state('jump')
            return
        if keys[pg.K_a] or keys[pg.K_d]:
            self._sm.set_state('run')
            return
        if self._sm.dir.y > 1:
            self._sm.set_state('fall')
            return


class Running(Moving):
    def __init__(self, *args, **kwargs):
        super().__init__('run', *args, **kwargs)

    def enter(self):
        self._sm.animation = self._sm.animations['run']

    def update(self):
        super().update()

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self._sm.set_state('jump')
            return

        if self._sm.dir.x == 0:
            self._sm.set_state('idle')
            return
        if self._sm.dir.y > 1:
            self._sm.set_state('fall')
            return
        if self._sm.touching_wall:
            self._sm.set_state('push')
            return


class Pushing(Moving):
    def __init__(self, *args, **kwargs):
        super().__init__('push', *args, **kwargs)

    def enter(self):
        self._sm.animation = self._sm.animations['push']

    def update(self):
        super().update()

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self._sm.set_state('jump')
            return
        if self._sm.dir.y > 0:
            self._sm.set_state('fall')
            return
        if not self._sm.touching_wall:
            self._sm.set_state('idle')
            return


class Jumping(Moving):
    def __init__(self, *args, **kwargs):
        super().__init__('jump', *args, **kwargs)
        self.jump_sound = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/jump.wav'))
        self.jump_sound.set_volume(0.5)

    def enter(self):
        self._sm.animation = self._sm.animations['jump']
        PhysicsEntity.jump(self._sm)
        self.jump_sound.play()

    def update(self):
        super().update()

        if self._sm.dir.y >= 0 and self._sm.touching_wall:
            self._sm.set_state('wallslide')
            return
        if self._sm.dir.y > 0.5:
            self._sm.set_state('fall')
            return
        if self._sm.is_grounded:
            self._sm.set_state('idle')
            return


class Falling(Moving):
    def __init__(self, *args, **kwargs):
        super().__init__('fall', *args, **kwargs)
        self.land_sound = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/land.wav'))
        self.land_sound.set_volume(0.1)

        self.last_y_speed = 0

    def enter(self):
        self.last_y_speed = 0
        self._sm.animation = self._sm.animations['fall']

    def update(self):
        super().update()

        if self._sm.touching_wall:
            self._sm.set_state('wallslide')
            return
        if self._sm.is_grounded:
            self._sm.set_state('idle')
            return

        self.last_y_speed = self._sm.dir.y

    def exit(self):
        if self.last_y_speed > 1:
            self.land_sound.play()


class Wallsliding(Moving):
    def __init__(self, *args, **kwargs):
        super().__init__('wallslide', *args, **kwargs)

    def enter(self):
        self._sm.animation = self._sm.animations['wallslide']

    def update(self):
        self._sm.dir.y = min(self._sm.dir.y, 0.25)

        super().update()

        if not self._sm.touching_wall or self._sm.is_grounded:
            self._sm.set_state('idle')
            return


# class AttackState(GravityState):
#     def __init__(self, *args, **kwargs):
#         super().__init__('attack', *args, **kwargs)
#         self.original_animation_speed = 0

#     def enter(self):
#         attack_rect = self._sm.rect.copy()
#         attack_rect.x += 8 if self._sm.facing_right else -8

#         for enemy in enemies:
#             if attack_rect.colliderect(enemy.rect):
#                 if isinstance(enemy, enemy.Enemy):
#                     # Enemy.damage returns true if entity died
#                     if enemy.damage(self._sm.weapon.damage * 10 if (enemy.facing_right and self._sm.facing_right) or (not enemy.facing_right and not self._sm.facing_right) else self._sm.weapon.damage):
#                         # Heal self._sm
#                         self._sm.hp = min(self._sm.hp + 25, 100)

#         self._sm.animation = self._sm.animations['attack'][self._sm.weapon.name]
#         self.original_animation_speed = self._sm.animation_speed
#         self._sm.animation_speed = self._sm.animation_speed = (
#             self._sm.weapon.attack_length_ms / len(self._sm.animations['attack'][self._sm.weapon.name])) ** -1

#     def update(self):
#         self._sm.dir.x = 0
#         self._sm.move([*terrain, *enemies])

#         if self._sm.animation_index >= len(self._sm.animation):
#             self._sm.set_state('idle')
#             return

#     def exit(self):
#         self._sm.animation_speed = self.original_animation_speed
