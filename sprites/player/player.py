import pygame as pg
import math

import config
from sprites.damageable import Damageable
from sprites.physics_entity import GravityState, PhysicsEntity
from utils.statemachine import StateMachine
from sprites.weapons.punch import Punch
from sprites.weapons.weapon import CollectableWeapon
from utils import debug
import game
import utils

# TODO: rework state methods to use _sm instead of expecting a prop to be passed to their update method


class MoveState(GravityState):
    def __init__(self, name, player: 'Player'):
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


class IdleState(MoveState):
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


class RunState(MoveState):
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


class PushState(MoveState):
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


class JumpState(MoveState):
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


class FallState(MoveState):
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


class WallslideState(MoveState):
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
        self.add_state(IdleState(self))
        self.add_state(RunState(self))
        self.add_state(PushState(self))
        self.add_state(JumpState(self))
        self.add_state(FallState(self))
        self.add_state(WallslideState(self))
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
