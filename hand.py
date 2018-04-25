from card import *
import sys


class Hand(object):
    def __init__(self):
        self._cards = []

    def score(self):
        score = 0
        for card in self._cards:
            score += card.value()
        return score

    def add_cards(self, c):
        self._cards.extend(c)

    def __len__(self):
        return len(self._cards)


class BlackJackHand(Hand):
    def score(self):
        scores = self.__possible_scores()
        max_under = -sys.maxsize - 1
        min_over = sys.maxsize
        for score in scores:
            if score > 21 and score < min_over:
                min_over = score
            elif score <= 21 and score > max_under:
                max_under = score
        return min_over if max_under == -sys.maxsize - 1 else max_under

    def __possible_scores(self):
        scores = []
        for card in self._cards:
            self.__update_scores(card, scores)
        return scores

    def __update_scores(self, card, scores):
        to_add = self.__get_scores(card)
        if len(scores) == 0:
            scores.extend(to_add)
        else:
            length = len(scores)
            for i in range(length):
                old_score = scores[i]
                scores[i] = old_score + to_add[0]
                for j in range(1, len(to_add)):
                    scores.append(old_score + to_add[j])

    def __get_scores(self, card):
        if card.value() > 1:
            return [min(card.value(), 10)]
        else:
            return [1, 11]

    def busted(self):
        return self.score() > 21

    def is_blackjack(self):
        if len(self._cards) != 2:
            return False
        first, second = self._cards[0], self._cards[1]
        return (BlackJackHand.__is_ace(first) and BlackJackHand.__is_facecard(second)) or \
               (BlackJackHand.__is_ace(second) and BlackJackHand.__is_facecard(first))

    @staticmethod
    def __is_ace(card):
        return card.value() == 1

    @staticmethod
    def __is_facecard(card):
        return card.value() >= 11 and card.value() <= 13

