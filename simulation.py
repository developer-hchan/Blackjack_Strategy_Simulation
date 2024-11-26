import random
import copy

from game_state import GameState
from cards import Hand
from cards import Card

# global dictionaries used for caching
data_dictionary: dict[tuple, float] = {}
split_dictionary: dict[tuple, float] = {}


# basically a glorified for loop on run_game(). Because run_game() returns the expected value for a given case, it is wrapped in a for loop so we can calculate the average
def expected_payout(configuration: dict, player_starting_hand_total: int, player_starting_hand_texture: str, dealer_face_up: int, output: dict) -> None:
    for choice in configuration['decisions']:

        expected_payout_inner: float = 0.0

        for _ in range(configuration['number_of_sims']):
            expected_payout_inner += run_game(
                                        configuration=configuration,
                                        hand_total=player_starting_hand_total,
                                        hand_texture=player_starting_hand_texture,
                                        dealer_face_up=dealer_face_up,
                                        choice=choice
                                        )

        expected_payout_inner = round(expected_payout_inner/configuration['number_of_sims'], 2)


        output[(player_starting_hand_total, player_starting_hand_texture, dealer_face_up, choice)] = expected_payout_inner


# same as above, but only calculating the expected payout for 'split' cases
def split_expected_payout(configuration: dict, player_starting_hand_total: int, dealer_face_up: int, output: dict) -> None:
    expected_payout_inner: float = 0.0

    for _ in range(configuration['number_of_sims']):
        expected_payout_inner += run_game(
                                    configuration=configuration,
                                    hand_total=player_starting_hand_total,
                                    hand_texture='split',
                                    dealer_face_up=dealer_face_up,
                                    choice='split'
                                    )

    expected_payout_inner = round(expected_payout_inner/configuration['number_of_sims'], 2)

    output[(player_starting_hand_total, 'split', dealer_face_up, 'split')] = expected_payout_inner


# one game of blackjack is defined as 1)checking for blackjack 2)the player's turn 3)the dealer's turn 4)evaluating all hands
# the beginning code is just set-up
# NOTE: the advance phases: split_phase, and player_turn_advance only occur if the player chooses to 'split' on their turn
def run_game(configuration: dict, hand_total: int, hand_texture: str, dealer_face_up: int, choice: str) -> float:
    game = GameState()
    game.bet = configuration['bet']
    game.blackjack_bonus = configuration['blackjack_bonus']
    game.dealer_hit_soft_17 = configuration['dealer_hit_soft_17']

    game.player_hands.append(generate_hand(hand_total=hand_total, hand_texture=hand_texture))
    game.dealer_hand = generate_dealer_hand(face_up_card=dealer_face_up)

    game.create_deck(configuration['deck_length'])
    game.remove_hands_from_deck()

    if configuration['shuffle'] == True:
        random.shuffle(game.deck)

    if configuration['kill'] == True:
        game.kill()
    
    check_4_blackjack(game)

    if game.skip != True:
        player_turn(game=game, player_first_choice=choice, dealer_face_up=dealer_face_up)

    if game.advance_phase != False:
        split_phase(game)
    
    if game.advance_phase != False:
        player_turn_advance(configuration=configuration, game=game, dealer_face_up=dealer_face_up)

    if game.skip != True:
        dealer_turn(game)
    
    if game.skip != True:
        evaluate(game)
    
    return game.value


# just check if any got blackjack. If so, award (or deduct) the appropiate amount of value and skip the rest of the phases
def check_4_blackjack(game: GameState):
    if game.dealer_hand.blackjack == True and game.player_hands[0].blackjack == True:
        game.value += 0
        game.skip = True
        return
    elif game.dealer_hand.blackjack == True:
        game.value -= game.bet
        game.skip = True
        return
    elif game.player_hands[0].blackjack == True:
        game.value += game.blackjack_bonus*game.bet
        game.skip = True
        return


def player_turn(game: GameState, player_first_choice: str, dealer_face_up: int):
    player_hand = game.player_hands[0]
    counter = 0

    while player_hand.total < 21:

        choice = player_first_choice
        # we only look for optimal decisions after the original player_first_choice was done
        if counter > 0:
            keys = (
                (player_hand.total, player_hand.texture, dealer_face_up, 'stand'),
                (player_hand.total, player_hand.texture, dealer_face_up, 'hit')
                )
            # if there is no existing key in data_dictionary, an error will be thrown and the except statement will be run instead
            try:
                subset_data_dictionary = {key: data_dictionary[key] for key in keys}
                # return the decision that has the highest expected value
                choice = max(subset_data_dictionary, key=subset_data_dictionary.get)[3]
            except:
                choice = 'stand'
        counter += 1

        if choice == 'hit':
            game.draw(player_hand)
            if player_hand.total > 21:
                return
            else:
                continue
        
        elif choice == 'double':
            game.draw(player_hand)
            player_hand.double_value = 2
            return

        elif choice == 'stand':
            return

        elif choice == 'surrender':
            game.value += -0.5*game.bet
            game.skip = True
            return
        
        # splitting aces; splitting aces is unique, each newly created ace hand is only allowed to draw one more card
        elif choice == 'split' and (player_hand.hand_list[0].number == 1 or player_hand.hand_list[0].number == 11) and (player_hand.hand_list[1].number == 1 or player_hand.hand_list[1].number == 11):
            # create a new hand
            player_hand2 = Hand()
            # pop one card from the original hand and append it to hand2
            player_hand2.hand_list.append(player_hand.hand_list.pop(1))

            # resetting the value of each ace to 11 after splitting
            player_hand.hand_list[0].number = 11
            player_hand2.hand_list[0].number = 11

            # have both hands draw a second card from the deck
            game.draw(player_hand)
            game.draw(player_hand2)

            # append the new hand to the player_hands lists in the game
            game.player_hands.append(player_hand2)
            
            return
        
        elif choice == 'split':
            # activates the advance--player turns: split_phase and player_turn_advance
            game.advance_phase = True
            return


