from enum import Enum
import random


class Suit(Enum):
    Club = "Club"
    Diamond = "Diamond"
    Heart = "Heart"
    Spade = "Spade"


class Card(object):
    def __init__(self, c, s):
        self.__face_value = c
        self.__suit = s

    def value(self):
        return self.__face_value

    def suit(self):
        return self.__suit


class Deck(object):
    def __init__(self):
        self.__cards = []
        self.__dealt_index = 0
        for i in range(1, 14):
            for suit in Suit:
                print(i, suit.value)
                self.__cards.append(Card(i, suit))

    def shuffle(self):
        random.shuffle(self.__cards)

    def remaining_cards(self):
        return len(self.__cards) - self.__dealt_index

    def deal_card(self):
        if self.remaining_cards() == 0:
            return None
        tmp = self.__cards[self.__dealt_index]
        self.__dealt_index += 1
        return tmp

    def deal_hand(self, number):
        return None if self.remaining_cards() < number else [self.deal_card() for i in range(number)]



