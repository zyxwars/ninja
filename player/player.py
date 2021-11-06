import pygame as pg

from .projectile_indicator import ProjectileIndicator


class Player(pg.sprite.Sprite):
    def __init__(self, pos, size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.idle_animation = []
        self.idle_animation_index = 0
        self.idle_animation_length = 2
        self.idle_animation_speed = 0.07
        self.load_images('player_idle', self.idle_animation_length,
                         self.idle_animation, size)
        self.jump_animation = pg.transform.scale(
            pg.image.load('./player/player_jump.png'), size)
        self.fall_animation = pg.transform.scale(
            pg.image.load('./player/player_falling.png'), size)
        self.attack_animation = []
        self.attack_animation_index = 0
        self.attack_animation_length = 4
        self.attack_animation_speed = 0.3
        self.is_attacking = False
        self.load_images(
            'player_attack', self.attack_animation_length, self.attack_animation, size)
        self.image = self.idle_animation[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.dir = pg.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.is_grounded = False
        self.jumped_from_wall = False
        self.jumped_from_right_wall = False
        self.is_touching_wall = False
        self.is_touching_right_wall = False
        self.projectile_indicator = pg.sprite.GroupSingle()
        self.projectile_indicator.add(ProjectileIndicator())

    def load_images(self, image_name, number_of_images, animation_list, size):
        for i in range(number_of_images):
            image = pg.image.load(
                f'./player/{image_name}{i+1}.png').convert_alpha()
            image = pg.transform.scale(image, size)
            animation_list.append(image)

    def update(self, tiles, surface):
        self.get_input()
        self.move_horizontal(tiles)
        self.move_vertical(tiles)
        self.animate()

        self.projectile_indicator.update(self.rect.center, surface)
        self.projectile_indicator.draw(surface)

    def get_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.dir.x = -1
        elif keys[pg.K_d]:
            self.dir.x = 1
        else:
            self.dir.x = 0

        if keys[pg.K_SPACE]:
            if self.is_grounded:
                self.dir.y = self.jump_speed
                self.jumped_from_right_wall = False
                self.jumped_from_wall = False
            elif self.is_touching_wall:
                if self.is_touching_right_wall:
                    if self.jumped_from_right_wall and self.jumped_from_wall:
                        return
                    self.dir.y = self.jump_speed
                    self.jumped_from_right_wall = True
                else:
                    if not self.jumped_from_right_wall and self.jumped_from_wall:
                        return
                    self.dir.y = self.jump_speed
                    self.jumped_from_right_wall = False

                self.jumped_from_wall = True

        if pg.mouse.get_pressed()[0]:
            self.is_attacking = True

    def move_horizontal(self, tiles):
        self.rect.x += self.dir.x * self.speed
        self.is_touching_wall = False
        self.is_touching_right_wall = False

        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                if self.dir.x > 0:
                    self.rect.right = tile.rect.left
                    self.is_touching_right_wall = True
                if self.dir.x < 0:
                    self.rect.left = tile.rect.right
                self.is_touching_wall = True

    def move_vertical(self, tiles):
        self.apply_gravity()
        self.is_grounded = False

        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                if self.dir.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.dir.y = 0
                    self.is_grounded = True
                if self.dir.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.dir.y = 0

    def apply_gravity(self):
        self.dir.y += self.gravity
        self.rect.y += self.dir.y

    def animate(self):
        if self.is_attacking:
            if self.attack_animation_index >= self.attack_animation_length:
                self.attack_animation_index = 0
                self.is_attacking = False
                return
            self.image = self.attack_animation[int(
                self.attack_animation_index)]
            self.attack_animation_index += self.attack_animation_speed
        elif self.dir.y < 0 and not self.is_grounded:
            self.image = self.jump_animation
        elif self.dir.y > self.gravity * 10 and not self.is_grounded:
            self.image = self.fall_animation
        else:
            if self.idle_animation_index >= self.idle_animation_length:
                self.idle_animation_index = 0
            self.image = self.idle_animation[int(self.idle_animation_index)]
            self.idle_animation_index += self.idle_animation_speed
