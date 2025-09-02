import random

from blackjack.helper.cards import Hand
from blackjack.helper.cards import Card


class GameState:
    def __init__(self, **settings) -> None:
        # gamestate settings
        self.player_hands: list[Hand] = []
        self.dealer_hand: Hand = Hand()
        self.deck: list[int] = []
        self.value: float = 0
        self.skip: bool = False
        self.advance_phase: bool = False
        
        # settings.toml settings
        self.number_of_sims = None
        self.decisions = None
        self.deck_length = None
        self.shuffle = None
        self.kill_cards = None
        self.bet = None
        self.blackjack_bonus = None
        self.dealer_hit_soft_17 = None
        self.double_after_split = None

        # From the settings.toml, turning the settings into class attributes
        for key, value in settings.items():
            setattr(self, key, value)


    def create_deck(self) -> list[int]:
        if self.deck_length == 0:
            raise ValueError('deck length can not be 0')
        
        place_holder = [2,3,4,5,6,7,8,9,10,10,10,10,11]
        for _ in range(self.deck_length*4):
            self.deck += place_holder

    
    def remove_hands_from_deck(self):
        """
        because we generate random hands at the start of a game, to mimic drawing those 
        hands we remove the cards in the player and dealer's hand from the deck
        """

        to_remove = []
        remove_cards = self.player_hands[0].hand_list + self.dealer_hand.hand_list
        #getting the cards we need to remove
        for card in remove_cards:
            if card.number == 1:
                to_remove.append(11)
            else:
                to_remove.append(card.number)
            continue
        # now removing the cards from the game deck; remove() removes the first occurence
        for number in to_remove:
            self.deck.remove(number)

    
    def kill(self):
        """
        kill 'kills' or destroys a random amount of cards in the deck (up to 70% of the cards) at the start of a game
        the reasoning for this is to randomize the deck's 'starting' point for each game... in real life they don't shuffle after every hand
        that is unless you are playing with a mechanical shuffler, then turn 'kill' to 'False' in the 'config' dictionary in main.py
        """

        random_number = random.randint(0, int(len(self.deck)*0.70))
        for _ in range(random_number):
            self.deck.pop(0)
    

    def draw(self, hand: Hand):
        """
        drawing a card from the deck
        """

        suits = ('heart','diamond','club','spade')
        card_number = self.deck.pop(0)
        hand.hand_list.append(Card(card_number, random.choice(suits)))
    

    def split(self, hand: Hand):
        """
        split one hand and end with two hands
        """

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




