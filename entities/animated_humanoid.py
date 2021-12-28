import pygame as pg
import math

from .base_humanoid import BaseHumanoid
import game
import config
from utils import debug


class AnimatedHumanoid(BaseHumanoid):
    def __init__(self, rect, animations):
        super().__init__(rect)

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

        self.animation = []
        self.animation_index = 0

    def animate(self):
        last_frame_animation = self.animation

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
        elif self.dir == pg.math.Vector2(0, 0):
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
