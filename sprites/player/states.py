import time
import pygame as pg
import random

import config
import game
from sprites.flag import Flag
import utils
from sprites.damageable import Damageable
from sprites.physics_entity import PulledByGravity, PhysicsEntity
from sprites.weapons.punch import Punch
from sprites.weapons.weapon import CollectableWeapon
from utils import debug
from utils import groups_to_sprites
from utils.statemachine import StateMachine
from .player import Player


class Moving(PulledByGravity):
    def __init__(self, name, player: Player):
        self.name = name
        self._sm = player

    def update(self):
        alert_rect = self._sm.rect.inflate(*self._sm.alert_area)
        debug.debug_rect(alert_rect, 'red')
        debug.debug_rect(self._sm.rect, 'blue')

        for enemy in self._sm.enemies.sprites():
            if alert_rect.colliderect(enemy.rect):
                direct_rect = pg.rect.Rect(
                    enemy.rect.x if enemy.rect.x < self._sm.rect.x else self._sm.rect.x, enemy.rect.y, abs(enemy.rect.x - self._sm.rect.x), 10)
                debug.debug_rect(direct_rect, 'yellow')
                for tile in self._sm.terrain.sprites():
                    if tile.rect.colliderect(direct_rect):
                        break
                else:
                    if (enemy.rect.x < self._sm.rect.x and enemy.facing_right) or (enemy.rect.x > self._sm.rect.x and not enemy.facing_right):
                        enemy.alert(self._sm.rect.center)

        mouse = pg.mouse.get_pressed()
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self._sm.dir.x = -1
        elif keys[pg.K_d]:
            self._sm.dir.x = 1
        else:
            self._sm.dir.x = 0

        if mouse[0] and not self._sm.current_state.name == 'attacking':
            self._sm.set_state('attacking')
            return

        super().update()


class Idling(Moving):
    def __init__(self, *args, **kwargs):
        super().__init__('idling', *args, **kwargs)

    def enter(self):
        self._sm.animation = self._sm.animations['idling']
        self._sm.dir.x = 0

    def update(self):
        super().update()

        for e in game.events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_e:
                    self._sm.set_state('collecting')
                    return
                if e.key == pg.K_g:
                    self._sm.set_state('dropping')
                    return

        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE] and not self._sm.is_roofed:
            self._sm.set_state('jumping')
            return
        if keys[pg.K_a] or keys[pg.K_d]:
            self._sm.set_state('running')
            return
        if self._sm.dir.y > 1:
            self._sm.set_state('falling')
            return


class Running(Moving):
    def __init__(self, *args, **kwargs):
        super().__init__('running', *args, **kwargs)

    def enter(self):
        self._sm.animation = self._sm.animations['running']

    def update(self):
        super().update()

        for e in game.events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_e:
                    self._sm.set_state('collecting')
                    return
                if e.key == pg.K_g:
                    self._sm.set_state('dropping')
                    return

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and not self._sm.is_roofed:
            self._sm.set_state('jumping')
            return

        if self._sm.dir.x == 0:
            self._sm.set_state('idling')
            return
        if self._sm.dir.y > 1:
            self._sm.set_state('falling')
            return
        if self._sm.touching_wall:
            self._sm.set_state('pushing')
            return


class Pushing(Moving):
    def __init__(self, *args, **kwargs):
        super().__init__('pushing', *args, **kwargs)

    def enter(self):
        self._sm.animation = self._sm.animations['pushing']

    def update(self):
        super().update()

        for e in game.events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_e:
                    self._sm.set_state('collecting')
                    return
                if e.key == pg.K_g:
                    self._sm.set_state('dropping')
                    return

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self._sm.set_state('jumping')
            return
        if self._sm.dir.y > 0:
            self._sm.set_state('falling')
            return
        if not self._sm.touching_wall:
            self._sm.set_state('idling')
            return


class Jumping(Moving):
    def __init__(self, *args, **kwargs):
        super().__init__('jumping', *args, **kwargs)
        self.jump_sound = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/jump.wav'))
        self.jump_sound.set_volume(0.5)

        self.last_jumped = time.time()

    def enter(self):
        self._sm.animation = self._sm.animations['jumping']
        PhysicsEntity.jump(self._sm)

        if time.time() - self.last_jumped > 0.5:
            self.jump_sound.play()
            self.last_jumped = time.time()

    def update(self):
        super().update()

        if self._sm.dir.y >= 0 and self._sm.touching_wall:
            self._sm.set_state('wallsliding')
            return
        if self._sm.dir.y > 0.5:
            self._sm.set_state('falling')
            return
        if self._sm.is_grounded:
            self._sm.set_state('idling')
            return


