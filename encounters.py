from Encounter import Encounter

class Test(Encounter):
    turn_limit = 8
    objectives = {
        'q1': ("Answer question 1", False),
        'q2': ("Answer question 2", False),
        'q3': ("Answer question 3", False),
        'qHard': ("Answer the hard question", False)
    }
    options = {
        'A': ("Answer question 1", {'knowledge': 5}),
        'B': ("Answer question 2", {'knowledge': 5}),
        'C': ("Answer question 3", {'knowledge': 5}),
        'D': ("Answer the hard question", {'knowledge': 10})
    }
    
    def __init__(self, deck):
        super().__init__(0, 10, deck)

    def on_encounter_end(self):
        pass