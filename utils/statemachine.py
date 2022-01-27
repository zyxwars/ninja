

class StateUndefined(Exception):
    def __init__(self, message, *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class State:
    def __init__(self, name):
        self.name = name

    def enter(self, sm_instance, *args, **kwargs):
        pass

    def update(self, sm_instance, *args, **kwargs):
        return None

    def exit(self, sm_instance, *args, **kwargs):
        pass


class StateMachine:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_state(self, state):
        self.states[state.name] = state

    def set_state(self, state_name, *args, **kwargs):
        if len(args) == 0:
            args = [self]

        if self.current_state:
            self.current_state.exit(*args, **kwargs)

        if not state_name in self.states:
            raise StateUndefined(state_name)

        self.current_state = self.states[state_name]
        self.current_state.enter(*args, **kwargs)

    def update_state(self, *args, **kwargs):
        if not self.current_state:
            return

        new_state_name = self.current_state.update(*args, **kwargs)
        if new_state_name:
            self.set_state(new_state_name, *args, **kwargs)
