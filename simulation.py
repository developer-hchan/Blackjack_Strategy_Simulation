from typing import Callable
from cards import Card
from cards import simulate_deck_draw
from cards import Hand
import random
# NOTE: data_dictionary is a GLOBAL variable, the only actually
data_dictionary: dict[tuple, float] = {}
split_dictionary: dict[tuple, float] = {}


def expected_payout(player_starting_hand_total: int, player_starting_hand_texture: str, dealer_face_up: int, bet: float | Callable[[any],float], number_of_matches: int, choices: list[str], dealer_hit_soft_17: bool, output: dict[tuple,float]) -> float:
    for choice in choices:
        expected_payout_inner: float = 0.0
        for _ in range(number_of_matches):
            expected_payout_inner += run_match(
                    player_hand= generate_hand(hand_total=player_starting_hand_total, hand_texture=player_starting_hand_texture), 
                    dealer_hand= generate_dealer_hand(face_up_card= dealer_face_up), 
                    bet= bet, 
                    player_first_choice= choice,
                    dealer_hit_soft_17= dealer_hit_soft_17
                    )

        expected_payout_inner = round(expected_payout_inner/number_of_matches,2)

        output[(player_starting_hand_total, player_starting_hand_texture, dealer_face_up, choice)] = expected_payout_inner

    return None


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
    hand = Hand()
    hand.hand_list = [Card(face_up_card, random.choice(suits)), Card(simulate_deck_draw(), random.choice(suits))]
    return hand


def run_match(player_hand: Hand, dealer_hand: Hand, bet: int, player_first_choice: str, dealer_hit_soft_17: bool) -> float:
    import copy
    suits = ('heart','diamond','club','spade')
    
    # checking for blackjack in both hands
    if dealer_hand.blackjack == True and player_hand.blackjack == True:
        return 0
    elif dealer_hand.blackjack == True:
        return -bet
    elif player_hand.blackjack == True:
        return 1.5*bet

    # player turn
    counter = 0
    while player_hand.total < 21:
        choice = player_first_choice
        
        if counter > 0:
            subset = ((player_hand.total, player_hand.texture, dealer_hand.hand_list[0].number, 'hit'),
                      (player_hand.total, player_hand.texture, dealer_hand.hand_list[0].number, 'stand'))
            # if there is no existing key in data_dictionary, an error will be thrown and the except statement will be run instead
            try:
                subset_data_dictionary = {k: data_dictionary[k] for k in subset}
                choice = max(subset_data_dictionary, key=subset_data_dictionary.get)[3]
            except:
                choice = 'stand'
        
        counter += 1

        if choice == 'hit':
            player_hand.hand_list.append(Card(simulate_deck_draw(), random.choice(suits)))
            if player_hand.total > 21:
                return -bet
            else:
                continue
        
        elif choice == 'double':
            player_hand.hand_list.append(Card(simulate_deck_draw(), random.choice(suits)))
            # NOTE: check to make sure this bet line won't cause problems in the future
            bet *=2
            break

        elif choice == 'stand':
            break

        elif choice == 'surrender':
            return -0.5*bet
        
        elif choice == 'split':
            hand_A = Hand()
            hand_A.hand_list = [Card(player_hand.total/2, random.choice(suits)), Card(simulate_deck_draw(), random.choice(suits))]
            hand_B = Hand()
            hand_B.hand_list = [Card(player_hand.total/2, random.choice(suits)), Card(simulate_deck_draw(), random.choice(suits))]
            
            subset_A = ((hand_A.total, hand_A.texture, dealer_hand.hand_list[0].number, 'hit'),
                      (hand_A.total, hand_A.texture, dealer_hand.hand_list[0].number, 'stand'),
                      (hand_A.total, hand_A.texture, dealer_hand.hand_list[0].number, 'double'),
                      (hand_A.total, hand_A.texture, dealer_hand.hand_list[0].number, 'surrender'),
                      )
            
            subset_B = ((hand_B.total, hand_B.texture, dealer_hand.hand_list[0].number, 'hit'),
                      (hand_B.total, hand_B.texture, dealer_hand.hand_list[0].number, 'stand'),
                      (hand_B.total, hand_B.texture, dealer_hand.hand_list[0].number, 'double'),
                      (hand_B.total, hand_B.texture, dealer_hand.hand_list[0].number, 'surrender'),
                      )
            
            # when split is called, data_dictionary should be completed filled out... so both subsets below should be able to be filled out
            try:
                subset_A_dictionary = {k: data_dictionary[k] for k in subset_A}
                subset_B_dictionary = {k: data_dictionary[k] for k in subset_B}
            except:
                raise Exception('unknown error in split portion of run_match()')

            # if hand A is splittable, then split again; else choose the optimal option
            if hand_A.hand_list[0].number == hand_A.hand_list[1].number:
                expected_value_A = run_match(player_hand= hand_A, dealer_hand= copy.deepcopy(dealer_hand), bet= bet, player_first_choice= 'split', dealer_hit_soft_17= dealer_hit_soft_17)
            else:
                expected_value_A = run_match(player_hand= hand_A, dealer_hand= copy.deepcopy(dealer_hand), bet= bet, player_first_choice= max(subset_A_dictionary, key=subset_A_dictionary.get)[3], dealer_hit_soft_17= dealer_hit_soft_17)
            # if hand B is pslittable, then split again; else choose the optimal option
            if hand_B.hand_list[0].number == hand_B.hand_list[1].number:
                expected_value_B = run_match(player_hand= hand_B, dealer_hand= copy.deepcopy(dealer_hand), bet= bet, player_first_choice= 'split', dealer_hit_soft_17= dealer_hit_soft_17)  
            else:
                expected_value_B = run_match(player_hand= hand_B, dealer_hand= copy.deepcopy(dealer_hand), bet= bet, player_first_choice= max(subset_B_dictionary, key=subset_B_dictionary.get)[3], dealer_hit_soft_17= dealer_hit_soft_17)
            
            return expected_value_A + expected_value_B

    # dealer turn
    while dealer_hand.total < 18:
        # dealer hits on soft 17
        if dealer_hand.total == 17 and any(card for card in dealer_hand.hand_list if card.number == 11) and dealer_hit_soft_17 == True:
            dealer_hand.hand_list.append(Card(simulate_deck_draw(), random.choice(suits)))
            continue
        # dealer has hard 17 or stands on soft 17
        elif dealer_hand.total == 17:
            break
        else:
            dealer_hand.hand_list.append(Card(simulate_deck_draw(), random.choice(suits)))
    
    # evaluation
    # player busts
    if player_hand.total > 21:
        return -bet
    # dealer busts
    elif dealer_hand.total > 21:
        return bet
    # dealer and player have the same total
    elif dealer_hand.total == player_hand.total:
        return 0
    # dealer has higher than player
    elif dealer_hand.total > player_hand.total:
        return -bet
    # player has higher than dealer
    elif player_hand.total > dealer_hand.total:
        return bet
    
    

