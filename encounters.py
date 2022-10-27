from random import random

from Encounter import Encounter
from Character import Teacher
from Option import Option

class Test(Encounter):
    turn_limit = 8
    objectives = {
        'q1': ("Answer question 1", False),
        'q2': ("Answer question 2", False),
        'q3': ("Answer question 3", False),
        'qHard': ("Answer the hard question", False)
    }
    
    class _Teacher(Teacher):
        """Character, used to watch for phones"""
        watchful = False
        def __init__(self, encounter):
            self.encounter = encounter
            super().__init__()
        def on_turn_start(self, turn):
            self.watchful = random() >= (turn + self.watchful) / Test.turn_limit
            print(f"The teacher is{' not'*(not self.watchful)} watching")
        def on_card_played(self, card):
            if self.watchful and 'phone' in repr(card).lower():
                print("The teacher caught you using your phone!")
                # clear all answers
                for objt in self.encounter.objt_progress:
                    self.encounter.objt_progress[objt] = False
                self.encounter.end()
    
    class _Answer(Option):
        requirements = {'player.info': 5}
        def __init__(self, encounter, key:str, description, corresponding_objective:str):
            super().__init__(encounter, description=description)
            self.objective = corresponding_objective
            self.key = key # key to access the option from the encounter.options dict
        def select(self):
            self.encounter.objt_progress[self.objective] = True
            del self.encounter.options[self.key]
            return [
                {'stat': 'player.stress', 'op': 'sub', 'value': 2, 'min': 0},
                {'stat': 'player.info', 'op': 'sub', 'value': 5, 'min': 0}]
    
    class _HardAnswer(_Answer):
        requirements = {'player.info': 10}
        def select(self):
            self.encounter.objt_progress[self.objective] = True
            del self.encounter.options[self.key]
            return [
                {'stat': 'player.stress', 'op': 'sub', 'value': 4, 'min': 0},
                {'stat': 'player.info', 'op': 'sub', 'value': 10, 'min': 0}]
    
    
    def __init__(self, player, deck):
        self.characters = {'teacher': self._Teacher(self)}
        self.options = {
            'A': Test._Answer(self, 'A', "Answer question 1", 'q1'),
            'B': Test._Answer(self, 'B', "Answer question 2", 'q2'),
            'C': Test._Answer(self, 'C', "Answer question 3", 'q3'),
            'D': Test._HardAnswer(self, 'D', "Answer the hard question", 'qHard')
        }
        super().__init__(player, 8, deck)

    def on_encounter_end(self):
        super().on_encounter_end()
        print(f"Score: {sum(self.objt_progress.values())}/4 ({sum(self.objt_progress.values())/4*100:.2f}%)")
        print("This score will influence grade.")