from hand import *
from card import *


class BlackJackSimulator(object):
    def __init__(self, num_players=1):
        self.__deck = None
        self.__hands = [BlackJackHand() for i in range(num_players)]
        self.__dealer_hand = BlackJackHand()
        self.__HIT_UNTIL = 16
        self.__DEALER_HIT_UNTIL = 17

    def initialize_deck(self):
        self.__deck = Deck()
        self.__deck.shuffle()

    def deal_initial(self):
        for hand in self.__hands:
            cards = self.__deck.deal_hand(2)
            if cards == None:
                return False
            hand.add_cards(cards)
        cards = self.__deck.deal_hand(2)
        if cards == None:
            return False
        self.__dealer_hand.add_cards(cards)
        return True

    def get_blackjacks(self):
        player = [i for i in range(len(self.__hands)) if self.__hands[i].is_blackjack()]
        dealer = ["dealer"] if self.__dealer_hand.is_blackjack() else []
        return player + dealer

    def play_hand(self, hand):
        while hand.score() < self.__HIT_UNTIL:
            card = self.__deck.deal_card()
            if card == None:
                return False
            hand.add_cards([card])
        return True

    def dealer_play_hand(self):
        while self.__dealer_hand.score() < self.__DEALER_HIT_UNTIL:
            card = self.__deck.deal_card()
            if card == None:
                return False
            self.__dealer_hand.add_cards([card])
        return True

    def play_all_hands(self):
        for hand in self.__hands:
            if not self.play_hand(hand):
                return False
        return True and self.dealer_play_hand()

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
        if not self.__dealer_hand.busted():
            if self.__dealer_hand.score() > winning_score:
                winning_score = self.__dealer_hand.score()
                winners = ["dealer"]
            elif self.__dealer_hand.score() == winning_score:
                winners.append("dealer")
        return winners

    def print_hand_and_score(self):
        for i, hand in enumerate(self.__hands):
            print("Hand {0} ({1})".format(i, hand.score()))
        print("Dealer hand ({0})".format(self.__dealer_hand.score()))

    def simulate(self):
        self.initialize_deck()

        success = self.deal_initial()
        if not success:
            print("Error: Out of Cards")
            return "out of cards"
        print("-- Initial --")
        self.print_hand_and_score()
        blackjacks = self.get_blackjacks()
        if len(blackjacks) > 0:
            print("Blackjack at ", blackjacks)
            print("Done.")
            return "draw" if len(blackjacks) >= 2 else ("loss" if "dealer" in blackjacks else "win")
        success = self.play_all_hands()
        if not success:
            print("Error: Out of Cards")
            return "out of cards"
        else:
            print("\n-- Completed Game --")
            self.print_hand_and_score()
            winners = self.get_winners()
            if len(winners) > 0:
                print("Winners: ", winners)
                if len(winners) >= 2 and ("dealer" in winners):
                    return "draw"
                elif len(winners) == 1 and ("dealer" in winners):
                    return "loss"
                else:
                    return "win"
            else:
                print("Draw. All players have busted.")
                return "draw"


if __name__ == "__main__":
    win = 0
    draw = 0
    loss = 0
    out_of_card = 0
    n = 10000
    for k in range(n):
        simulator = BlackJackSimulator()
        result = simulator.simulate()
        if result == "win":
            win += 1
        elif result == "draw":
            draw += 1
        elif result == "loss":
            loss += 1
        else:
            out_of_card += 1
    print("probability of win: {:.1f}%".format(win * 100.0 / n))
    print("probability of draw: {:.1f}%".format(draw * 100.0 / n))
    print("probability of loss: {:.1f}%".format(loss * 100.0 / n))
    print("probability of out of card: {:.1f}%".format(out_of_card * 100.0 / n))

