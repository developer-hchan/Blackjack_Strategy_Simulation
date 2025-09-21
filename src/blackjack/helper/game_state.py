import random
import copy

from blackjack.helper.cards import Hand
from blackjack.helper.cards import Card
from blackjack.helper.cards import generate_hand
from blackjack.helper.cards import generate_dealer_hand
from blackjack import global_data_dictionary


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
    

    def run_game(self, sim_case: tuple) -> float:
        """
        one game of blackjack is defined as 
            1. checking for blackjack
            2. the player's turn 3)the dealer's turn 4)evaluating all hands
            3. the beginning code is just set-up
    
        NOTE: the advance phases: split_phase, and player_turn_advance only occur if the player chooses to 'split' on their turn
        """

        #TODO: change most of these from game to self
        self.player_hands.append(generate_hand(hand_total=sim_case[0], hand_texture=sim_case[1]))
        self.dealer_hand = generate_dealer_hand(face_up_card=sim_case[2])

        self.create_deck()
        self.remove_hands_from_deck()

        if self.shuffle is True:
            random.shuffle(self.deck)

        if self.kill_cards is True:
            self.kill()
    
        self.check_4_blackjack()

        if self.skip is not True:
            self.player_turn(player_first_choice=sim_case[3], dealer_face_up=sim_case[2])

        if self.advance_phase is not False:
            self.split_phase()
    
        if self.advance_phase is not False:
            self.player_turn_advance(dealer_face_up=sim_case[2])

        if self.skip is not True:
            self.dealer_turn()
    
        if self.skip is not True:
            self.evaluate()
        
        # resetting the game object; everything except game.value
        self.reset_game()
    
        return
    

    # TODO: implement: resets everything except game.value for game object
    def reset_game(self):
        self.player_hands: list[Hand] = []
        self.dealer_hand: Hand = Hand()
        self.deck: list[int] = []
        self.skip: bool = False
        self.advance_phase: bool = False


    def check_4_blackjack(self):
        """
        check if any hand got blackjack. If so, award (or deduct) the appropiate amount 
        of value and skip the rest of the phases
        """

        if self.dealer_hand.blackjack is True and self.player_hands[0].blackjack is True:
            self.value += 0
            self.skip = True
            return
        elif self.dealer_hand.blackjack is True:
            self.value -= self.bet
            self.skip = True
            return
        elif self.player_hands[0].blackjack is True:
            self.value += self.blackjack_bonus*self.bet
            self.skip = True
            return


    def player_turn(self, player_first_choice: str, dealer_face_up: int):
        player_hand = self.player_hands[0]
        counter = 0

        while player_hand.total < 21:

            choice = player_first_choice
            # we only look for optimal decisions after the original player_first_choice was done
            if counter > 0:
                keys = (
                    (player_hand.total, player_hand.texture, dealer_face_up, "stand"),
                    (player_hand.total, player_hand.texture, dealer_face_up, "hit")
                )
                # checking to see if the keys are in the global dictionary, if not then "stand"
                if (keys[0] not in global_data_dictionary) and (keys[1] not in global_data_dictionary):
                    choice = "stand"
                else:
                    subset_data_dictionary = {key: global_data_dictionary[key] for key in keys}
                    # return the decision that has the highest expected value
                    choice = max(subset_data_dictionary, key=subset_data_dictionary.get)[3]
            
            counter += 1

            if choice == "hit":
                self.draw(player_hand)
                if player_hand.total > 21:
                    return
                else:
                    continue
        
            elif choice == "double":
                self.draw(player_hand)
                player_hand.double_value = 2
                return

            elif choice == "stand":
                return

            elif choice == "surrender":
                self.value += -0.5*self.bet
                self.skip = True
                return
        
            # splitting aces; splitting aces is unique, each newly created ace hand is only allowed to draw one more card
            elif choice == "split" and (player_hand.hand_list[0].number == 1 or player_hand.hand_list[0].number == 11) and (player_hand.hand_list[1].number == 1 or player_hand.hand_list[1].number == 11):
                # create a new hand
                player_hand2 = Hand()
                # pop one card from the original hand and append it to hand2
                player_hand2.hand_list.append(player_hand.hand_list.pop(1))

                # resetting the value of each ace to 11 after splitting
                player_hand.hand_list[0].number = 11
                player_hand2.hand_list[0].number = 11

                # have both hands draw a second card from the deck
                self.draw(player_hand)
                self.draw(player_hand2)

                # append the new hand to the player_hands lists in the game
                self.player_hands.append(player_hand2)
            
                return
        
            elif choice == "split":
                # activates the advance--player turns: split_phase and player_turn_advance
                self.advance_phase = True
                return


    def split_phase(self):
        """
        The purpose of the split phase is to split hands as many times as possible prior to player_turn_advance(), where the player plays with their split hands
        hence we will keep trying to split every hand we have, when we fail to split any hand then split_phase ends
        """

        while True:
            fail = 0
            for hand in self.player_hands:
                try:
                    self.split(hand)
                except:
                    fail += 1
                    continue
        
            if fail == len(self.player_hands):
                break


    def player_turn_advance(self, dealer_face_up: int):
        """
        the player chooses the optimal strategies for all the hands they have after split_phase()
        """

        # split hands can do every available decision, except surrender
        decision_list = list(copy.deepcopy(self.decisions))
    
        # removing the ability to surrender the hand, even if it has the highest expected value for a given situation
        if "surrender" in decision_list:
            decision_list.remove("surrender")
    
        # removing the ability to double after splitting if the game rules do not allow it
        if "double" in decision_list and self.double_after_split is False:
            decision_list.remove("double")
    
        for player_hand in self.player_hands:
            while player_hand.total < 21:
            
                # generating the keys needed to search the global_data_dictionary for the optimal decision for all available decisions
                keys = []
                for decision in decision_list:
                    keys.append((player_hand.total, player_hand.texture, dealer_face_up, decision))
            
                # if there is no existing key in global_data_dictionary, an error will be thrown
                # by the time we are simulating 'split' cases, data dictionary should be filled out, so there isn't any case that can't be found
                try:
                    subset_data_dictionary = {key: global_data_dictionary[key] for key in keys}
                    # return the decision that has the highest expected value
                    choice = max(subset_data_dictionary, key=subset_data_dictionary.get)[3]
                except Exception as e:
                    print(f'unexpected {type(e)} when making the subset_data_dictionary in player_turn_advance')

                if choice == "hit":
                    self.draw(player_hand)
                    if player_hand.total > 21:
                        break
                    else:
                        continue
            
                elif choice == "double":
                    self.draw(player_hand)
                    player_hand.double_value = 2
                    break

                elif choice == "stand":
                    break


    def dealer_turn(self):
        while self.dealer_hand.total < 18:
            # if dealer hits on soft 17
            if self.dealer_hand.total == 17 and any(card for card in self.dealer_hand.hand_list if card.number == 11) and self.dealer_hit_soft_17 is True:
                self.draw(self.dealer_hand)
                continue
            # if dealer has hard 17 or stands on soft 17
            elif self.dealer_hand.total == 17:
                break
            else:
                self.draw(self.dealer_hand)
        return


    def evaluate(self):
        """
        evaluates every hand the player has, in the case the player has multiple
        """

        for player_hand in self.player_hands:
            # player busts
            if player_hand.total > 21:
                self.value += -self.bet*player_hand.double_value
            # dealer busts
            elif self.dealer_hand.total > 21:
                self.value += self.bet*player_hand.double_value
            # dealer and player have the same total
            elif self.dealer_hand.total == player_hand.total:
                self.value += 0
            # dealer has higher than player
            elif self.dealer_hand.total > player_hand.total:
                self.value += -self.bet*player_hand.double_value
            # player has higher than dealer
            elif player_hand.total > self.dealer_hand.total:
                self.value += self.bet*player_hand.double_value


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




