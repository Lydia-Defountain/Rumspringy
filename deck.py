import random
from constants import REG_RANKS, REG_SUITS, ALT_RANKS, ALT_SUITS

class RummyDeck:
    def __init__(self, type="REG"):
        self.__cards = []
        self.__discard = []
        self.type = type
        self.create_deck(self.type)

    def create_deck(self, type):
        if type == "REG":
            ranks = REG_RANKS
            suits = REG_SUITS
        elif type == "ALT":
            ranks = ALT_RANKS
            suits = ALT_SUITS
        
        for suit in suits:
            for rank in ranks:
                card = (rank, suit)
                self.__cards.append(card)


    def shuffle_deck(self):
        random.shuffle(self.__cards)