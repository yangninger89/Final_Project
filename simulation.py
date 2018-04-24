from hand import *
from card import *


class BlackJackSimulator(object):
    def __init__(self, num_players=1):
        self.__deck = None
        self.__hands = [BlackJackHand() for i in range(num_players)]
        self.__HIT_UNTIL = 16

    def initialize_deck(self):
        self.__deck = Deck()
        self.__deck.shuffle()

    def deal_initial(self):
        for hand in self.__hands:
            cards = self.__deck.deal_hand(2)
            if cards == None:
                return False
            hand.add_cards(cards)
        return True

    def get_blackjacks(self):
        return [i for i in range(len(self.__hands)) if self.__hands[i].is_blackjack()]

    def play_hand(self, hand):
        while hand.score() < self.__HIT_UNTIL:
            card = self.__deck.deal_card()
            if card == None:
                return False
            hand.add_cards([card])
        return True

    def play_all_hands(self):
        for hand in self.__hands:
            if not self.play_hand(hand):
                return False
        return True

    def get_winners(self):
        winners = []
        winning_score = 0
        for i, hand in enumerate(self.__hands):
            if not hand.busted():
                if hand.score() > winning_score:
                    winning_score = hand.score()
                    winners = [i]
                elif hand.score() == winning_score:
                    winners.append(i)
        return winners

    def print_hand_and_score(self):
        for i, hand in enumerate(self.__hands):
            print("Hand {0} ({1})".format(i, hand.score()))

    def simulate(self):
        self.initialize_deck()

        success = self.deal_initial()
        if not success:
            print("Error: Out of Cards")
            return
        print("-- Initial --")
        self.print_hand_and_score()
        blackjacks = self.get_blackjacks()
        if len(blackjacks) > 0:
            print("Blackjack at ", blackjacks)
            print("Done.")
            return
        success = self.play_all_hands()
        if not success:
            print("Error: Out of Cards")
        else:
            print("\n-- Completed Game --")
            self.print_hand_and_score()
            winners = self.get_winners()
            if len(winners) > 0:
                print("Winners: ", winners)
            else:
                print("Draw. All players have busted.")


if __name__ == "__main__":
    simulator = BlackJackSimulator(2)
    simulator.simulate()