class Falling(Moving):
    def __init__(self, *args, **kwargs):
        super().__init__('falling', *args, **kwargs)
        self.land_sound = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/land.wav'))
        self.land_sound.set_volume(0.1)

        self.last_y_speed = 0

    def enter(self):
        self.last_y_speed = 0
        self._sm.animation = self._sm.animations['falling']

    def update(self):
        super().update()

        if self._sm.touching_wall:
            self._sm.set_state('wallsliding')
            return
        if self._sm.is_grounded:
            self._sm.set_state('idling')
            return

        self.last_y_speed = self._sm.dir.y

    def exit(self):
        if self.last_y_speed > 1:
            self.land_sound.play()


class Wallsliding(Moving):
    def __init__(self, *args, **kwargs):
        super().__init__('wallsliding', *args, **kwargs)

    def enter(self):
        self._sm.animation = self._sm.animations['wallsliding']

    def update(self):
        self._sm.dir.y = min(self._sm.dir.y, 0.25)

        super().update()

        if not self._sm.touching_wall or self._sm.is_grounded:
            self._sm.set_state('idling')
            return


class Collecting(Moving):
    def __init__(self, *args, **kwargs):
        super().__init__('collecting', *args, **kwargs)
        self.flag_sound = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/success.mp3'))
        self.flag_sound.set_volume(0.7)

    def enter(self):
        collectables = self._sm.collectables.sprites()

        i = self._sm.rect.collidelist(collectables)
        if i == -1:
            self._sm.set_state('idling')
            return

        collectable = collectables[i]

        if isinstance(collectable, CollectableWeapon):
            weapon = collectable.collect()
            if weapon:
                # Drop old weapon
                if isinstance(self._sm.weapon, CollectableWeapon):
                    self._sm.collectables.add(self._sm.weapon.drop(
                        (self._sm.rect.centerx + random.randint(0, 64) * (-1 if not self._sm.facing_right else 1), self._sm.rect.centery - 64)))

                self._sm.weapon = weapon
        else:
            if isinstance(collectable, Flag):
                self.flag_sound.play()
                collectable.collect()
                self._sm.flags_collected += 1

        self._sm.set_state('idling')


class Dropping(Moving):
    def __init__(self, *args, **kwargs):
        super().__init__('dropping', *args, **kwargs)

    def enter(self):
        if isinstance(self._sm.weapon, CollectableWeapon):
            self._sm.collectables.add(self._sm.weapon.drop(
                (self._sm.rect.centerx + random.randint(0, 64) * (-1 if not self._sm.facing_right else 1), self._sm.rect.centery - 64)))
            self._sm.weapon = Punch()

        self._sm.set_state('idling')


class Attacking(Moving):
    def __init__(self, player: Player, *args, **kwargs):
        self.name = 'attacking'
        self._sm = player

        self.original_animation_speed = 0

    def enter(self):
        attack_rect = self._sm.rect.copy()
        attack_rect.x += 8 if self._sm.facing_right else -8
        attack_rect.height += 16
        debug.debug_rect(attack_rect, 'green')

        for enemy in self._sm.enemies.sprites():
            if attack_rect.colliderect(enemy.rect):
                # Jump attack
                if enemy.rect.y - 32 > self._sm.rect.y:
                    damage = self._sm.weapon.damage * 10
                else:
                    damage = self._sm.weapon.damage * 10 if (enemy.facing_right and self._sm.facing_right) or (
                        not enemy.facing_right and not self._sm.facing_right) else self._sm.weapon.damage
                # Enemy.damage returns true if entity died
                if enemy.damage(damage):
                    # Heal self._sm
                    self._sm.hp = min(self._sm.hp + 25, 100)

        self._sm.animation = self._sm.animations['attacking'][self._sm.weapon.name]
        self.original_animation_speed = self._sm.animation_speed
        self._sm.animation_speed = self._sm.animation_speed = (
            self._sm.weapon.attack_length_ms / len(self._sm.animations['attacking'][self._sm.weapon.name])) ** -1

        self._sm.weapon.play_sound()

    def update(self):
        super().update()

        if self._sm.animation_index >= len(self._sm.animation):
            self._sm.set_state('idling')
            return

    def exit(self):
        self._sm.animation_speed = self.original_animation_speed
