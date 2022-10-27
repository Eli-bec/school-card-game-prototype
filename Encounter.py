from random import randrange
from math import inf
from typing import *

from copy import copy
from cards import Deck, Card, C_BrainFog
from base import Listener

class Encounter(Listener):
    turn_limit = 6
    objectives = {} # {id,  (description, required)}
    objt_progress:dict = None # {id, progress}
    options = {} # {key, (description, requirements)}
    characters = {}

    def __init__(self, player, max_stress:int, deck:Deck, max_hand_size:int = 5):
        self.player = player
        self.characters['player'] = player
        self.max_stress = max_stress
        self.deck = deck
        self.max_hand_size = max_hand_size
        self.draw_pile = copy(deck.cards)
        self.hand = []
        self.discard_pile = []
        self.turn = 1
        self.player.card_played = 0
        # subscribe to stress changes
        self.player.on_stress_changed.append(self.on_stress_changed)
        # flags
        self.new_turn = True
        self.ended = False
        # setup dict to keep track of objective progresses
        if self.objt_progress is None: self.objt_progress = {}
        for objt in self.objectives:
            if objt not in self.objt_progress:
                self.objt_progress[objt] = False
    
    def start(self):
        """
        the actual process of the game
        """
        print(self.deck.cards)
        self.draw(5)
        self.turn = 1 # turn counter
        
        while not self.ended:
            print()
            print(f"Turn {self.turn}")
            if self.new_turn:
                self.on_turn_start(self.turn)
                self.new_turn = False
            print(f"Stress: {self.player.stress}/{self.max_stress}")
            print(f"Info: {self.player.info}")
            if self.options: print(self.options_as_str())
            print(self.hand_as_str())
            cmd = input(": ")
            # card play
            if cmd.isdigit() and 0 <= int(cmd) - 1 < len(self.hand) and self.hand[int(cmd) - 1].playable:
                card = self.hand.pop(int(cmd) - 1)
                flags = self.resolve(card.play())
                self.on_card_played(card)
                self.discard_pile.append(card)
                if 'stressfree' not in flags: self.player.stress += card.stress
            # option select
            elif cmd.lower() in map(lambda s: s.lower(), self.options):
                if cmd not in self.options:
                    for key in self.options:
                        if cmd.lower() == key.lower():
                            cmd = key
                            break
                print(f"attempt {cmd}")
                option = self.options[cmd]
                for req in option.req:
                    print(req, option.req[req], self.getstat(req))
                    if self.getstat(req) <= option.req[req]:
                        break
                # if all requirements are met
                # for-else clause: loop ended without breaking
                else:
                    self.resolve(option.select())
                    self.next_turn()
            # card draw (new turn)
            elif cmd in ("endturn", 'draw'):
                self.next_turn()
                if self.turn > self.turn_limit: self.end()
            # view objectives
            elif cmd == "objectives":
                print(self.objectives_as_str())
            # terminate the encounter
            elif cmd == "end":
                self.end()
            # discard
            elif cmd[:2] == 'd ':
                nums = cmd.split()[1:]
                new_hand = []
                for i, card in enumerate(self.hand):
                    if str(i + 1) not in nums:
                        new_hand.append(card)
                    else:
                        self.discard_pile.append(card)
                self.hand = new_hand
        self.on_encounter_end()
    
    def draw(self, num:int):
        for _ in range(num):
            # replace cards from the discard pile to the draw pile
            # if the draw pile is empty
            if not self.draw_pile and self.discard_pile:
                self.draw_pile = self.discard_pile
                self.discard_pile = []
            # draw a random card from the draw pile if there are any
            if self.draw_pile:
                card = self.draw_pile.pop(randrange(0, len(self.draw_pile)))
                self.hand.append(card)
                self.resolve(card.on_card_drawn())
    
    def end(self):
        self.ended = True
    
    def next_turn(self):
        self.draw(max(self.max_hand_size - len(self.hand), 0))
        self.turn += 1
        self.new_turn = True
        self.player.stress -= 1 # int(self.max_stress * .25)

    def resolve(self, statChanges) -> Set[str]:
        """
        resolve the return value of card plays \n
        [{'stat': str, 'op': 'add'|'sub'|'mul'|'div', 'value':num, 'min': min, 'max': max}]
        """
        flags = set()
        for change in statChanges:
            if isinstance(change, str):
                flags.add(change)
                continue
            stat = change['stat']
            if not self.hasstat(stat): continue
            if change['op'] == 'add': self.setstat(stat, self.getstat(stat)+change['value'])
            elif change['op'] == 'sub': self.setstat(stat, self.getstat(stat)-change['value'])
            elif change['op'] == 'mul': self.setstat(stat, self.getstat(stat)*change['value'])
            elif change['op'] == 'div': self.setstat(stat, self.getstat(stat)/change['value'])
            elif change['op'] == 'set': self.setstat(stat, change['value'])
            _min = change['min'] if 'min' in change else -inf
            _max = change['max'] if 'max' in change else inf
            self.setstat(stat, min(max(self.getstat(stat), _min), _max))
        return flags

    def hand_as_str(self) -> str:
        return '\n'.join(f"{i+1}. {name}" for i, name in enumerate(self.hand))
    
    def objectives_as_str(self) -> str:
        objList = []
        for obj_info in self.objectives.values():
            objList.append(('[optional]', '[required]')[obj_info[1]] + ' ' + obj_info[0])
        return '\n'.join(objList)
    
    def options_as_str(self) -> str:
        optList = []
        for key, option in self.options.items():
            optList.append(f"{key}. {option.des} {option.req}")
        return '\n'.join(optList)
    
    def stress_amount(self) -> int:
        #return (self.player.card_played + 1) // 2
        return self.player.card_played // 2 + 1
        
    def hasstat(self, stat):
        if stat.count('.') != 1: return
        objName, attrName = stat.split('.')
        return objName in self.characters and hasattr(self.characters[objName], attrName)
    
    def setstat(self, stat:str, value):
        """
        wrapper of setattr
        """
        if stat.count('.') != 1: return
        objName, attrName = stat.split('.')
        if objName not in self.characters or not hasattr(self.characters[objName], attrName): return
        setattr(self.characters[objName], attrName, value)
    
    def getstat(self, stat, default = None):
        if stat.count('.') != 1: return
        objName, attrName = stat.split('.')
        if objName not in self.characters or not hasattr(self.characters[objName], attrName): return
        return getattr(self.characters[objName], attrName, default)
    
    def on_stress_changed(self, stress):
        # add negative card 'brain fog' to draw pile when stress maxed out
        while self.player.stress >= self.max_stress:
            print("Stress reached limit, 'BrainFog' added to draw pile.")
            self.draw_pile.append(C_BrainFog())
            self.player._stress -= self.max_stress
    
    def on_encounter_start(self): raise NotImplementedError
    def on_turn_start(self, turn):
        for char in self.characters.values(): char.on_turn_start(turn)
        for cards in self.deck.cards: cards.on_turn_start(turn)
    def on_turn_end(self, turn): raise NotImplementedError
    def on_encounter_end(self): 
        for char in self.characters.values(): char.on_encounter_end()
        for cards in self.deck.cards: cards.on_encounter_end()
    def on_card_played(self, card): 
        for char in self.characters.values(): char.on_card_played(card)
        for cards in self.deck.cards: cards.on_card_played(card)
