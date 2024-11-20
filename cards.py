
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
    # This line is to make aces more clear to the player when playing game (which value the ace currently is)
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
        


# Adding hand totals, NOTE the special adding cases for aces
def add(hand: list[Card]) -> int:
    emergency_break = 0
    
    # NOTE: this list comprehension creates a shallow copy of the filtered Card objects, so any adjustments made to the shallow copy changes the original object reference 
    soft_cards = [card for card in hand if card.number == 11]

    while True:
        emergency_break += 1
        if emergency_break == 100:
            raise Exception("Detected infinite while loop within add() fucntion, terminating process...")
        
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


    
