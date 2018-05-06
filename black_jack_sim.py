import itertools
import random
import csv

VALUE_CHART = {'ace': 11, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
               'ten': 10, 'jack': 10, 'queen': 10, 'king': 10}
# value of ace is default to 11, and will be adjusted to 1 if needed when calculate the points.

COLOR_CHART = {'diamond': 'red', 'heart': 'red', 'spade': 'black', 'club': 'black'}

BLACK_JACK = [['ace', 'ten'], ['ten', 'ace'], ['ace', 'jack'], ['jack', 'ace'], ['ace', 'queen'], ['queen', 'ace'],
             ['ace', 'king'], ['king', 'ace']]

is_simple_strategy = False

# reads in the strategy_chart  example: {17: {2: 'S', 3: 'S', ...}, ...}
strategy_chart = {}

with open('black_jack_strategy.csv', 'r') as f:
    FIRST_ROW = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        key1 = str(row[0])
        strategies_in_row = {}
        i = 1
        for key2 in FIRST_ROW:
            strategies_in_row[key2] = str(row[i])
            i += 1
        strategy_chart[key1] = strategies_in_row


def initiating_deck() -> list:  # example: ('diamond', 'three')
    """
    This function creates a complete single deck contains 52 cards, which is to mimic dealer's shuffling action.
    :return: a list of 52 tuples, each stores information of one card, its suit and value
    """
    suits = ['heart', 'diamond', 'club', 'spade']
    face_values = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']
    complete_single_deck = list(itertools.product(suits, face_values))
    random.shuffle(complete_single_deck)

    return complete_single_deck


def calculate_value(cards_at_hand: list) -> int:
    """
    This function calculates total points of cards at hand based on the value chart provided at the top as constants.
    :param cards_at_hand: a list of values of the cards at hand

    >>> cards = ['ace', 'queen']
    >>> calculate_value(cards)
    21
    >>> cards = ['three', 'six', 'king']
    >>> calculate_value(cards)
    19
    """
    value_at_hand = 0
    for card in cards_at_hand:
        card_value = VALUE_CHART[card]
        value_at_hand += card_value
    if value_at_hand > 21:
        if 'ace' in cards_at_hand:
            value_at_hand = value_at_hand - 10

    return value_at_hand


def draw_card(cards_pool: list) -> tuple:
    """
    This function is used to mimic the action of drawing a card from the deck.
    :param cards_pool: list of tuples that mimic cards left in the deck
    :return: a tuple that represents the card being drawn
    """
    new_card = cards_pool[0]
    del cards_pool[0]

    return new_card


def calculate_points_exclude_ace(list_of_cards) -> int:
    """
    This function calculates the total points at hand excluding Ace card if there is any.
    :param list_of_cards: a list of the values of cards at hand
    :return: integer value of the total points excluding ace

    >>> cards = ['ace', 'queen', 'three']
    >>> calculate_value(cards)
    14
    """
    temp_value = 0
    for card in list_of_cards:
        if card != 'ace':
            temp_value += VALUE_CHART[card]
    return temp_value


def construct_key(list_of_cards: list) -> str:
    """
    This function construct the key to be used to search the strategy chart, in order to get
    the next strategy -- only when there's ace card at hand.
    :param list_of_cards: a list of the values of cards at hand
    :return: key as a string

    >>> cards = ['five', 'jack']
    >>> construct_key(cards)
    'A, 15'
    """
    temp_value = calculate_points_exclude_ace(list_of_cards)
    return 'A, ' + str(temp_value)


def game_start(player_name: str):
    """
    This function mimic the start of a single game where dealer shuffles teh complete deck, and then both parties
    receive first two cards.
    :param player_name: name of the main player
    :return: main player which is an instance of Player class, shuffled deck, and dealer's face up card
    """
    deck = initiating_deck()
    Player.list_of_player_instance = []
    Player.list_of_players = []
    Player.players = {}
    Dealer.cards = []
    initial_bet = random.sample(range(2, 500), 1)[0]
    main_player = Player(player_name, initial_bet, deck)
    Dealer(deck)
    Player.players[main_player.name]['cards'].append(draw_card(deck)[1])
    Player.players[main_player.name]['colors'].append(draw_card(deck)[0])
    Dealer.cards.append(draw_card(deck)[1])

    return main_player, deck


def game_proceed(current_player):
    """
    This function mimic the entire process of players checking strategy chart and take actions.
    Player (and any "players" from splitting) will be ready for dealer to reveal his cards and
    check the final result by the end of this process.
    :param current_player: the original player, which is a instance of the Player class
    :return: none
    """
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


