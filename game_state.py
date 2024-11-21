import copy
import random

from cards import Hand
from cards import Card

class GameState():
    def __init__(self) -> None:
        self.player_hands: list[Hand] = []
        self.dealer_hand: Hand = None
        self.deck: list[int] = []
        self.value: float = 0
        self.skip: bool = False
        self.advance_phase: bool = False
        self.bet: float = 25.00
        self.blackjack_bonus: float = 1.5
        self.dealer_hit_soft_17: bool = True
    

    def create_deck(self, deck_length: int) -> list[int]:
        if deck_length == 0:
            raise Exception('deck length can not be 0')
        
        place_holder = [2,3,4,5,6,7,8,9,10,10,10,10,11]
        for _ in range(deck_length*4):
            self.deck += copy.deepcopy(place_holder)


    def remove_hands_from_deck(self):
        remove_cards = self.player_hands[0].hand_list + self.dealer_hand.hand_list
        for card in remove_cards:
            if card.number == 1:
                self.deck.remove(11)
            else:
                self.deck.remove(card.number)
            continue

    
    def kill(self):
        random_number = random.randint(0, int(len(self.deck)*0.70))
        for _ in range(random_number):
            self.deck.pop(0)
    

    def draw(self, hand: Hand):
        suits = ('heart','diamond','club','spade')
        card_number = self.deck.pop(0)
        hand.hand_list.append(Card(card_number, random.choice(suits)))
    

    # split one hand and end with two hands
    def split(self, hand: Hand):
        if len(hand.hand_list) > 2:
            raise Exception('hand has more than 2 cards, cannot split')
        elif len(hand.hand_list) < 2:
            raise Exception('hand has less than 2 cards, cannot split')
        elif hand.hand_list[0].number != hand.hand_list[1].number:
            raise Exception('hand has different cards, cannot split')
        else:
            # create a new hand
            hand2 = Hand()
            # pop one card from the original hand and append it to hand2
            hand2.hand_list.append(hand.hand_list.pop(1))

            # have both hands draw a second card from the deck
            self.draw(hand)
            self.draw(hand2)

            # append the new hand to the player_hands lists in the game
            self.player_hands.append(hand2)




