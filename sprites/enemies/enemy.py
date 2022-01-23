import pygame as pg
import random
import math
from sprites import enemies

from sprites.damageable import Damageable

import config
from sprites.physics_entity import PhysicsEntity
from sprites.player.player import Player
import utils
import game
from utils import debug


class Enemy(PhysicsEntity, Damageable):
    def __init__(self, pos, patrol_area):
        self.image = pg.Surface((64, 64)).convert()
        super().__init__(self.image.get_rect(topleft=pos))

        self.hp = 100
        self.speed = config.SPEED * (random.randrange(3, 7) / 10)
        self.base_speed = self.speed
        self.patrol_area = patrol_area
        self.alert_timer_ms = 4000
        self.alert_timer = 0

        # Animation
        sheet_parser = utils.SheetParser('assets/enemy_sheet.png', __file__)
        self.animations = {'idle': sheet_parser.load_images_row((0, 0), 3, (64, 64)),
                           'attack': sheet_parser.load_images_row((0, 1), 4, (64, 64)),
                           'jump': sheet_parser.load_images_row((0, 2), 1, (64, 64)),
                           'fall': sheet_parser.load_images_row((0, 3), 1, (64, 64)),
                           'run': sheet_parser.load_images_row((0, 4), 2, (64, 64)),
                           'push': sheet_parser.load_images_row((0, 5), 3, (64, 64)),
                           'wallslide': sheet_parser.load_images_row((0, 6), 1, (64, 64))}
        self.animation = 'idle'
        self.animation_index = 0
        self.animation_speed = config.ANIMATION_SPEED
        self.attack_speed_ms = 80

        self.is_touching_player = False
        self.last_touched_player = False
        self.is_attacking = False

    def on_died(self):
        pg.mixer.Sound(
            utils.get_path(__file__, 'assets/death.mp3')).play()
        self.kill()

    def on_damaged(self):
        print(self.hp)

    def patrol(self):
        if self.touching_wall and self.is_grounded and not self.is_touching_player:
            self.jump()

        if self.dir.x == 0:
            self.dir.x = random.randint(-1, 1)
            return

      # Reverse direction if border is reached
        if self.pos.x < self.patrol_area[0]:
            self.dir.x = 1
            return
        if self.pos.x > self.patrol_area[1]:
            self.dir.x = -1
            return

    def follow(self, pos):
        if self.touching_wall and self.is_grounded and not self.is_touching_player:
            self.jump()

        if self.rect.centerx > pos[0]:
            self.dir.x = -1
        elif self.rect.centerx < pos[0]:
            self.dir.x = 1
        else:
            self.dir.x = 0

    def roam(self, change_chance=0.0005):
        if self.touching_wall and self.is_grounded and not self.is_touching_player:
            # Sometimes turn and sometimes jump over obstacles
            if random.random() < 0.5:
                self.jump()
            else:
                self.dir.x = -self.dir.x

            return

        if self.dir.x == 0:
            self.dir.x = random.randint(-1, 1)
            return

        # Reverse direction if border is reached
        if self.pos.x < self.patrol_area[0]:
            self.dir.x = 1
            return
        if self.pos.x > self.patrol_area[1]:
            self.dir.x = -1
            return

        # Make the chance equal with different fps > delta_time
        if random.random() < change_chance * game.delta_time:
            self.dir.x = -self.dir.x

    def spot_player(self, player):
        if abs(player.rect.centery - self.rect.centery) > 32:
            return

        if 0 > player.rect.centerx - self.rect.centerx > -300 and not self.facing_right:
            self.alert(player.rect.center)
        elif 0 < player.rect.centerx - self.rect.centerx < 300 and self.facing_right:
            self.alert(player.rect.center)

    def alert(self, alert_others=True):
        self.alert_timer = self.alert_timer_ms

        if not alert_others:
            return

        for enemy in self.groups()[0] or []:
            if enemy is self:
                continue

            if abs(enemy.rect.centerx - self.rect.centerx) > 800:
                continue

            enemy.alert(alert_others=False)

    def attack(self, entity):
        if self.is_attacking:
            return

        attack_rect = self.rect.copy()
        attack_rect.x += 16 if self.facing_right else -16

        if attack_rect.colliderect(entity.rect):
            if isinstance(entity, Damageable):
                entity.damage(25)

    def animate(self, player):
        last_frame_animation = self.animation
        self.animation_speed = config.ANIMATION_SPEED

        # Attacking
        if self.is_attacking:
            self.animation = 'attack'
            self.animation_speed = self.attack_speed_ms ** -1
        # Touching wall
        elif self.touching_wall or self.last_touched_player:
            # Running against wall or player
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

        if self.animation_index >= len(self.animations[self.animation]):
            if self.animation == 'attack':
                self.animation_index = 0
                if self.is_touching_player:
                    self.animation = 'push'
                else:
                    self.animation = 'idle'
                self.is_attacking = False
                self.animation_speed = config.ANIMATION_SPEED
                self.attack(player)
                self.animation_index = 0
            else:
                self.animation_index = 0

        # flip_x = !facing_right, flip image only when not facing right
        self.image = pg.transform.flip(
            self.animations[self.animation][math.floor(self.animation_index)], not self.facing_right, False)

        self.animation_index += self.animation_speed * game.delta_time

    def collide_horizontal(self, collidables):
        self.touching_wall = False
        self.is_touching_right_wall = False
        self.is_touching_player = False

        for collidable in collidables:
            if collidable.rect.colliderect(self.rect):
                if self.dir.x > 0:
                    self.rect.right = collidable.rect.left
                    self.touching_wall = 'right'
                if self.dir.x < 0:
                    self.rect.left = collidable.rect.right
                    self.touching_wall = 'left'

                if isinstance(collidable, Player):
                    self.is_touching_player = True
                self.pos.x = self.rect.x

    # def collide_vertical(self, collidables):
    #     self.is_grounded = False

    #     # Check collision 1 pixel below the actual position
    #     # This prevents collision not being detected when apply_gravity() moves less than 1 pixel every frame

    #     # Lowering the rect causes head collision to be confused with horizontal collision
    #     # Inflating the rect instead of moving it seems to work for now
    #     temp_rect = self.rect.copy()
    #     temp_rect = temp_rect.inflate(0, 1)

    #     for collidable in collidables:
    #         if isinstance(collidable, Enemy):
    #             continue
    #         if collidable.rect.colliderect(temp_rect):
    #             # Falling
    #             if self.dir.y > 0:
    #                 self.rect.bottom = collidable.rect.top
    #                 self.is_grounded = True
    #             # Jumping
    #             if self.dir.y < 0:
    #                 self.rect.top = collidable.rect.bottom

    #             self.dir.y = 0
    #             self.pos.y = self.rect.y

    def update(self, player, terrain):
        if self.alert_timer > self.alert_timer_ms / 2:
            self.speed = min(self.base_speed * 1.5, config.SPEED - 0.1)
        else:
            self.speed = self.base_speed

        self.alert_timer -= game.delta_time

        # enemies = []
        # for enemy in self.groups()[0]:
        #     if enemy is self:
        #         continue

        #     enemies.append(enemy)

        self.move([*terrain, player])
        self.animate(player)
        self.last_touched_player = self.is_touching_player
