import unittest
from simulation import *
import random

class TestGenerateHand(unittest.TestCase):
    def test_generate_hard_hand(self):
        # a hard hand can only have a total between 4 and 20; NOTE: a hard 21 is not possible
        random_total = random.randint(4,20)
        hand = generate_hand(random_total,'hard')

        print(f"\nTEST_GENERATE_HARD_HAND: ")
        for card in hand.hand_list:
            print(card)

        self.assertEqual(random_total, hand.total)
        self.assertEqual(2, len(hand.hand_list))
    

    def test_generate_soft_hand(self):
        # a soft hand can only have a total between 12 and 21
        random_total = random.randint(12,21)
        hand = generate_hand(random_total,'soft')

        print(f"\nTEST_GENERATE_SOFT_HAND: ")
        for card in hand.hand_list:
            print(card)

        self.assertEqual(random_total,hand.total)
        self.assertEqual(2, len(hand.hand_list))


    # just checking that the code in dealer_hand_generation() could properly handle the case where the second card drawn is an ace when the face_up card is also an ace
    def test_dealer_hand_ace_generation(self):
        suits = ('heart','diamond','club','spade')
        hand = Hand()
        hand.hand_list = [Card(11, random.choice(suits)), Card(11, random.choice(suits))]

        print(f"\nTEST_DEALER_HAND_ACE_GENERATION: ")
        
        for card in hand.hand_list:
            print(card)

        self.assertEqual(12, hand.total)


class TestRunMatch(unittest.TestCase):
    def test_run_match_no_option(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(2,'heart'))
        player_hand.hand_list.append(Card(2,'diamond'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(8,'club'))
        dealer_hand.hand_list.append(Card(10,'spade'))

        run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'hit', dealer_hit_soft_17= True)

        print(f'\nTEST_RUN_MATCH_NO_OPTION... player hand: ')
        for card in player_hand.hand_list:
            print(card)

        # no matter what card is draw, a player hand total of 4 can only go to a maximum of 14.
        # because there is no 14 case in the data dictionary, the default choice is to stand
        self.assertEqual(3, len(player_hand.hand_list))


    def test_run_match_option_1(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(8,'heart'))
        player_hand.hand_list.append(Card(2,'diamond'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(8,'club'))
        dealer_hand.hand_list.append(Card(10,'spade'))

        # this seed will make it so the player will draw an 8 of spades
        random.seed(0)
        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'hit', dealer_hit_soft_17= True)

        print(f'\nTEST_RUN_MATCH_OPTION_1.. player hand: ')
        for card in player_hand.hand_list:
            print(card)

        # after drawing the 8 of spades the player will be at a total of 18, which should hit according to the data_dictionary
        # then the player will draw into a 20, which should stand according to he data_dictionary
        self.assertEqual(20, player_hand.total)
        # player should win with a 20
        self.assertEqual(25, expected_value)


    def test_run_match_option_2(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(7,'heart'))
        player_hand.hand_list.append(Card(3,'diamond'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(8,'club'))
        dealer_hand.hand_list.append(Card(10,'spade'))

        # this seed will make it so the player will draw a 5 of diamonds
        random.seed(3)
        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'hit', dealer_hit_soft_17= True)

        print(f'\nTEST_RUN_MATCH_OPTION_2.. player hand: ')
        for card in player_hand.hand_list:
            print(card)
        
        # after drawing the 5 of diamonds the player will be at a total of 15, which should hit according to the data_dictionary
        # then the player will draw into a 22 which should bust them
        self.assertEqual(22, player_hand.total)
        # player should bust with a 22
        self.assertEqual(-25, expected_value)
    

    def test_run_match_double(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(7,'heart'))
        player_hand.hand_list.append(Card(3,'diamond'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(7,'club'))
        dealer_hand.hand_list.append(Card(10,'spade'))

        # this seed will make it so the player will draw an 8 of spades
        random.seed(0)
        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'double', dealer_hit_soft_17= True)

        print(f'\nTEST_RUN_MATCH_DOUBLE.. player hand: ')
        for card in player_hand.hand_list:
            print(card)

        # although 18s should hit according to data_dictionary, double is only allowed one card
        self.assertEqual(18, player_hand.total)
        # player should win twice the bet of 25, i.e. 50
        self.assertEqual(50, expected_value)


    def test_run_match_double_lose(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(7,'heart'))
        player_hand.hand_list.append(Card(3,'diamond'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(9,'club'))
        dealer_hand.hand_list.append(Card(10,'spade'))

        # this seed will make it so the player will draw an 8 of spades
        random.seed(0)
        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'double', dealer_hit_soft_17= True)

        print(f'\nTEST_RUN_MATCH_DOUBLE_LOSE.. player hand: ')
        for card in player_hand.hand_list:
            print(card)

        # although 18s should hit according to data_dictionary, double is only allowed one card
        self.assertEqual(18, player_hand.total)
        # player should lose twice the bet of 25, i.e. 50
        self.assertEqual(-50, expected_value)


    def test_player_surrender(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(10,'heart'))
        player_hand.hand_list.append(Card(10,'diamond'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(8,'club'))
        dealer_hand.hand_list.append(Card(10,'spade'))

        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'surrender', dealer_hit_soft_17= True)

        print(f'\nTEST_PLAYER_SURRENDER.. player hand: ')
        for card in player_hand.hand_list:
            print(card)
        
        self.assertEqual(-12.50, expected_value)


    def test_dealer_hit_soft_17(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(10,'heart'))
        player_hand.hand_list.append(Card(10,'diamond'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(6,'club'))
        dealer_hand.hand_list.append(Card(11,'spade'))

        # this seed will make it so the player will draw an 8 of spades
        random.seed(0)
        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'stand', dealer_hit_soft_17= True)

        print(f'\nTEST_DEALER_HIT_SOFT_17.. player hand: ')
        for card in player_hand.hand_list:
            print(card)

        print(f'\nTEST_DEALER_HIT_SOFT_17.. dealer hand: ')
        for card in dealer_hand.hand_list:
            print(card)

        self.assertEqual(dealer_hand.total, 17)
        # should hit at soft 17 and then stand at hard 17; four cards in the dealer's hand
        self.assertEqual(len(dealer_hand.hand_list),4)
        self.assertEqual(25.00, expected_value)

    def test_tie(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(10,'heart'))
        player_hand.hand_list.append(Card(7,'diamond'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(6,'club'))
        dealer_hand.hand_list.append(Card(11,'spade'))

        # this seed will make it so the player will draw an 8 of spades
        random.seed(0)
        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'stand', dealer_hit_soft_17= True)

        print(f'\nTEST_TIE.. player hand: ')
        for card in player_hand.hand_list:
            print(card)

        print(f'\nTEST_TIE.. dealer hand: ')
        for card in dealer_hand.hand_list:
            print(card)

        self.assertEqual(dealer_hand.total, 17)
        self.assertEqual(player_hand.total, 17)
        self.assertEqual(00.00, expected_value)


    def test_player_blackjack(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(10,'heart'))
        player_hand.hand_list.append(Card(11,'diamond'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(6,'club'))
        dealer_hand.hand_list.append(Card(11,'spade'))

        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'hit', dealer_hit_soft_17= True)

        print(f'\nTEST_PLAYER_BLACKJACK.. player hand: ')
        for card in player_hand.hand_list:
            print(card)
        
        self.assertEqual(37.50, expected_value)

    
    def test_dealer_blackjack(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(10,'heart'))
        player_hand.hand_list.append(Card(10,'diamond'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(10,'club'))
        dealer_hand.hand_list.append(Card(11,'spade'))

        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'hit', dealer_hit_soft_17= True)

        print(f'\nTEST_DEALER_BLACKJACK.. dealer hand: ')
        for card in dealer_hand.hand_list:
            print(card)
        
        self.assertEqual(-25.00, expected_value)

    
    def test_both_blackjack(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(10,'heart'))
        player_hand.hand_list.append(Card(11,'diamond'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(10,'club'))
        dealer_hand.hand_list.append(Card(11,'spade'))

        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'hit', dealer_hit_soft_17= True)

        print(f'\nTEST_BOTH_BLACKJACK.. player hand: ')
        for card in player_hand.hand_list:
            print(card)

        print(f'\nTEST_BOTH_BLACKJACK.. dealer hand: ')
        for card in dealer_hand.hand_list:
            print(card)
        
        self.assertEqual(00.00, expected_value)


