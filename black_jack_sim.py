import itertools
import random
import csv

value_chart = {'ace': 11, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
               'ten': 10, 'jack': 10, 'queen': 10, 'king': 10}    # value of ace is default to 11

# reads in the strategy_chart  {17: {2: 'S', 3: 'S'}}
first_row = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
strategy_chart = {}
with open('black_jack_strategy.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        key1 = str(row[0])
        strategies_in_row = {}
        i = 1
        for key2 in first_row:
            strategies_in_row[key2] = str(row[i])
            i += 1
        strategy_chart[key1] = strategies_in_row


def initiating_deck() -> list:  # ex: ('diamond', 'three')
    suits = ['heart', 'diamond', 'club', 'spade']
    face_values = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']
    complete_single_deck = list(itertools.product(suits, face_values))
    random.shuffle(complete_single_deck)

    return complete_single_deck


def calculate_value(cards_at_hand: list) -> int:
    value_at_hand = 0
    for card in cards_at_hand:
        card_value = value_chart[card]
        value_at_hand += card_value
    if value_at_hand > 21:
        if 'ace' in cards_at_hand:
            value_at_hand = value_at_hand - 10

    return value_at_hand


def draw_card(cards_pool: list) -> tuple:
    new_card = cards_pool[0]
    del cards_pool[0]

    return new_card


def calculate_points_exclude_ace(list_of_cards):
    temp_value = 0
    for card in list_of_cards:
        if card != 'ace':
            temp_value += value_chart[card]
    return temp_value


def construct_key(list_of_cards: list) -> str:
    temp_value = calculate_points_exclude_ace(list_of_cards)

    return 'A, ' + str(temp_value)


class Player:
    list_of_players = []  # list of players's name
    players = {}  # {name: {bet: bet, cards: [...]}}

    def __init__(self, name: str, bet: int, cards_pool: list):
        self.name = name
        self.bet = bet
        self.card = cards_pool[0]
        del cards_pool[0]

        Player.players[name] = {}
        Player.players[name]['cards'] = [self.card[1]]
        Player.players[name]['bet'] = self.bet
        Player.list_of_players.append(self.name)

    # def __str__(self):
    #     return self.name

    # def __repr__(self):
    #     return self.name

    def choose_strategy(self):

        my_cards = Player.players[self.name]['cards']
        my_points = calculate_value(my_cards)

        if len(my_cards) == 2 and my_cards[0] == my_cards[1]:
            if 'ace' not in my_cards:
                key = str(value_chart[my_cards[0]]) + ', ' + str(value_chart[my_cards[1]])
                if dealer_face_up[1] == 'ace':
                    strategy = strategy_chart[key]['A']
                else:
                    strategy = strategy_chart[key][str(value_chart[dealer_face_up[1]])]
            else:
                strategy = 'SP'

        elif 'ace' in my_cards and calculate_points_exclude_ace(my_cards) <= 9:
            key = construct_key(my_cards)
            if dealer_face_up[1] == 'ace':
                strategy = strategy_chart[key]['A']
            else:
                strategy = strategy_chart[key][str(value_chart[dealer_face_up[1]])]

        else:
            if my_points >= 17:
                strategy = 'S'
            else:
                if dealer_face_up[1] == 'ace':
                    strategy = strategy_chart[str(my_points)]['A']
                else:
                    strategy = strategy_chart[str(my_points)][str(value_chart[dealer_face_up[1]])]

        return strategy

    def hitting(self, cards_pool):
        Player.players[self.name]['cards'].append(draw_card(cards_pool)[1])

    def double_down(self, cards_pool):
        additional_bet = random.sample(range(1, self.bet + 1), 1)
        Player.players[self.name]['bet'] += additional_bet[0]
        Player.players[self.name]['cards'].append(draw_card(cards_pool)[1])

    def splitting(self, cards_pool):
        i = len(Player.list_of_players)
        new_name = self.name + str(i)
        Player(new_name, self.bet, cards_pool)
        Player.players[new_name]['cards'].append(Player.players[self.name]['card'][0])
        del Player.players[self.name]['card'][0]
        Player.players[self.name]['cards'].append(draw_card(cards_pool)[1])


class Dealer:
    cards = []
    win = 0

    def __init__(self, cards_pool: list):
        self.face_down = cards_pool[0]
        del cards_pool[0]
        Dealer.cards.append(self.face_down[1])

    def __str__(self):
        return 'The House'

    def check_final_result(self):
        dealer_points = calculate_value(Dealer.cards)

        while dealer_points < 17:
            Dealer.cards.append(draw_card(deck)[1])
            dealer_points = calculate_value(Dealer.cards)

        for p in Player.list_of_players:
            cards = Player.players[p]['cards']
            player_points = calculate_value(cards)
            if dealer_points > player_points or player_points > 21:
                Dealer.win += Player.players[p]['bet']
            if dealer_points < player_points:
                Dealer.win -= 3/2 * Player.players[p]['bet']


if __name__ == '__main__':
    player_win_count = 0
    player_gain = 0

    for i in range(100):
        deck = initiating_deck()
        main_player = Player('steven', 5, deck)
        the_house = Dealer(deck)
        player_card = draw_card(deck)
        Player.players[main_player.name]['cards'].append(player_card[1])
        dealer_face_up = draw_card(deck)
        Dealer.cards.append(dealer_face_up[1])

    def game_proceed(current_player):
        my_cards = Player.players[current_player.name]['cards']
        my_points = calculate_value(my_cards)

        if my_points > 21:
            game_result = False
            Player.win -= 3/2 * Player.players[current_player.name]['bet']
        elif my_points == 21:
            Dealer.check_final_result(the_house)
        else:
            next_strategy = current_player.choose_strategy()
            if next_strategy == 'S':
                Dealer.check_final_result(the_house)
            elif next_strategy == 'D':
                current_player.double_down(deck)
                Dealer.check_final_result(the_house)
            elif next_strategy == 'H':
                current_player.hitting(deck)
                game_proceed(current_player)
            else:
                current_player.splitting(deck)
                for p in Player.list_of_players:
                    game_proceed(p)

        # game_proceed(main_player)

    # print(Player.win)

