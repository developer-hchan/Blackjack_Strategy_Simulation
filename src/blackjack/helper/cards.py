import random

class Card:
    def __init__(self, number: int, suit: str) -> None:
        if number < 1:
            raise ValueError("A card with an int value below one tried to be created")
        elif number > 11:
            raise ValueError("A card with and int value above 11 tried to be created")
        else:
            self.number: int = number
        
        if suit.lower() not in ['heart','diamond','club','spade']:
            raise ValueError("suit value for the entered card is invalid")
        else:
            self.suit: str = suit

    
    def __str__(self):
    # aces can have a value of either 1 or 11
        if self.number == 1 or self.number == 11:
            return f"Ace of {self.suit}s"
        else:
            return f"{self.number} of {self.suit}s"

        
class Hand:
    def __init__(self) -> None:
        self.hand_list: list[Card] = []
    
    @property
    def total(self):
        return add(self.hand_list)

    @property
    def texture(self) -> str:
        self.total
        if any(card.number == 11 for card in self.hand_list):
            return 'soft'
        else:
            return 'hard'
    
    @property
    def blackjack(self):
        if self.total == 21 and len(self.hand_list) == 2:
            return True
        else:
            return False
    
    double_value: int = 1
        


def add(hand: list[Card]) -> int:
    """
    Adding hand totals, NOTE the special adding cases for aces
    """

    # NOTE: this list comprehension creates a shallow copy of the filtered Card objects, so any adjustments made to the shallow copy changes the original object reference 
    soft_cards = [card for card in hand if card.number == 11]

    while True:
        total = 0
        for card in hand:
            total += card.number

        if total > 21 and len(soft_cards) != 0:
            for idx, card in enumerate(soft_cards):
                card.number = 1
                soft_cards.pop(idx)
                break
            continue
        else:
            return total
    

# NOTE: *sigh* python 3.10 added match-case, but is it worth the rebase?
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