def check_final_result(fee_option_indicator):
    """
    This function checks the final status of each party at the game table when neither of then gets black jack.
    The amount of gain/lose from the perspective the House will be recorded at the end.
    :param fee_option_indicator: is the indicator of whether the player choose to pay the normal fee, double fee or triple fee.
    :return: none
    """

    dealer_gain_of_current_game = 0
    dealer_points = calculate_value(Dealer.cards)
    while dealer_points < 17:
        Dealer.cards.append(draw_card(deck)[1])
        dealer_points = calculate_value(Dealer.cards)

    for p in Player.list_of_players:
        cards = Player.players[p]['cards']
        player_points = calculate_value(cards)

        if player_points > 21:  # Dealer wins
            # According to game rules, if player get busted, dealer automatically wins without showing hands.
            dealer_gain_of_current_game += Player.players[p]['bet']
        elif dealer_points > 21:  # Player wins
            if fee_option_indicator != 1:
                if len(set(Player.players[main_player.name]['colors'])) == 1:
                    dealer_gain_of_current_game -= fee_option_indicator * Player.players[p]['bet']
                else:
                    dealer_gain_of_current_game -= Player.players[p]['bet']
            else:
                dealer_gain_of_current_game -= Player.players[p]['bet']
        elif dealer_points > player_points:  # Dealer wins
            dealer_gain_of_current_game += Player.players[p]['bet']
        elif dealer_points < player_points:  # Player wins
            if fee_option_indicator != 1:
                if len(set(Player.players[main_player.name]['colors'])) == 1:
                    dealer_gain_of_current_game -= fee_option_indicator * Player.players[p]['bet']
                else:
                    dealer_gain_of_current_game -= Player.players[p]['bet']
            else:
                dealer_gain_of_current_game -= Player.players[p]['bet']

    Dealer.game_result.append(dealer_gain_of_current_game)


def print_result(number_of_test, player_black_jack_count, dealer_black_jack_count, dealer_gain_from_fee):
    """
    This function prints the final gain/lose rate from the perspective of the House, as well as the amount
    of black jacks appeared during the entire simulation.
    :param number_of_test: number of simulations
    :param player_black_jack_count: number of the instances where player got black jack
    :param dealer_black_jack_count: number of the instances where dealer got black jack
    :param dealer_gain_from_fee: the total amount of fees collected by the House
    :return: none
    """
    win = 0
    draw = 0
    lose = 0
    total_gain = dealer_gain_from_fee
    total_black_jack_count = player_black_jack_count + dealer_black_jack_count
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
    print('BlackJack appeared {} times: {} times at the player side and {} time at the dealer side.'
          .format(total_black_jack_count, player_black_jack_count, dealer_black_jack_count))


class Player:
    list_of_players = []  # list of players's name
    list_of_player_instance = []
    players = {}  # {name: {bet: bet, cards: [...], color: 'red'}}

    def __init__(self, name: str, bet: int, cards_pool: list):
        self.name = name
        self.bet = bet
        self.card = cards_pool[0]
        del cards_pool[0]

        Player.players[name] = {}
        Player.players[name]['cards'] = [self.card[1]]
        Player.players[name]['bet'] = self.bet
        Player.players[name]['colors'] = [COLOR_CHART[self.card[0]]]
        Player.list_of_players.append(self.name)
        Player.list_of_player_instance.append(self)

    def choose_strategy(self):
        """
        This class method mimics the process of player checking his cards at and and chooses the next strategy.
        Depending on the value of the global variable is_simple_strategy, player will choose next strategy using
        the strategy chart or using the simple strategy of "hit until 16".
        :return: The next strategy

        >>> deck = initiating_deck()
        >>> player = Player('steven', 5, deck)
        >>> Player.players['steven']['cards'] = ['ace', 'ace']
        >>> player.choose_strategy()
        'SP'

        >>> deck = initiating_deck()
        >>> player = Player('steven', 5, deck)
        >>> Player.players['steven']['cards'] = ['six', 'six']
        >>> dealer = Dealer(deck)
        >>> Dealer.cards.append('ten')
        >>> player.choose_strategy()
        'H'

        >>> deck = initiating_deck()
        >>> player = Player('steven', 5, deck)
        >>> Player.players['steven']['cards'] = ['five', 'five']
        >>> Dealer.cards[1] = 'five'
        >>> player.choose_strategy()
        'D'

        >>> deck = initiating_deck()
        >>> player = Player('steven', 5, deck)
        >>> Player.players['steven']['cards'] = ['ace', 'two', 'seven']
        >>> Dealer.cards[1] = 'five'
        >>> player.choose_strategy()
        'S'
        """
        my_cards = Player.players[self.name]['cards']
        my_points = calculate_value(my_cards)

        if not is_simple_strategy:
            if len(my_cards) == 2 and my_cards[0] == my_cards[1]:
                if 'ace' not in my_cards:
                    key = str(VALUE_CHART[my_cards[0]]) + ', ' + str(VALUE_CHART[my_cards[1]])
                    if Dealer.cards[1] == 'ace':
                        strategy = strategy_chart[key]['A']
                    else:
                        strategy = strategy_chart[key][str(VALUE_CHART[Dealer.cards[1]])]
                else:
                    strategy = 'SP'
            elif 'ace' in my_cards and calculate_points_exclude_ace(my_cards) <= 9:
                key = construct_key(my_cards)
                if Dealer.cards[1] == 'ace':
                    strategy = strategy_chart[key]['A']
                else:
                    strategy = strategy_chart[key][str(VALUE_CHART[Dealer.cards[1]])]
            else:
                if my_points >= 17:
                    strategy = 'S'
                else:
                    if Dealer.cards[1] == 'ace':
                        strategy = strategy_chart[str(my_points)]['A']
                    else:
                        strategy = strategy_chart[str(my_points)][str(VALUE_CHART[Dealer.cards[1]])]
        else:
            if my_points < 16:
                strategy = 'H'
            else:
                strategy = 'S'

        return strategy

    def hitting(self, cards_pool):
        """
        This mimic the situation where player choose to hit -- ask for another card.
        :param cards_pool: deck of cards left
        :return: none
        """
        Player.players[self.name]['cards'].append(draw_card(cards_pool)[1])
        Player.players[self.name]['colors'].append(draw_card(cards_pool)[0])

    def double_down(self, cards_pool):
        """
        This mimic the situation where player choose to add additional bet and then only get one more card.
        :param cards_pool: deck of cards left
        :return: none
        """
        additional_bet = random.sample(range(1, self.bet + 1), 1)[0]
        Player.players[self.name]['bet'] += additional_bet
        Player.players[self.name]['cards'].append(draw_card(cards_pool)[1])
        Player.players[self.name]['colors'].append(draw_card(cards_pool)[0])

    def splitting(self, cards_pool):
        """
        This mimic the situation where player choose to split the first two cards (when they are same) into two
        separate hands by placing another bet equal to his initial bet.

        :param cards_pool: deck of cards left
        :return: none
        """
        i = len(Player.list_of_players)
        new_name = self.name + str(i)
        Player(new_name, self.bet, cards_pool)
        Player.players[new_name]['cards'].append(Player.players[self.name]['cards'][0])
        Player.players[new_name]['colors'].append(Player.players[self.name]['colors'][0])
        del Player.players[self.name]['cards'][0]
        del Player.players[self.name]['colors'][0]
        Player.players[self.name]['cards'].append(draw_card(cards_pool)[1])
        Player.players[self.name]['colors'].append(draw_card(cards_pool)[0])


