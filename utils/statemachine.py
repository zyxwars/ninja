
from typing import Optional


class StateUndefined(Exception):
    def __init__(self, message, *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class State:
    def __init__(self, name: str, sm: 'StateMachine'):
        self.name = name
        self._sm = sm

    def enter(self):
        pass

    def update(self):
        pass

    def exit(self):
        pass


class StateMachine:
    def __init__(self):
        self.states: dict[str, State] = {}
        self.current_state: Optional[State] = None

    def add_state(self, state):
        self.states[state.name] = state

    def set_state(self, state_name):
        if self.current_state:
            self.current_state.exit()

        if not state_name in self.states:
            raise StateUndefined(state_name)

        self.current_state = self.states[state_name]

        self.current_state.enter()
