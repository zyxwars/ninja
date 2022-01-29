import pygame as pg

from .physics_entity import PhysicsEntity, PulledByGravity
import game


class Collectable(PhysicsEntity):
    def __init__(self, image, pos, *args, **kwargs):
        self.image = image
        super().__init__(self.image.get_rect(topleft=pos), *args, **kwargs)

        self.collect_cooldown_ms = 500
        self.collect_cooldown_timer = 0

        self.add_state(PulledByGravity(self))
        self.set_state('pulled_by_gravity')

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

    def update(self):
        self.current_state.update()

        self.collect_cooldown_timer -= game.delta_time