class Dealer:
    cards = []
    game_result = []

    def __init__(self, cards_pool: list):
        self.face_down = cards_pool[0]
        del cards_pool[0]
        Dealer.cards.append(self.face_down[1])


if __name__ == '__main__':

    normal_fee = 3
    number_of_test = 5000
    player_black_jack_count = 0
    dealer_black_jack_count = 0
    dealer_gain_from_fee = 0
    is_simple_strategy = False
    fee_option = False

    for i in range(number_of_test):
        pay_rate = 3 / 2
        if fee_option:
            fee_option_indicator = random.sample([1, 2, 3], 1)[0]
            choice_of_fee = fee_option_indicator * normal_fee
            dealer_gain_from_fee = choice_of_fee * number_of_test
            main_player, deck = game_start('steven')

        # check if player/dealer got blackjack
            if Player.players[main_player.name]['cards'] in BLACK_JACK:
                player_black_jack_count += 1
                if fee_option_indicator != 1:
                    if len(set(Player.players[main_player.name]['colors'])) == 1:
                        pay_rate = fee_option_indicator * pay_rate
                        Dealer.game_result.append(-1 * pay_rate * Player.players[main_player.name]['bet'])
                    else:
                        Dealer.game_result.append(-1 * pay_rate * Player.players[main_player.name]['bet'])
                else:
                    Dealer.game_result.append(-1 * pay_rate * Player.players[main_player.name]['bet'])
            elif Dealer.cards in BLACK_JACK:
                dealer_black_jack_count += 1
                Dealer.game_result.append(Player.players[main_player.name]['bet'])

            else:   # common situation when player didn't get blackjack
                game_proceed(main_player)
                check_final_result(fee_option_indicator)
        else:
            main_player, deck = game_start('steven')
            dealer_gain_from_fee = normal_fee * number_of_test
            fee_option_indicator = 1
            if Player.players[main_player.name]['cards'] in BLACK_JACK:
                player_black_jack_count += 1
                Dealer.game_result.append(-1 * pay_rate * Player.players[main_player.name]['bet'])
            elif Dealer.cards in BLACK_JACK:
                dealer_black_jack_count += 1
                Dealer.game_result.append(Player.players[main_player.name]['bet'])
            # common situation when player didn't get blackjack
            else:
                game_proceed(main_player)
                check_final_result(fee_option_indicator)

    print_result(number_of_test, player_black_jack_count, dealer_black_jack_count, dealer_gain_from_fee)

