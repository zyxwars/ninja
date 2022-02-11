import random

import game
from sprites.enemies.enemy import Enemy
from sprites.physics_entity import PulledByGravity
from ..physics_entity import PhysicsEntity, PulledByGravity


class EnemyState(PulledByGravity):
    def __init__(self, name, enemy: Enemy):
        self.name = name
        self._sm = enemy

    def set_patrol_or_chase(self):
        if self._sm.alert_timer > 0:
            return self._sm.set_state('chasing')

        return self._sm.set_state('patrolling')


class Patrolling(EnemyState):
    def __init__(self, *args, **kwargs):
        super().__init__('patrolling', *args, **kwargs)

    def enter(self):
        self._sm.animation = self._sm.animations['walking']

    def update(self):
        super().update()

        if self._sm.alert_timer > 0:
            return self._sm.set_state('chasing')

        if self._sm.touching_wall and self._sm.is_grounded:
            return self._sm.set_state('jumping')

        if self._sm.dir.x == 0:
            self._sm.dir.x = 1

        if self._sm.rect.x > self._sm.patrol_area[1]:
            self._sm.dir.x = -1
        elif self._sm.rect.x < self._sm.patrol_area[0]:
            self._sm.dir.x = 1


class Idling(EnemyState):
    def __init__(self, *args, **kwargs):
        super().__init__('idling', *args, **kwargs)

    def enter(self):
        self._sm.dir.x = 0
        self._sm.animation = self._sm.animations['idling']

    def update(self):
        # Enemy got alerted again
        if self._sm.alert_timer > self._sm.last_alert_timer:
            return self._sm.set_state('chasing')

        if self._sm.alert_timer < 0:
            self._sm.set_state('patrolling')


class Searching(EnemyState):
    def __init__(self, *args, **kwargs):
        super().__init__('searching', *args, **kwargs)
        self.original_speed = 0

    def enter(self):
        self._sm.animation = self._sm.animations['running']
        self._sm.dir.x = self._sm.last_dir.x
        self.original_speed = self._sm.speed
        self._sm.speed *= 2

    def update(self):
        super().update()

        if self._sm.alert_timer > self._sm.last_alert_timer:
            return self._sm.set_state('chasing')

        if self._sm.alert_timer < 1000:
            return self._sm.set_state('idling')

        self._sm.alert_timer -= game.delta_time * 5

    def exit(self):
        self._sm.speed = self.original_speed


class Chasing(EnemyState):
    def __init__(self, *args, **kwargs):
        super().__init__("chasing", *args, **kwargs)
        self.original_speed = 0

    def enter(self):
        self.original_speed = self._sm.speed
        self._sm.speed *= 2
        self._sm.animation = self._sm.animations['running']

    def update(self):
        super().update()

        if self._sm.alert_timer < 1000:
            return self._sm.set_state('idling')

        if self._sm.touching_wall:
            attack_rect = self._sm.rect.inflate(64, 0)
            if attack_rect.colliderect(self._sm.player):
                return self._sm.set_state('attacking')

            if self._sm.is_grounded:
                return self._sm.set_state('jumping')

        if self._sm.rect.x > self._sm.player_spotted_pos[0]:
            self._sm.dir.x = -1
        elif self._sm.rect.x < self._sm.player_spotted_pos[0]:
            self._sm.dir.x = 1
        else:
            self._sm.last_dir = self._sm.dir
            return self._sm.set_state('searching')

    def exit(self):
        self._sm.speed = self.original_speed


class Jumping(EnemyState):
    def __init__(self, *args, **kwargs):
        super().__init__('jumping', *args, **kwargs)

    def enter(self):
        PhysicsEntity.jump(self._sm)
        self._sm.animation = self._sm.animations['jumping']

    def update(self):
        super().update()

        if self._sm.dir.y > 0.5:
            self._sm.set_state('falling')
            return
        if self._sm.is_grounded:
            self.set_patrol_or_chase()
            return


class Falling(EnemyState):
    def __init__(self, *args, **kwargs):
        super().__init__('falling', *args, **kwargs)

    def enter(self):
        self._sm.animation = self._sm.animations['falling']

    def update(self):
        super().update()

        if self._sm.is_grounded:
            self.set_patrol_or_chase()
            return

    def exit(self):
        self._sm.dir.x = 0


class Attacking(EnemyState):
    def __init__(self, *args, **kwargs):
        super().__init__('attacking', *args, **kwargs)
        self.original_animation_speed = 0

    def enter(self):
        self._sm.animation = self._sm.animations['attacking']
        self.original_animation_speed = self._sm.animation_speed
        self._sm.animation_speed = self._sm.animation_speed = (
            self._sm.attack_length / len(self._sm.animations['attacking'])) ** -1

    def update(self):
        super().update()

        if self._sm.animation_index >= len(self._sm.animation):
            self.set_patrol_or_chase()
            return

    def exit(self):
        attack_rect = self._sm.rect.inflate(32, 0)
        if attack_rect.colliderect(self._sm.player):
            self._sm.player.damage(self._sm.damage_amount)

        self._sm.animation_speed = self.original_animation_speed
