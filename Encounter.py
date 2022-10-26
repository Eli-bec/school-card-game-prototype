from copy import copy
from random import randrange
from cards import Deck

class Encounter:
    turn_limit = 6
    objectives = {} # {id,  (description, required)}
    options = {} # {key, (description, requirements)}

    def __init__(self, stress:int, max_stress:int, deck:Deck, max_hand_size:int = 5):
        self.stress, self.max_stress = stress, max_stress
        self.deck = deck
        self.max_hand_size = max_hand_size
        self.draw_pile = copy(deck.cards)
        self.hand = []
        self.discard_pile = []
        self.turn = 1
        self.card_played = 0
    
    def start(self):
        """
        the actual process of the game
        """
        print(self.deck.cards)
        self.draw(5)
        self.turn = 1 # turn counter
        
        while True:
            print()
            print(f"Turn {self.turn}")
            print(f"Stress: {self.stress}/{self.max_stress}")
            if self.options:
                print(self.options_as_str())
            print(self.hand_as_str())
            cmd = input(": ")
            if cmd.isdigit() and 0 <= int(cmd) - 1 < len(self.hand):
                card = self.hand.pop(int(cmd) - 1)
                card.play()
                self.discard_pile.append(card)
                print(self.stress_amount())
                self.stress += self.stress_amount()
                self.card_played += 1
            elif cmd == "draw":
                self.draw(self.max_hand_size - len(self.hand))
                self.turn += 1
                self.card_played = 0
                if self.turn == self.turn_limit: self.end()
            elif cmd == "objectives":
                print(self.objectives_as_str())
            elif cmd == "end":
                self.end()
    
    def draw(self, num:int):
        for _ in range(num):
            # replace cards from the discard pile to the draw pile
            # if the draw pile is empty
            if not self.draw_pile and self.discard_pile:
                self.draw_pile = self.discard_pile
                self.discard_pile = []
            # draw a random card from the draw pile if there are any
            if self.draw_pile:
                self.hand.append(self.draw_pile.pop(randrange(0, len(self.draw_pile))))
    
    def end(self):
        pass

    def hand_as_str(self) -> str:
        return '\n'.join(f"{i+1}. {name}" for i, name in enumerate(self.hand))
    
    def objectives_as_str(self) -> str:
        objList = []
        for obj_info in self.objectives.values():
            objList.append(('[optional]', '[required]')[obj_info[1]] + ' ' + obj_info[0])
        return '\n'.join(objList)
    
    def options_as_str(self) -> str:
        optList = []
        for key, opt_info in self.options.items():
            optList.append(f"{key}. {opt_info[0]} {opt_info[1]}")
        return '\n'.join(optList)
    
    def stress_amount(self) -> int:
        return (self.card_played + 1) // 2
    
    def on_encounter_start(self): pass
    def on_turn_start(self, turn): pass
    def on_turn_end(self, turn): pass
    def on_encounter_end(self): pass