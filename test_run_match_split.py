import random
import unittest
import csv

from simulation import run_match, DATA_DICTIONARY
from cards import Card, Hand


class TestSplitAces(unittest.TestCase):
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

        # Hand AA will be 13 and should lose to dealer's 20; should return a value of -25.0
        # Hand BB will be 14 and should lose to dealer's 20; should return a value of -25.0
        self.assertEqual(-50.0, expected_value)

    
class TestSplit(unittest.TestCase):
    # loading a test dictionary from test_data.csv
    # NOTE: test_data is not necessarily accurate, it is just used for the testing of inputs and expected outputs
    with open('test_data.csv') as csv_file:
        reader = csv.reader(csv_file)
        test_dictionary = dict(reader)

    # after importing from the test_data.csv, the dictionary is storing the key as a large string, so we need to convert it back to a tuple
    for k,v in test_dictionary.items():
        # eval() converts the string-tuple back into a proper tuple
        DATA_DICTIONARY[eval(k)] = float(v)

    # for k,v in DATA_DICTIONARY.items():
    #     print(f'{k} {type(k)}: {v} {type(v)}')


    def test_split(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(4,'spade'))
        player_hand.hand_list.append(Card(10,'club'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(10,'diamond'))
        dealer_hand.hand_list.append(Card(10,'heart'))

        random.seed(0)
        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'split', dealer_hit_soft_17= True, verbose= True)

        print(f'\nTEST_SPLIT.. player hand: ')
        for card in player_hand.hand_list:
            print(card)

        print(f'\nTEST_SPLIT.. dealer hand: ')
        for card in dealer_hand.hand_list:
            print(card)

        # hand A will 15, against dealer 20, the hand should surrender according to test_data.csv; -12.5
        # hand B will draw to 19 and lost against dealer 20; -25.0
        self.assertEqual(-37.5, expected_value)
    
    
    # hand A will split a second time; i.e. recursively call split() again within split()
    def test_split_split(self):
        player_hand = Hand()
        player_hand.hand_list.append(Card(2,'spade'))
        player_hand.hand_list.append(Card(2,'club'))

        dealer_hand = Hand()
        dealer_hand.hand_list.append(Card(10,'diamond'))
        dealer_hand.hand_list.append(Card(10,'heart'))

        random.seed(2)
        expected_value = run_match(player_hand= player_hand,dealer_hand= dealer_hand, bet= 25.00, player_first_choice= 'split', dealer_hit_soft_17= True, verbose= True)

        print(f'\nTEST_SPLIT_SPLIT.. player hand: ')
        for card in player_hand.hand_list:
            print(card)

        print(f'\nTEST_SPLIT_SPLIT.. dealer hand: ')
        for card in dealer_hand.hand_list:
            print(card)

        # hand A will be 2 of spades and 2 hearts, it will split again (recursively call split()) and lose to dealer 20; should have -50 expected value
        # hand B will bust; should have a -25 value
        self.assertEqual(-75, expected_value)



if __name__ == "__main__":
    unittest.main()



