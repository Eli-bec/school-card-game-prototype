from cards import *
from encounters import Test

def main():
    deck = Deck([
        C_Recall(),
        C_Recall(),
        C_Recall(),
        C_Phone(),
        C_Inspired(),
        C_DeepBreath()
        ])
    encounter = Test(deck)
    encounter.start()

if __name__ == "__main__": main()