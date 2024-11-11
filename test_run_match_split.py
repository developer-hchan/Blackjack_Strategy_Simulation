from simulation import run_match
from cards import simulate_deck_draw, Card, Hand
import random
import unittest


class TestSplit(unittest.TestCase):
    # NOTE: I suggest looking at the print statements in the console to assist in assessing the test
    def test_ace_split(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(1,'heart'))
        player_hand.hand_list.append(Card(1,'diamond'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(8,'heart'))
        dealer_hand.hand_list.append(Card(11,'diamond'))

        random.seed(0)
        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'split', dealer_hit_soft_17= True, verbose= True)

        print(f'\nTEST_ACE_SPLIT.. player hand: ')
        for card in player_hand.hand_list:
            print(card)

        print(f'\nTEST_ACE_SPLIT.. dealer hand: ')
        for card in dealer_hand.hand_list:
            print(card)
        
        print('\n')

        # Hand AA will be 19 and should tie to dealer's 19; should return a value of 0
        # Hand BB will be 13 and should lost to dealer's 19; should return a value of -25.0
        self.assertEqual(expected_value, -25.0)


    # NOTE: I suggest looking at the print statements in the console to assist in assessing the test
    def test_ace_split2(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(1,'club'))
        player_hand.hand_list.append(Card(1,'spade'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(10,'club'))
        dealer_hand.hand_list.append(Card(10,'spade'))

        random.seed(2)
        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'split', dealer_hit_soft_17= True, verbose= True)

        print(f'\nTEST_ACE_SPLIT2.. player hand: ')
        for card in player_hand.hand_list:
            print(card)

        print(f'\nTEST_ACE_SPLIT2.. dealer hand: ')
        for card in dealer_hand.hand_list:
            print(card)
        
        print('\n')

        # Hand AA will be 13 and should lose to dealer's 20; should return a value of -25.0
        # Hand BB will be 14 and should lose to dealer's 20; should return a value of -25.0
        self.assertEqual(-50.0, expected_value)



if __name__ == "__main__":
    unittest.main()



