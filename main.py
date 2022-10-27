"""
Run this file to start the program
enter option id or card number to select
enter 'endturn' to end turn and draw cards
enter 'end' to end the encounter
"""

from cards import *
from encounters import Test
from Character import Player

def main():
    deck = Deck([
        C_Recall(),
        C_Recall(),
        C_Recall(),
        C_Phone(),
        C_Inspired(),
        C_DeepBreath()
        ])
    encounter = Test(Player(), deck)
    encounter.start()

if __name__ == "__main__": main()