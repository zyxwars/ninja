import pygame as pg
import math

from .physics_entity import PhysicsEntity
import game
import config
from utils import debug
from .damageable import Damageable


class Humanoid(PhysicsEntity):
    def __init__(self, rect, animations):
        super().__init__(rect)

        # TODO: Change the animatin initialization
        self.idle_animation = animations['idle']
        self.attack_animation = animations['attack']
        self.jump_animation = animations['jump']
        self.fall_animation = animations['fall']
        self.run_animation = animations['run']
        self.push_animation = animations['push']
        self.wall_slide_animation = animations['wall_slide']

        self.animation_speed = config.ANIMATION_SPEED
        self.attack_speed = config.ATTACK_SPEED

        # Attack speed is directly tied to the attack animation speed
        self.is_attacking = False
        self.jumped_from_wall = False

        self.animation = self.idle_animation
        self.animation_index = 0

    def attack(self, entities, attack_sound, hit_sound):
        if self.is_attacking:
            return

        is_hit = False
        self.is_attacking = True

        for entity in entities:
            if entity is self:
                continue

            # TODO: use collidelist
            attack_rect = self.rect.copy()
            attack_rect.x += 8 if self.facing_right else -8

            if attack_rect.colliderect(entity.rect):
                if isinstance(entity, Damageable):
                    hit_sound.play()
                    entity.damage(25)
                    is_hit = True

        if not is_hit:
            attack_sound.play()

    def animate(self):
        last_frame_animation = self.animation
        self.animation_speed = config.ANIMATION_SPEED

        # Attacking
        if self.is_attacking:
            self.animation = self.attack_animation
            self.animation_speed = self.attack_speed
        # Touching wall
        elif self.touching_wall:
            # Running against wall
            if self.is_grounded:
                self.animation = self.push_animation
            # Wall sliding
            else:
                self.animation = self.wall_slide_animation
                # Slow down gravity when player is wallsliding
                self.dir.y = min(self.dir.y, 0.5)
        # Running
        elif self.is_grounded and self.dir.x != 0:
            self.animation = self.run_animation
        # Jumping
        elif self.dir.y < 0:
            self.animation = self.jump_animation
        # Falling
        elif (self.animation in [self.jump_animation, self.fall_animation] and self.dir.y > 0.5) or self.dir.y > 1:
            self.animation = self.fall_animation
        # Idle
        elif self.dir == pg.Vector2(0, 0):
            self.animation = self.idle_animation

        # Restart animation  when animation state changes
        # This is required since attack speed is tied to the animation,
        # animation starting on index > 0 caused the attack cooldown to reset early
        if last_frame_animation != self.animation:
            self.animation_index = 0

        if self.animation_index >= len(self.animation):
            self.animation_index = 0
            # End attack animation after it played once
            if self.is_attacking:
                self.is_attacking = False

        # flip_x = !facing_right, flip image only when not facing right
        self.image = pg.transform.flip(
            self.animation[math.floor(self.animation_index)], not self.facing_right, False)

        self.animation_index += self.animation_speed * game.delta_time