def split_phase(game: GameState):
    # The purpose of the split phase is to split hands as many times as possible prior to player_turn_advance(), where the player plays with their split hands
    # hence we will keep trying to split every hand we have, when we fail to split any hand then split_phase ends
    while True:
        fail = 0
        for hand in game.player_hands:
            try:
                game.split(hand)
            except:
                fail += 1
                continue
        
        if fail == len(game.player_hands):
            break


# the player chooses the optimal strategies for all the hands they have after split_phase()
def player_turn_advance(configuration: dict, game: GameState, dealer_face_up: int):
    # split hands can do every available decision, except surrender
    decision_list = list(copy.deepcopy(configuration['decisions']))
    
    # removing the ability to surrender the hand, even if it has the highest expected value for a given situation
    if 'surrender' in decision_list:
        decision_list.remove('surrender')
    
    # removing the ability to double after splitting if the game rules do not allow it
    if 'double' in decision_list and configuration['double_after_split'] == False:
        decision_list.remove('double')
    
    for player_hand in game.player_hands:
        while player_hand.total < 21:
            
            # generating the keys needed to search the data_dictionary for the optimal decision for all available decisions
            keys = []
            for decision in decision_list:
                keys.append((player_hand.total, player_hand.texture, dealer_face_up, decision))
            
            # if there is no existing key in data_dictionary, an error will be thrown
            # by the time we are simulating 'split' cases, data dictionary should be filled out, so there isn't any case that can't be found
            try:
                subset_data_dictionary = {key: data_dictionary[key] for key in keys}
                # return the decision that has the highest expected value
                choice = max(subset_data_dictionary, key=subset_data_dictionary.get)[3]
            except:
                raise Exception('error when making the subset_data_dictionary in player_turn_advance')

            if choice == 'hit':
                game.draw(player_hand)
                if player_hand.total > 21:
                    break
                else:
                    continue
            
            elif choice == 'double':
                game.draw(player_hand)
                player_hand.double_value = 2
                break

            elif choice == 'stand':
                break


def dealer_turn(game: GameState):
    while game.dealer_hand.total < 18:
        # if dealer hits on soft 17
        if game.dealer_hand.total == 17 and any(card for card in game.dealer_hand.hand_list if card.number == 11) and game.dealer_hit_soft_17 == True:
            game.draw(game.dealer_hand)
            continue
        # if dealer has hard 17 or stands on soft 17
        elif game.dealer_hand.total == 17:
            break
        else:
            game.draw(game.dealer_hand)
    return


# NOTE: evaluates every hand the player has, in the case the player has multiple
def evaluate(game: GameState):
    for player_hand in game.player_hands:
        # player busts
        if player_hand.total > 21:
            game.value += -game.bet*player_hand.double_value
        # dealer busts
        elif game.dealer_hand.total > 21:
            game.value += game.bet*player_hand.double_value
        # dealer and player have the same total
        elif game.dealer_hand.total == player_hand.total:
            game.value += 0
        # dealer has higher than player
        elif game.dealer_hand.total > player_hand.total:
            game.value += -game.bet*player_hand.double_value
        # player has higher than dealer
        elif player_hand.total > game.dealer_hand.total:
            game.value += game.bet*player_hand.double_value


# only if base-Python had switch-case, *sigh*
def generate_hand(hand_total: int, hand_texture: str) -> Hand:
    suits = ('heart','diamond','club','spade')

    if hand_total < 12 and hand_texture == 'soft':
        raise ValueError("cannot create a soft hand with a value of less than 12")

    # split just make sure that both cards are the same when splitting, i.e. 5,5 for a requested hand total of 10
    elif hand_texture == 'split':
        first_card = int(hand_total/2)
        second_card = int(hand_total/2)

        hand = Hand()
        hand.hand_list = [Card(first_card, random.choice(suits)), Card(second_card, random.choice(suits))]
        return hand
    
    elif hand_texture == 'hard':
        minimum_int = hand_total - 10

        # this line is an algorithm that makes it so that any possible combination cards could be generated
        first_card = random.randint(max(1,minimum_int), min(10, hand_total-1))
        second_card = hand_total - first_card

        hand = Hand()
        hand.hand_list = [Card(first_card,random.choice(suits)), Card(second_card,random.choice(suits))]
        return hand
    
    elif hand_texture == 'soft':
        first_card = 11
        second_card = hand_total - first_card

        hand = Hand()
        hand.hand_list = [Card(first_card,random.choice(suits)), Card(second_card,random.choice(suits))]
        return hand
    
    else:
        raise Exception("Unexpected Error within generate_hand()")


def generate_dealer_hand(face_up_card: int) -> Hand:
    suits = ('heart','diamond','club','spade')
    simulated_deck = [2,3,4,5,6,7,8,9,10,10,10,10,11]
    hand = Hand()
    hand.hand_list = [Card(face_up_card, random.choice(suits)), Card(random.choice(simulated_deck), random.choice(suits))]
    return hand


