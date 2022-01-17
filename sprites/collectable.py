import pygame as pg

from .physics_entity import PhysicsEntity
import game


class Collectable(PhysicsEntity):
    def __init__(self, image, pos, * args, **kwargs):
        self.image = image
        super().__init__(self.image.get_rect(topleft=pos), *args, **kwargs)

        self.collect_cooldown_ms = 500
        self.collect_cooldown_timer = 0

    def collect(self):
        if self.collect_cooldown_timer > 0:
            return

        self.kill()
        return self

    def drop(self, drop_pos):
        self.set_pos(*drop_pos)
        self.collect_cooldown_timer = self.collect_cooldown_ms
        # Use self to add collectable back to collectable group to render it
        return self

    def update(self, terrain):
        self.move(terrain)
        self.collect_cooldown_timer -= game.delta_time
