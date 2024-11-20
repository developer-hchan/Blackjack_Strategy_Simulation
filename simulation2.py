import random

from game_state import GameState
from cards import Hand
from cards import Card

# global dictionaries used for caching
data_dictionary: dict[tuple, float] = {}
split_dictionary: dict[tuple, float] = {}


def run_match(configuration: dict, hand_total: int, hand_texture: str, dealer_face_up: int, choice: str):
    game = GameState()
    game.bet = configuration['bet']
    game.blackjack_bonus = configuration['blackjack_bonus']
    game.dealer_hit_soft_17 = configuration['dealer_hit_soft_17']

    game.player_hands.append(generate_hand(hand_total=hand_total, hand_texture=hand_texture))
    game.dealer_hand.append(generate_dealer_hand(dealer_face_up=dealer_face_up))

    game.create_deck(configuration['deck_length'])
    game.remove_hands_from_deck()

    if configuration['shuffle'] == True:
        random.shuffle(game.deck)

    if configuration['kill'] == True:
        game.kill()
    
    check_4_blackjack(game)

    if game.skip != True:
        player_turn(game=game, player_first_choice=choice)

    if game.ace_skip != False:
        # TODO
        special_ace_split_phase()

    if game.advance_skip != False:
        split_phase(game)
    
    if game.advance_skip != False:
        player_turn_advance(game)

    if game.skip != True:
        dealer_turn(game)
    
    if game.skip != True:
        evaluate(game)
    
    return game.value


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


def player_turn(game: GameState, player_first_choice: str):
    player_hand = game.player_hands[0]
    counter = 0

    while player_hand.total < 21:

        choice = player_first_choice

        if counter > 0:
            subset = (
                (player_hand.total, player_hand.texture, game.dealer_hand.hand_list[0].number, 'stand'),
                (player_hand.total, player_hand.texture, game.dealer_hand.hand_list[0].number, 'hit')
                )
            # if there is no existing key in data_dictionary, an error will be thrown and the except statement will be run instead
            try:
                subset_data_dictionary = {key: data_dictionary[key] for key in subset}
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


def special_ace_split_phase(game: GameState):
    pass


def split_phase(game: GameState):
    while True:
        for player_hand in game.player_hands:
            fail = 0
            try:
                player_hand.split
            except:
                fail += 1
        
        if fail == len(game.player_hands):
            break


def player_turn_advance(game: GameState):
    for player_hand in game.player_hands:
        
        while player_hand.total < 21:

            # TODO: update subset to adjust with config decisions
            subset = (
                (player_hand.total, player_hand.texture, game.dealer_hand.hand_list[0].number, 'stand'),
                (player_hand.total, player_hand.texture, game.dealer_hand.hand_list[0].number, 'hit'),
                (player_hand.total, player_hand.texture, game.dealer_hand.hand_list[0].number, 'double')
                )
            # if there is no existing key in data_dictionary, an error will be thrown
            # data dictionary should be filled out, so there isn't any case that can't be found
            try:
                subset_data_dictionary = {key: data_dictionary[key] for key in subset}
                choice = max(subset_data_dictionary, key=subset_data_dictionary.get)[3]
            except:
                raise Exception('error when making the subset in player_turn_advance')

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
        # dealer hits on soft 17
        if game.dealer_hand.total == 17 and any(card for card in game.dealer_hand.hand_list if card.number == 11) and game.dealer_hit_soft_17 == True:
            game.draw(game.dealer_hand)
            continue
        # dealer has hard 17 or stands on soft 17
        elif game.dealer_hand.total == 17:
            break
        else:
            game.draw(game.dealer_hand)
    return


def evaluate(game: GameState):
    for player_hand in game.player_hands:
        # player busts
        if player_hand.total > 21:
            game.value += -game.bet*player_hand.double_value
            continue
        # dealer busts
        elif game.dealer_hand.total > 21:
            game.value += game.bet*player_hand.double_value
            continue
        # dealer and player have the same total
        elif game.dealer_hand.total == player_hand.total:
            game.value += 0
            continue
        # dealer has higher than player
        elif game.dealer_hand.total > player_hand.total:
            game.value += -game.bet*player_hand.double_value
            continue
        # player has higher than dealer
        elif player_hand.total > game.dealer_hand.total:
            game.value += game.bet*player_hand.double_value
            continue


# only if base-Python had switch-case, *sigh*
def generate_hand(hand_total: int, hand_texture: str) -> Hand:
    suits = ('heart','diamond','club','spade')

    if hand_total < 12 and hand_texture == 'soft':
        raise ValueError("cannot create a soft hand with a value of less than 12")   
    
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


