from __future__ import annotations
from typing import *
from random import random, randint

from base import Listener

class Deck:
    def __init__(self, cards:List[Card]):
        self.cards = cards

class Card(Listener):
    name = None
    playable = True
    stress = 1
    def __repr__(self): return self.name or type(self).__name__[2:]
    def play(self) -> List[Tuple[str, str, str, int]]:
        """
        card play effects \n
        return: [{'stat': str, 'op': 'add'|'sub'|'mul'|'div', 'value':num, 'min': min, 'max': max}]
        """
        print(f"{repr(self)} played")
        return []
    def on_card_drawn(self): return []

class C_Recall(Card):
    chance = .7
    def play(self):
        super().play()
        success = random() <= C_Recall.chance
        C_Recall.chance += (1 - C_Recall.chance) / 3
        if success:
            amt = randint(4, 6)
            print(f'Gained {amt} info.')
            return [{'stat': 'player.info', 'op':'add', 'value':amt}]
        print("Failed to recall.")
        return []
    def on_turn_start(self, turn):
        C_Recall.chance = .7

class C_Phone(Card): 
    """
    can be used as stress release or info gather
    """
    def play(self):
        super().play()
        affect = input("Affect (stress/info): ")
        affect = affect.lower() if affect.lower() in ('stress', 'info') else 'stress'
        if affect == 'stress': return [
            {'stat': 'player.stress', 'op': 'sub', 'value': 5, 'min': 0},
            'stressfree']
        elif affect == 'info': return [{'stat': 'player.info', 'op': 'add', 'value': 5}]
class C_Inspired(Card): 
    """ gain 5 info """
    def play(self):
        super().play()
        return [{'stat': 'player.info', 'op': 'add', 'value': 5}]
class C_DeepBreath(Card):
    stress = 0
    def play(self):
        super().play()
        return [
            {'stat': 'player.stress', 'op': 'sub', 'value': 2, 'min': 0},
            {'stat': 'player.card_played', 'op': 'set', 'value': 0},]
class C_BrainFog(Card):
    playable = False
    def on_card_drawn(self):
        return [{'stat': 'player.info', 'op': 'sub', 'value': 3, 'min': 0}]#TODO
    def on_turn_end(self):
        pass