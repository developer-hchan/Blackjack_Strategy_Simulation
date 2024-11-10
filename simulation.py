from typing import Callable
from cards import Card
from cards import Hand
import random


def expected_payout(player_starting_hand_total: int, player_starting_hand_texture: str, dealer_face_up: int, bet: float | Callable[[any],float], number_of_matches: int) -> float:
    expected_payout_inner: float = 0.0

    run_match(player_hand= generate_hand(hand_total=player_starting_hand_total, hand_texture=player_starting_hand_texture), 
              dealer_face_up= dealer_face_up, 
              bet= bet)


    return


# only if base-Python had switch-case, *sigh*
def generate_hand(hand_total: int, hand_texture: str) -> Hand:
    suits = ('heart','diamond','club','spade')

    if hand_total < 12 and hand_texture == 'soft':
        raise ValueError("cannot create a soft hand with a value of less than 12")
    
    elif hand_texture == 'hard':
        minimum_int = hand_total - 10

        first_card = random.randint(max(1,minimum_int), hand_total-1)
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


def run_match(player_hand: Hand, dealer_face_up: int) -> float:
    pass


