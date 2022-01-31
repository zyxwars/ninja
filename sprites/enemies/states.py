import random
from sprites.physics_entity import PulledByGravity

from ..physics_entity import PulledByGravity


class EnemyState(PulledByGravity):
    def __init__(self, name, enemy):
        self.name = name
        self._sm = enemy


class Patrolling(EnemyState):
    def __init__(self, *args, **kwargs):
        super().__init__('patrolling', *args, **kwargs)

    def update(self):
        super().update()
