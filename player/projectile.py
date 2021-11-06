import pygame as pg


class Projectile(pg.sprite.Sprite):
    def __init__(self, player_pos, mouse_pos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pg.image.load('./player/shuriken.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect(topleft=player_pos)
        self.dir = (pg.math.Vector2(
            mouse_pos) - pg.math.Vector2(player_pos)).normalize()
        self.speed = 16

    def update(self):
        self.rect.x += self.dir.x * self.speed
        self.rect.y += self.dir.y * self.speed
