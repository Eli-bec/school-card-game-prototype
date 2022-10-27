from base import Listener

class Character(Listener):
    pass

class Player(Character):
    _stress = 0
    def set_stress(self, value:int):
        self._stress = value
        for func in self.on_stress_changed: func(value)
    def get_stress(self) -> int: return self._stress
    stress = property(get_stress, set_stress)
    on_stress_changed = []
    info = 0
    card_played = 0
    encounter = None

class Teacher(Character):
    def __init__(self):
        pass
