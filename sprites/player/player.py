import random
from re import I
import pygame as pg
import math

import config
from sprites.damageable import Damageable
from sprites.physics_entity import PhysicsEntity
from utils.statemachine import StateMachine, State
from sprites.weapons.punch import Punch
from sprites.weapons.weapon import Weapon
from utils import debug
import game
import utils


class BaseState(State):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

    def enter(self, player, terrain=None, enemies=None, collectables_group=None):
        return self._enter(player, terrain, enemies, collectables_group)

    def _enter(self, player, terrain, enemies, collectables_group):
        pass

    def update(self, player, terrain=None, enemies=None, collectables_group=None):
        return self._update(player, terrain, enemies, collectables_group)

    def _update(self, player, terrain, enemies, collectables_group):
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            player.dir.x = -1
        elif keys[pg.K_d]:
            player.dir.x = 1
        else:
            player.dir.x = 0

        player.move([*terrain, *enemies])
        return None

    def exit(self, player, terrain=None, enemies=None, collectables_group=None):
        return self._exit(player, terrain, enemies, collectables_group)

    def _exit(self, player, terrain, enemies, collectables_group):
        pass


class IdleState(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__('idle', *args, **kwargs)

    def _enter(self, player, terrain, enemies, collectables_group):
        player.animation = player.animations['idle']
        player.dir.x = 0

    def _update(self, player, terrain, enemies, collectables_group):
        super()._update(player, terrain, enemies, collectables_group)

        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE]:
            return 'jump'
        if keys[pg.K_a] or keys[pg.K_d]:
            return 'run'
        if player.dir.y > 1:
            return 'fall'


class RunState(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__('run', *args, **kwargs)

    def _enter(self, player, terrain, enemies, collectables_group):
        player.animation = player.animations['run']

    def _update(self, player, terrain, enemies, collectables_group):
        super()._update(player, terrain, enemies, collectables_group)

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            return 'jump'

        if player.dir.x == 0:
            return 'idle'
        if player.dir.y > 1:
            return 'fall'
        if player.touching_wall:
            return 'push'


class PushState(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__('push', *args, **kwargs)

    def _enter(self, player, terrain, enemies, collectables_group):
        player.animation = player.animations['push']

    def _update(self, player, terrain, enemies, collectables_group):
        super()._update(player, terrain, enemies, collectables_group)

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            return 'jump'
        if player.dir.y > 0:
            return 'fall'
        if not player.touching_wall:
            return 'idle'


class JumpState(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__('jump', *args, **kwargs)
        self.jump_sound = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/jump.wav'))
        self.jump_sound.set_volume(0.5)

    def _enter(self, player, terrain, enemies, collectables_group):
        player.animation = player.animations['jump']
        PhysicsEntity.jump(player)
        self.jump_sound.play()

    def _update(self, player, terrain, enemies, collectables_group):
        super()._update(player, terrain, enemies, collectables_group)

        # keys = pg.key.get_pressed()
        # if keys[pg.K_SPACE]:
        #     return 'jump'

        if player.dir.y >= 0 and player.touching_wall:
            return 'wallslide'
        if player.dir.y > 0.5:
            return 'fall'
        if player.is_grounded:
            return 'idle'


class FallState(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__('fall', *args, **kwargs)
        self.land_sound = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/land.wav'))
        self.land_sound.set_volume(0.1)

        self.last_y_speed = 0

    def _enter(self, player, terrain, enemies, collectables_group):
        self.last_y_speed = 0
        player.animation = player.animations['fall']

    def _update(self, player, terrain, enemies, collectables_group):
        super()._update(player, terrain, enemies, collectables_group)

        if player.touching_wall:
            return 'wallslide'
        if player.is_grounded:
            return 'idle'

        self.last_y_speed = player.dir.y

        return None

    def _exit(self, player, terrain, enemies, collectables_group):
        if self.last_y_speed > 1:
            self.land_sound.play()


class WallslideState(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__('wallslide', *args, **kwargs)

    def _enter(self, player, terrain, enemies, collectables_group):
        player.animation = player.animations['wallslide']

    def _update(self, player, terrain, enemies, collectables_group):
        player.dir.y = min(player.dir.y, 0.25)

        super()._update(player, terrain, enemies, collectables_group)

        if not player.touching_wall or player.is_grounded:
            return 'idle'


class AttackState(BaseState):
    def __init__(self, *args, **kwargs):
        super().__init__('attack', *args, **kwargs)
        self.original_animation_speed = 0

    def _enter(self, player, terrain, enemies, collectables_group):
        attack_rect = player.rect.copy()
        attack_rect.x += 8 if player.facing_right else -8

        for enemy in enemies:
            if attack_rect.colliderect(enemy.rect):
                if isinstance(enemy, enemy.Enemy):
                    # Enemy.damage returns true if entity died
                    if enemy.damage(player.weapon.damage * 10 if (enemy.facing_right and player.facing_right) or (not enemy.facing_right and not player.facing_right) else player.weapon.damage):
                        # Heal player
                        player.hp = min(player.hp + 25, 100)

        player.animation = player.animations['attack'][player.weapon.name]
        self.original_animation_speed = player.animation_speed
        player.animation_speed = player.animation_speed = (
            player.weapon.attack_length_ms / len(player.animations['attack'][player.weapon.name])) ** -1

    def _exit(self, player, terrain, enemies, collectables_group):
        player.animation_speed = self.original_animation_speed


class Player(PhysicsEntity, Damageable, StateMachine):
    def __init__(self, pos):
        self.image = pg.Surface((64, 64)).convert()
        PhysicsEntity.__init__(
            self, self.image.get_rect(topleft=pos))
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
        self.add_state(IdleState())
        self.add_state(RunState())
        self.add_state(PushState())
        self.add_state(JumpState())
        self.add_state(FallState())
        self.add_state(WallslideState())
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
        if self.animation_index >= len(self.animation) or self.last_animation != self.last_animation:
            self.animation_index = 0

        # flip_x = !facing_right, flip image only when not facing right
        self.image = pg.transform.flip(self.animation[math.floor(
            self.animation_index)], not self.facing_right, False)

        self.animation_index += self.animation_speed * game.delta_time

        self.last_animation = self.animation

    def update(self, terrain, enemies, collectables_group):
        debug.debug('rect', self.rect)
        debug.debug('jumped_from_wall', self.jumped_from_wall)
        debug.debug('touching_wall', self.touching_wall)
        debug.debug('is_grounded', self.is_grounded)
        debug.debug('dir', self.dir)
        debug.debug('state', self.current_state.name)

        # self.get_input(enemies, collectables_group)
        # self.move([*terrain, *enemies])
        # self.update_state()
        # self.react_state()
        # self.animate()

        # # Play land sound logic
        # self.last_jumped += game.delta_time

        # if self.is_grounded != self.last_grounded:
        #     if self.is_grounded and self.last_gravity > 1:
        #         self.land_sound.play()
        # self.last_grounded = self.is_grounded
        # self.last_gravity = self.dir.y

        # self.equip_cooldown += game.delta_time

        # self.last_state = self.state

        self.update_state(self, terrain, enemies, collectables_group)
        self.animate()

        return self.rect.center

    def draw(self, screen, shift: pg.Vector2):
        screen.blit(self.image, (self.rect.x +
                    int(shift.x), self.rect.y + int(shift.y)))
