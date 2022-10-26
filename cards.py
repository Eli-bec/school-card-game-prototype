from __future__ import annotations
from typing import *

class Deck:
    def __init__(self, cards:List[Card]):
        self.cards = cards

class Card:
    name = None
    def __repr__(self): return self.name or type(self).__name__[2:]
    def play(self):
        print(f"{repr(self)} played")

class C_Recall(Card): pass
class C_Phone(Card): pass
class C_Inspired(Card): pass
class C_DeepBreath(Card): pass
class C_Notebook(Card): pass