# assigining temporary values to global variable data_dictionary
data_dictionary[(20, 'hard', 8, 'hit')] = 10.0
data_dictionary[(20, 'hard', 8, 'double')] = 2.0
data_dictionary[(20, 'hard', 8, 'stand')] = 30.0
data_dictionary[(20, 'hard', 8, 'surrender')] = 40.0

data_dictionary[(19, 'hard', 8, 'hit')] = 20.0
data_dictionary[(19, 'hard', 8, 'double')] = 3.0
data_dictionary[(19, 'hard', 8, 'stand')] = 4.0
data_dictionary[(19, 'hard', 8, 'surrender')] = 1.0

data_dictionary[(18, 'hard', 8, 'hit')] = 30.0
data_dictionary[(18, 'hard', 8, 'double')] = 4.0
data_dictionary[(18, 'hard', 8, 'stand')] = 1.0
data_dictionary[(18, 'hard', 8, 'surrender')] = 2.0

data_dictionary[(17, 'hard', 8, 'hit')] = 30.0
data_dictionary[(17, 'hard', 8, 'double')] = 4.0
data_dictionary[(17, 'hard', 8, 'stand')] = 50.0
data_dictionary[(17, 'hard', 8, 'surrender')] = 2.0

data_dictionary[(16, 'hard', 8, 'hit')] = 40.0
data_dictionary[(16, 'hard', 8, 'double')] = 1.0
data_dictionary[(16, 'hard', 8, 'stand')] = 2.0
data_dictionary[(16, 'hard', 8, 'surrender')] = 3.0

data_dictionary[(15, 'hard', 8, 'hit')] = 10.0
data_dictionary[(15, 'hard', 8, 'double')] = 2.0
data_dictionary[(15, 'hard', 8, 'stand')] = 3.0
data_dictionary[(15, 'hard', 8, 'surrender')] = 4.0



if __name__ == "__main__":
    print(f'\nlength of data_dictionary: {len(data_dictionary)}')
    unittest.main()