import random
import pygame as pg
import math

import config
from sprites.damageable import Damageable
# Avoid ImportError
import sprites.enemies.enemy as enemy
from sprites.physics_entity import PhysicsEntity
from sprites.weapons.punch import Punch
from sprites.weapons.weapon import Weapon
from utils import debug
import utils
import game
import utils


class Player(PhysicsEntity, Damageable):
    def __init__(self, pos):
        self.image = pg.Surface((64, 64)).convert()
        PhysicsEntity.__init__(
            self, self.image.get_rect(topleft=pos))
        Damageable.__init__(self, 100)

        self.state = 'idle'
        self.last_state = self.state

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

        self.weapon = Punch()
        self.jumped_from_wall = False

        # Sounds
        self.jump_sound = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/jump.wav'))
        self.jump_sound.set_volume(0.5)
        self.last_jumped = 1000

        self.land_sound = pg.mixer.Sound(
            utils.get_path(__file__, 'assets/land.wav'))
        self.land_sound.set_volume(0.1)
        self.last_grounded = False
        self.last_gravity = 0

        self.punch_sounds = []
        for sound_name in range(1, 38):
            sound = pg.mixer.Sound(
                utils.get_path(__file__, f'assets/hits/hit{sound_name:02d}.mp3.flac'))
            sound.set_volume(0.5)
            self.punch_sounds.append(sound)

        self.equip_cooldown = 250

    def on_died(self):
        pass

    def on_damaged(self):
        print('ouch')

    def attack(self, entities, attack_sound, hit_sound):
        if self.state == 'attack':
            return

        is_hit = False
        self.state = 'attack'

        attack_rect = self.rect.copy()
        attack_rect.x += 8 if self.facing_right else -8

        for entity in entities:
            if entity is self:
                continue

            if attack_rect.colliderect(entity.rect):
                if isinstance(entity, enemy.Enemy):
                    hit_sound.play()
                    # Returns true if entity died
                    if entity.damage(self.weapon.damage * 10 if (entity.facing_right and self.facing_right) or (not entity.facing_right and not self.facing_right) else self.weapon.damage):
                        self.hp = min(self.hp + 25, 100)

                    is_hit = True

        if not is_hit:
            attack_sound.play()

    def collect(self, collectables_group):
        i = self.rect.collidelist(collectables_group.sprites())
        if i == -1:
            return

        collectable = collectables_group.sprites()[i]

        if isinstance(collectable, Weapon):
            to_equip = collectable.collect()
            if to_equip:
                self.drop(collectables_group)
                self.weapon = to_equip
                self.equip_cooldown = 0

    def drop(self, collectables_group):
        if not isinstance(self.weapon, Punch):
            collectables_group.add(self.weapon.drop(
                (self.rect.centerx + random.randint(0, 64) * (-1 if not self.facing_right else 1), self.rect.centery - 64)))
            self.weapon = Punch()

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

    def get_input(self, enemies, collectables_group):
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
        if keys[pg.K_e]:
            if self.equip_cooldown > 250:
                self.collect(collectables_group)
        if keys[pg.K_g]:
            self.drop(collectables_group)

        if mouse[0]:
            self.attack(enemies, self.jump_sound,
                        random.choice(self.punch_sounds))

    def update_state(self):
        # Attacking
        if self.state == 'attack':
            pass
        # Touching wall
        elif self.touching_wall:
            # Running against wall
            if self.is_grounded:
                self.state = 'push'
            # Wall sliding
            else:
                self.state = 'wallslide'
        # Running
        elif self.is_grounded and self.dir.x != 0:
            self.state = 'run'
        # Jumping
        elif self.dir.y < 0:
            self.state = 'jump'
        # Falling
        elif (self.state in ['jump', 'fall'] and self.dir.y > 0.5) or self.dir.y > 1:
            self.state = 'fall'
        # Idle
        elif self.dir == pg.Vector2(0, 0):
            self.state = 'idle'

    def react_state(self):
        s = self.state

        self.animation = self.animations[s]

        if s == 'wallslide':
            # Slow down gravity when player is wallsliding
            self.dir.y = min(self.dir.y, 0.5)
        elif s == 'attack':
            self.animation_speed = (
                self.weapon.attack_length_ms / len(self.animations['attack'][self.weapon.name])) ** -1
            self.animation = self.animations['attack'][self.weapon.name]

            if self.animation_index >= len(self.animation):
                self.state = 'idle'
                self.animation_speed = config.ANIMATION_SPEED

    def animate(self):
        # Restart animation  when animation state changes
        # This is required since attack speed is tied to the animation, animation starting on index > 0 caused the attack cooldown to reset early
        if self.last_state != self.state or self.animation_index >= len(self.animation):
            self.animation_index = 0

        # flip_x = !facing_right, flip image only when not facing right
        self.image = pg.transform.flip(
            self.animation[math.floor(self.animation_index)], not self.facing_right, False)

        self.animation_index += self.animation_speed * game.delta_time

    def update(self, terrain, enemies, collectables_group):
        debug.debug('rect', self.rect)
        debug.debug('jumped_from_wall', self.jumped_from_wall)
        debug.debug('touching_wall', self.touching_wall)
        debug.debug('is_grounded', self.is_grounded)
        debug.debug('dir', self.dir)
        debug.debug('state', self.state)

        self.get_input(enemies, collectables_group)
        self.move([*terrain, *enemies])
        self.update_state()
        self.react_state()
        self.animate()

        # Play land sound logic
        self.last_jumped += game.delta_time

        if self.is_grounded != self.last_grounded:
            if self.is_grounded and self.last_gravity > 1:
                self.land_sound.play()
        self.last_grounded = self.is_grounded
        self.last_gravity = self.dir.y

        self.equip_cooldown += game.delta_time

        self.last_state = self.state

        return self.rect.center

    def draw(self, screen, shift: pg.Vector2):
        screen.blit(self.image, (self.rect.x +
                    int(shift.x), self.rect.y + int(shift.y)))
