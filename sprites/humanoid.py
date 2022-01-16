import pygame as pg
import math

from sprites.weapons.weapon import Weapon

from .physics_entity import PhysicsEntity
import game
import config
from utils import debug
from .damageable import Damageable

from .weapons.punch import Punch


class Humanoid(PhysicsEntity):
    def __init__(self, rect):
        super().__init__(rect)

        self.animations = {'idle': [], 'attack': {'punch': []}, 'jump': [],
                           'fall': [], 'run': [], 'push': [], 'wallslide': []}
        self.animation = 'idle'
        self.animation_index = 0

        self.animation_speed = config.ANIMATION_SPEED
        self.weapon = Punch()

        # Attack speed is directly tied to the attack animation speed
        self.is_attacking = False
        self.jumped_from_wall = False

    def attack(self, entities, attack_sound, hit_sound):
        if self.is_attacking:
            return

        is_hit = False
        self.is_attacking = True

        attack_rect = self.rect.copy()
        attack_rect.x += 8 if self.facing_right else -8

        for entity in entities:
            if entity is self:
                continue

            if attack_rect.colliderect(entity.rect):
                if isinstance(entity, Damageable):
                    hit_sound.play()
                    entity.damage(self.weapon.damage)
                    is_hit = True

        if not is_hit:
            attack_sound.play()

    def collect(self, collectables):
        for collectable in collectables:
            if collectable.rect.colliderect(self.rect):
                if isinstance(collectable, Weapon):
                    self.weapon = collectable.equip()
                break

    def animate(self):
        last_frame_animation = self.animation

        # Attacking
        if self.is_attacking:
            self.animation = 'attack'
            self.animation_speed = (
                self.weapon.attack_length_ms / len(self.animations['attack'][self.weapon.name])) ** -1
        # Touching wall
        elif self.touching_wall:
            # Running against wall
            if self.is_grounded:
                self.animation = 'push'
            # Wall sliding
            else:
                self.animation = 'wallslide'
                # Slow down gravity when player is wallsliding
                self.dir.y = min(self.dir.y, 0.5)
        # Running
        elif self.is_grounded and self.dir.x != 0:
            self.animation = 'run'
        # Jumping
        elif self.dir.y < 0:
            self.animation = 'jump'
        # Falling
        elif (self.animation in ['jump', 'fall'] and self.dir.y > 0.5) or self.dir.y > 1:
            self.animation = 'fall'
        # Idle
        elif self.dir == pg.Vector2(0, 0):
            self.animation = 'idle'

        # Restart animation  when animation state changes
        # This is required since attack speed is tied to the animation,
        # animation starting on index > 0 caused the attack cooldown to reset early
        if last_frame_animation != self.animation:
            self.animation_index = 0

        if self.animation == 'attack':
            # End attack animation after it played once
            if self.animation_index >= len(self.animations['attack'][self.weapon.name]):
                self.animation_index = 0
                self.animation = 'idle'
                self.is_attacking = False
                self.animation_speed = config.ANIMATION_SPEED
        else:
            if self.animation_index >= len(self.animations[self.animation]):
                self.animation_index = 0

        if self.animation == 'attack':
            self.image = pg.transform.flip(
                self.animations['attack'][self.weapon.name][math.floor(self.animation_index)], not self.facing_right, False)
        else:
            # flip_x = !facing_right, flip image only when not facing right
            self.image = pg.transform.flip(
                self.animations[self.animation][math.floor(self.animation_index)], not self.facing_right, False)

        self.animation_index += self.animation_speed * game.delta_time
