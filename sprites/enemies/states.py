import random


from sprites.enemies.enemy import Enemy
from sprites.physics_entity import PulledByGravity
from ..physics_entity import PhysicsEntity, PulledByGravity


class EnemyState(PulledByGravity):
    def __init__(self, name, enemy: Enemy):
        self.name = name
        self._sm = enemy


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

        if self._sm.alert_timer < 0:
            return self._sm.set_state('patrolling')

        if self._sm.touching_wall:
            inf_rect = self._sm.rect.inflate(70, 64)
            if inf_rect.colliderect(self._sm.player):
                return self._sm.set_state('attacking')

            if self._sm.is_grounded:
                return self._sm.set_state('jumping')

        if self._sm.rect.x > self._sm.player.rect.x:
            self._sm.dir.x = -1
        elif self._sm.rect.x < self._sm.player.rect.x:
            self._sm.dir.x = 1
        else:
            self._sm.dir.x = 0

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
            self._sm.set_state('patrolling')
            return


class Falling(EnemyState):
    def __init__(self, *args, **kwargs):
        super().__init__('falling', *args, **kwargs)

    def enter(self):
        self._sm.animation = self._sm.animations['falling']

    def update(self):
        super().update()

        if self._sm.is_grounded:
            self._sm.set_state('patrolling')
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
            self._sm.set_state('patrolling')
            return

    def exit(self):
        self._sm.animation_speed = self.original_animation_speed
