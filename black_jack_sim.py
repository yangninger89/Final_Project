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


def game_proceed(current_player):
    next_strategy = current_player.choose_strategy()
    if next_strategy == 'D':
        current_player.double_down(deck)
    elif next_strategy == 'H':
        current_player.hitting(deck)
        game_proceed(current_player)
    elif next_strategy == 'SP':
        current_player.splitting(deck)
        for p in Player.list_of_player_instance:
            game_proceed(p)


def check_final_result():

    dealer_gain_of_current_game = 0
    dealer_points = calculate_value(Dealer.cards)
    while dealer_points < 17:
        Dealer.cards.append(draw_card(deck)[1])
        dealer_points = calculate_value(Dealer.cards)

    for p in Player.list_of_players:
        cards = Player.players[p]['cards']
        player_points = calculate_value(cards)

        if player_points > 21:
            if dealer_points <= 21:
                dealer_gain_of_current_game += Player.players[p]['bet']
        elif dealer_points > 21:
            dealer_gain_of_current_game -= pay_rate * Player.players[p]['bet']
        elif dealer_points > player_points:
            dealer_gain_of_current_game += pay_rate * Player.players[p]['bet']
        elif dealer_points < player_points:
            dealer_gain_of_current_game -= pay_rate * Player.players[p]['bet']

    Dealer.game_result.append(dealer_gain_of_current_game)


def print_result(number_of_test, black_jack_count):
    win = 0
    draw = 0
    lose = 0
    total_gain = 0

    for result in Dealer.game_result:
        total_gain += result
        if result > 0:
            win += 1
        elif result < 0:
            lose += 1
        else:
            draw += 1

    print('Win rate for the house is: ' + str(round(win / number_of_test * 100, 2)) + '%')
    print('Lose rate for the house is: ' + str(round(lose / number_of_test * 100, 2)) + '%')
    print('Draw rate for the house is: ' + str(round(draw / number_of_test * 100, 2)) + '%')
    print('Total gain of the House is: ' + str(total_gain))
    print('BlackJack appeared: ' + str(black_jack_count) + ' times.')


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
    list_of_player_instance = []
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
        Player.list_of_player_instance.append(self)

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
        # additional_bet = self.bet * 3
        additional_bet = random.sample(range(1, self.bet + 1), 1)[0]
        Player.players[self.name]['bet'] += additional_bet
        Player.players[self.name]['cards'].append(draw_card(cards_pool)[1])

    def splitting(self, cards_pool):
        i = len(Player.list_of_players)
        new_name = self.name + str(i)
        Player(new_name, self.bet, cards_pool)
        Player.players[new_name]['cards'].append(Player.players[self.name]['cards'][0])
        del Player.players[self.name]['cards'][0]
        Player.players[self.name]['cards'].append(draw_card(cards_pool)[1])


class Dealer:
    cards = []
    game_result = []

    def __init__(self, cards_pool: list):
        self.face_down = cards_pool[0]
        del cards_pool[0]
        Dealer.cards.append(self.face_down[1])


if __name__ == '__main__':
    number_of_test = 10000
    pay_rate = 1
    black_jack_count = 0

    # baseline model
    for i in range(number_of_test):
        deck = initiating_deck()
        Player.list_of_player_instance = []
        Player.list_of_players = []
        Player.players = {}
        Dealer.cards = []
        random_bet = random.sample(range(2, 500), 1)[0]
        main_player = Player('steven', random_bet, deck)
        the_house = Dealer(deck)
        Player.players[main_player.name]['cards'].append(draw_card(deck)[1])
        dealer_face_up = draw_card(deck)
        Dealer.cards.append(dealer_face_up[1])

        # check if player got blackjack
        BlackJack = [['ace', 'ten'], ['ten', 'ace'], ['ace', 'jack'], ['jack', 'ace'], ['ace', 'queen'], ['queen', 'ace'],
                     ['ace', 'king'], ['king', 'ace']]
        if Player.players[main_player.name]['cards'] in BlackJack:
                    black_jack_count += 1
                    Dealer.game_result.append(- 3/2 * pay_rate * Player.players[main_player.name]['bet'])
        # common situation when player didn't get blackjack
        else:
            game_proceed(main_player)
            check_final_result()

    print_result(number_of_test, black_jack_count)

    # new_rule
