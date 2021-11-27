import pygame as pg
import math

from ..physics_entity import PhysicsEntity
import config
import utils
import shared_data


class BaseEnemy(PhysicsEntity):
    def __init__(self, pos, *args, **kwargs):
        sheet_parser = utils.SpriteSheetParser(
            __file__, 'assets/enemy_sheet.png')
        size = (64, 64)
        self.image = pg.Surface(size).convert_alpha()
        super().__init__(self.image.get_rect(topleft=pos), *args, **kwargs)

        self.speed = config.ENEMY_SPEED

        self.idle_animation = sheet_parser.load_row((0, 0), 3, size)
        self.attack_animation = sheet_parser.load_row((0, 1), 4, size)
        # Attack speed is directly tied to the attack animation speed
        self.is_attacking = False
        self.jump_animation = sheet_parser.load_row((0, 2), 1, size)
        self.fall_animation = sheet_parser.load_row((0, 3), 1, size)
        self.run_animation = sheet_parser.load_row((0, 4), 3, size)
        self.wall_jump_animation = sheet_parser.load_row((0, 5), 1, size)
        self.animation = []
        self.animation_index = 0
        self.animation_speed = config.PLAYER_ANIMATION_SPEED

    def update(self, tiles, player_pos):
        self.dir.x = 0

        if self.rect.centerx > player_pos[0]:
            self.dir.x = -1
        elif self.rect.centerx < player_pos[0]:
            self.dir.x = 1

        if self.touching_wall and self.is_grounded:
            self.dir.y = -1.5

        self.move(tiles)
        self.animate()

    def animate(self):
        self.animation_speed = config.PLAYER_ANIMATION_SPEED

        last_frame_animation = self.animation

        # Attacking
        if self.is_attacking:
            self.animation = self.attack_animation
            self.animation_speed = config.PLAYER_ATTACK_SPEED
        # Running
        elif self.is_grounded and self.dir.x != 0:
            self.animation = self.run_animation
        # Jumping
        elif self.dir.y < 0:
            if self.touching_wall:
                self.animation = self.wall_jump_animation
            else:
                self.animation = self.jump_animation
        # Touching wall
        elif self.touching_wall:
            if self.is_grounded:
                pass
            else:
                pass
        # Falling
        elif self.dir.y >= 0.5 and not self.is_grounded:
            self.animation = self.fall_animation
        # Idle
        else:
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

        self.animation_index += self.animation_speed * shared_data.delta_time
