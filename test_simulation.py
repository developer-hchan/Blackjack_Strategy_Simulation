import unittest
import random
import csv

from game_state import GameState
from cards import Card
from cards import Hand
import simulation as sim
from simulation import dealer_turn
from simulation import generate_hand
from simulation import generate_dealer_hand
from simulation import check_4_blackjack
from simulation import player_turn
from simulation import split_phase
from simulation import evaluate
from simulation import player_turn_advance


class TestGenerateHands(unittest.TestCase):
    def test_generate_hand_hard(self):
        random_total = random.randint(4,20)
        hand = generate_hand(random_total, 'hard')

        self.assertEqual(random_total, hand.total)
        self.assertEqual('hard', hand.texture)
        self.assertEqual(2, len(hand.hand_list))


    def test_generate_hand_soft_1(self):
        random_total = random.randint(12,21)
        hand = generate_hand(random_total, 'soft')

        self.assertEqual(random_total, hand.total)
        self.assertEqual('soft', hand.texture)
        self.assertEqual(2, len(hand.hand_list))


    def test_generate_hand_soft_2(self):
        hand = generate_hand(12, 'soft')

        self.assertEqual(12, hand.total)
        self.assertEqual('soft', hand.texture)
        self.assertEqual(2, len(hand.hand_list))


    def test_generate_hand_soft_1(self):
        hand = generate_hand(21, 'soft')
        
        self.assertEqual(21, hand.total)
        self.assertEqual('soft', hand.texture)
        self.assertEqual(2, len(hand.hand_list))


    def test_generate_hand_split(self):
        hand = generate_hand(6, 'split')

        self.assertEqual(3, hand.hand_list[0].number)
        self.assertEqual(3, hand.hand_list[1].number)
        self.assertEqual(2, len(hand.hand_list))


    def test_generate_hand_split_2(self):
        hand = generate_hand(2, 'split')

        self.assertEqual(1, hand.hand_list[0].number)
        self.assertEqual(1, hand.hand_list[1].number)
        self.assertEqual(2, len(hand.hand_list))


    def test_generate_dealer_hand(self):
        dealer_hand = generate_dealer_hand(2)

        self.assertGreater(dealer_hand.total, 2+1)
        self.assertLess(dealer_hand.total, 22)
        self.assertEqual(2, len(dealer_hand.hand_list))


class TestCheck4Blackjack(unittest.TestCase):
    def test_player_blackjack(self):
        game = GameState()
        game.deck = []
        
        player_hand = Hand()
        player_hand.hand_list = [Card(10,'diamond'), Card(11,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(6, 'heart'), Card(11, 'heart')]

        check_4_blackjack(game)

        self.assertEqual(game.bet*game.blackjack_bonus, game.value)

    def test_dealer_blackjack(self):
        game = GameState()
        game.deck = []

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(4,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(11, 'heart'), Card(10, 'heart')]

        check_4_blackjack(game)

        self.assertEqual(-game.bet, game.value)

    def test_tie_blackjack(self):
        game = GameState()
        game.deck = []

        player_hand = Hand()
        player_hand.hand_list = [Card(10,'diamond'), Card(11,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(10, 'heart'), Card(11, 'heart')]

        check_4_blackjack(game)

        self.assertEqual(0, game.value)


class TestPlayerTurn(unittest.TestCase):
    def test_hit_hit(self):
        # loading a test dictionary from test_data.csv
        # NOTE: test_data is not necessarily accurate, it is just used for the testing of inputs and expected outputs
        with open('test_data.csv') as csv_file:
            reader = csv.reader(csv_file)
            test_dictionary = dict(reader)
        
        # after importing from the test_data.csv, the dictionary is storing the key as a large string, so we need to convert it back to a tuple
        for k,v in test_dictionary.items():
            # eval() converts the string-tuple back into a proper tuple
            # NOTE: by calling data_dictionary directly, it shouldn't maintain it's value for the other tests
            sim.data_dictionary[eval(k)] = float(v)
        
        game = GameState()
        game.deck = [2,9,2]

        player_hand = Hand()
        player_hand.hand_list = [Card(2,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(6, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='hit', dealer_face_up=6)
        dealer_turn(game)
        evaluate(game)

        # according to test_data.csv, a hard 11 should hit against a dealer_face_up of 6, so we expect the player_hand to draw the 9 for a total of 20
        # the dealer will then draw the remaining 2 in the deck, for a total of 17
        # the game value will then be 25.00 because the player won
        self.assertEqual(game.player_hands[0].total, 20)
        self.assertEqual(game.dealer_hand.total, 17)
        self.assertEqual(len(game.deck), 0)
        # eventhough 'double' has a higher value than stand, a hand can only 'hit' or 'stand' after having already hit
        self.assertEqual(game.value, game.bet)


    def test_hit_stand(self):
        # loading a test dictionary from test_data.csv
        # NOTE: test_data is not necessarily accurate, it is just used for the testing of inputs and expected outputs
        with open('test_data.csv') as csv_file:
            reader = csv.reader(csv_file)
            test_dictionary = dict(reader)
        
        # after importing from the test_data.csv, the dictionary is storing the key as a large string, so we need to convert it back to a tuple
        for k,v in test_dictionary.items():
            # eval() converts the string-tuple back into a proper tuple
            # NOTE: by calling data_dictionary directly, it shouldn't maintain it's value for the other tests
            sim.data_dictionary[eval(k)] = float(v)
        
        game = GameState()
        game.deck = [5,3]

        player_hand = Hand()
        player_hand.hand_list = [Card(5,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(7, 'heart'), Card(8, 'heart')]

        player_turn(game=game, player_first_choice='hit', dealer_face_up=7)
        dealer_turn(game)
        evaluate(game)

        # according to test_data.csv, a hard 17 should stand against a dealer_face_up of 7, so we expect the player_hand to stand after the initially drawing of the 5
        # the dealer will then draw the remaining 3 in the deck, for a total of 18
        # the game value will then be -25.00 because the player loses
        self.assertEqual(game.player_hands[0].total, 17)
        self.assertEqual(game.dealer_hand.total, 18)
        self.assertEqual(len(game.deck), 0)
        # eventhough 'double' has a higher value than stand, a hand can only 'hit' or 'stand' after having already hit
        self.assertEqual(game.value, -game.bet)


    def test_stand(self):
        game = GameState()
        game.deck = []

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(8,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(4, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='stand', dealer_face_up=4)

        self.assertEqual(game.player_hands[0].total, 15)


    def test_double(self):
        pass # test is done in Class TestEvaluate() below...

    def test_surrender(self):
        game = GameState()
        game.deck = []

        player_hand = Hand()
        player_hand.hand_list = [Card(10,'diamond'), Card(8,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='surrender', dealer_face_up=8)

        self.assertEqual(game.player_hands[0].total, 18)
        self.assertEqual(game.dealer_hand.total, 17)
        self.assertEqual(game.value, -0.5*game.bet)


    def test_split_aces(self):
        game = GameState()
        game.deck = [7, 10]

        player_hand = Hand()
        player_hand.hand_list = [Card(11,'diamond'), Card(11,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='split', dealer_face_up=8)

        self.assertEqual(len(game.player_hands), 2)
        self.assertEqual(18, game.player_hands[0].total)
        self.assertEqual(21, game.player_hands[1].total)


    def test_split_aces_2(self):
        game = GameState()
        game.deck = [7, 10]

        player_hand = Hand()
        player_hand.hand_list = [Card(1,'diamond'), Card(11,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='split', dealer_face_up=8)

        self.assertEqual(len(game.player_hands), 2)
        self.assertEqual(18, game.player_hands[0].total)
        self.assertEqual(21, game.player_hands[1].total)


    def test_split_aces_3(self):
        game = GameState()
        game.deck = [7, 10]

        player_hand = Hand()
        player_hand.hand_list = [Card(1,'diamond'), Card(1,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='split', dealer_face_up=8)

        self.assertEqual(len(game.player_hands), 2)
        self.assertEqual(18, game.player_hands[0].total)
        self.assertEqual(21, game.player_hands[1].total)


class TestSplitPhase(unittest.TestCase):
    def test_split_phase(self):
        game = GameState()
        game.deck = [4, 10]

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        split_phase(game)

        self.assertEqual(len(game.player_hands), 2)
        self.assertEqual(11, game.player_hands[0].total)
        self.assertEqual(17, game.player_hands[1].total)

    def test_split_phase_then_back_split(self):
        game = GameState()
        game.deck = [4, 7, 9, 8]

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        split_phase(game)

        self.assertEqual(len(game.player_hands), 3)
        self.assertEqual(11, game.player_hands[0].total)
        self.assertEqual(16, game.player_hands[1].total)
        self.assertEqual(15, game.player_hands[2].total)


    def test_split_phase_then_front_split(self):
        game = GameState()
        game.deck = [7, 4, 2, 11]

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        split_phase(game)

        self.assertEqual(len(game.player_hands), 3)
        self.assertEqual(9, game.player_hands[0].total)
        self.assertEqual(11, game.player_hands[1].total)
        self.assertEqual(18, game.player_hands[2].total)


class TestPlayerTurnAdvance(unittest.TestCase):
    def test_player_turn_advance(self):
        # loading a test dictionary from test_data.csv
        # NOTE: test_data is not necessarily accurate, it is just used for the testing of inputs and expected outputs
        with open('test_data.csv') as csv_file:
            reader = csv.reader(csv_file)
            test_dictionary = dict(reader)
        
        # after importing from the test_data.csv, the dictionary is storing the key as a large string, so we need to convert it back to a tuple
        for k,v in test_dictionary.items():
            # eval() converts the string-tuple back into a proper tuple
            # NOTE: by calling data_dictionary directly, it shouldn't maintain it's value for the other tests
            sim.data_dictionary[eval(k)] = float(v)
        
        config = {
            'decisions': ('stand','hit','double','surrender'),
            'double_after_split': True
            }
        
        game = GameState()
        game.deck = [7, 4, 11, 9, 9, 9]

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(10, 'heart'), Card(9, 'heart')]

        # after split phase, the player will be left with three hands with the following totals: soft 18, 11, 16
        split_phase(game)
        player_turn_advance(configuration=config, game=game, dealer_face_up=10)
        dealer_turn(game)
        evaluate(game)

        self.assertEqual(3, len(game.player_hands))
        # NOTE: all decision are based on what is in test_data.csv

        # soft 18 hits against a face-up 10: so player hand 1 will draw a 9, ending with a hard total of 17, with the cards: 7, 11, 9
        # loses against dealer hard 19: -25.00 to game.value
        self.assertEqual(17, game.player_hands[0].total)

        # hard 11 doubles against a face-up 10: so player hand 2 will draw a 9, ending with a hard total of 20, with the cards: 7, 4, 9
        # wins against dealer hard 19: 50.00 to game.value
        self.assertEqual(20, game.player_hands[1].total)

        # hard 16 should surrender against a face-up 10, but split hands don't have that option. The next best option is to stand, so player hand 3 will end with cards: 7, 9
        # loses against dealer hard 19: -25.00 to game.value
        self.assertEqual(16, game.player_hands[2].total)

        self.assertEqual(0.00, game.value)


    # NOTE: same as the test above, but doubling is not allowed
    def test_player_turn_advance_2(self):
        # loading a test dictionary from test_data.csv
        # NOTE: test_data is not necessarily accurate, it is just used for the testing of inputs and expected outputs
        with open('test_data.csv') as csv_file:
            reader = csv.reader(csv_file)
            test_dictionary = dict(reader)
        
        # after importing from the test_data.csv, the dictionary is storing the key as a large string, so we need to convert it back to a tuple
        for k,v in test_dictionary.items():
            # eval() converts the string-tuple back into a proper tuple
            # NOTE: by calling data_dictionary directly, it shouldn't maintain it's value for the other tests
            sim.data_dictionary[eval(k)] = float(v)
        
        config = {
            'decisions': ('stand','hit','surrender'),
            'double_after_split': True
            }
        
        game = GameState()
        game.deck = [7, 4, 11, 9, 9, 9]

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(10, 'heart'), Card(9, 'heart')]

        # after split phase, the player will be left with three hands with the following totals: soft 18, 11, 16
        split_phase(game)
        player_turn_advance(configuration=config, game=game, dealer_face_up=10)
        dealer_turn(game)
        evaluate(game)

        self.assertEqual(3, len(game.player_hands))
        # NOTE: all decision are based on what is in test_data.csv

        # soft 18 hits against a face-up 10: so player hand 1 will draw a 9, ending with a hard total of 17, with the cards: 7, 11, 9
        # loses against dealer hard 19: -25.00 to game.value
        self.assertEqual(17, game.player_hands[0].total)

        # hard 11 doubles against a face-up 10, but because that is not allowed the player will hit: so player hand 2 will draw a 9, ending with a hard total of 20, with the cards: 7, 4, 9
        # wins against dealer hard 19: 25.00 to game.value because the hands were not allowed to double
        self.assertEqual(20, game.player_hands[1].total)

        # hard 16 should surrender against a face-up 10, but split hands don't have that option. The next best option is to stand, so player hand 3 will end with cards: 7, 9
        # loses against dealer hard 19: -25.00 to game.value
        self.assertEqual(16, game.player_hands[2].total)

        self.assertEqual(-25.00, game.value)


    # NOTE: same as the test above, but surrendering and doubling are not allowed... making sure that a error won't be thrown if 'surrender' is not present in the original decision list
    def test_player_turn_advance_no_surrender_no_error(self):
        # loading a test dictionary from test_data.csv
        # NOTE: test_data is not necessarily accurate, it is just used for the testing of inputs and expected outputs
        with open('test_data.csv') as csv_file:
            reader = csv.reader(csv_file)
            test_dictionary = dict(reader)
        
        # after importing from the test_data.csv, the dictionary is storing the key as a large string, so we need to convert it back to a tuple
        for k,v in test_dictionary.items():
            # eval() converts the string-tuple back into a proper tuple
            # NOTE: by calling data_dictionary directly, it shouldn't maintain it's value for the other tests
            sim.data_dictionary[eval(k)] = float(v)
        
        config = {
            'decisions': ('stand','hit'),
            'double_after_split': True
            }
        
        game = GameState()
        game.deck = [7, 4, 11, 9, 9, 9]

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(10, 'heart'), Card(9, 'heart')]

        # after split phase, the player will be left with three hands with the following totals: soft 18, 11, 16
        split_phase(game)
        player_turn_advance(configuration=config, game=game, dealer_face_up=10)
        dealer_turn(game)
        evaluate(game)

        self.assertEqual(3, len(game.player_hands))
        # NOTE: all decision are based on what is in test_data.csv

        # soft 18 hits against a face-up 10: so player hand 1 will draw a 9, ending with a hard total of 17, with the cards: 7, 11, 9
        # loses against dealer hard 19: -25.00 to game.value
        self.assertEqual(17, game.player_hands[0].total)

        # hard 11 doubles against a face-up 10, but because that is not allowed the player will hit: so player hand 2 will draw a 9, ending with a hard total of 20, with the cards: 7, 4, 9
        # wins against dealer hard 19: 25.00 to game.value because the hands were not allowed to double
        self.assertEqual(20, game.player_hands[1].total)

        # hard 16 should surrender against a face-up 10, but split hands don't have that option. The next best option is to stand, so player hand 3 will end with cards: 7, 9
        # loses against dealer hard 19: -25.00 to game.value
        self.assertEqual(16, game.player_hands[2].total)

        self.assertEqual(-25.00, game.value)


class TestDealerTurn(unittest.TestCase):
    def test_hit_on_soft_17(self):
        game = GameState()
        game.dealer_hit_soft_17 = True
        game.deck = [11]

        game.dealer_hand.hand_list = [Card(6, 'heart'), Card(11, 'heart')]
        dealer_turn(game)

        self.assertEqual(18, game.dealer_hand.total)

    def test_stand_on_soft_17(self):
        game = GameState()
        game.dealer_hit_soft_17 = False
        game.deck = [11]

        game.dealer_hand.hand_list = [Card(6, 'heart'), Card(11, 'heart')]
        dealer_turn(game)

        self.assertEqual(17, game.dealer_hand.total)

    def test_hit_on_soft_17_multiple_cards(self):
        game = GameState()
        game.dealer_hit_soft_17 = True
        game.deck = [2]

        game.dealer_hand.hand_list = [Card(4, 'heart'), Card(11, 'heart'), Card(2, 'heart')]
        dealer_turn(game)

        self.assertEqual(19, game.dealer_hand.total)


class TestEvaluate(unittest.TestCase):
    # evaluate's job is to compare a player's hand after their turn and a dealer's hand after their turn and award money (value) accordingly
    def test_evaluate_hit(self):
        game = GameState()
        game.deck = [6]

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='hit', dealer_face_up=8)
        dealer_turn(game=game)

        evaluate(game)

        self.assertEqual(game.bet, game.value)


    def test_evaluate_player_bust(self):
        game = GameState()
        game.deck = [10, 2, 7, 8, 11]

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='hit', dealer_face_up=8)
        dealer_turn(game=game)

        evaluate(game)

        self.assertEqual(24, game.player_hands[0].total)
        self.assertEqual(-game.bet, game.value)
        self.assertEqual(4, len(game.deck)) # player should stop drawing cards after going above 21
    

    # game.value should be -game.bet (25.00) in this case because player busting takes priority over dealer busting
    def test_evaluate_player_bust_first(self):
        game = GameState()
        game.deck = [10, 10, 7, 8, 11]

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(5, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='hit', dealer_face_up=5)
        dealer_turn(game=game)

        evaluate(game)

        self.assertEqual(24, game.player_hands[0].total)
        self.assertEqual(24, game.dealer_hand.total)
        self.assertEqual(-game.bet, game.value)
        self.assertEqual(3, len(game.deck))
    

    def test_evaluate_stand_lose(self):
        game = GameState()
        game.deck = []

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(8, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='stand', dealer_face_up=8)
        dealer_turn(game=game)

        evaluate(game)

        self.assertEqual(-game.bet, game.value)


    def test_evaluate_double_win(self):
        game = GameState()
        game.deck = [7,6]

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(4, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='double', dealer_face_up=4)
        dealer_turn(game=game)

        evaluate(game)

        self.assertEqual(2*game.bet, game.value)

    
    def test_evaluate_double_lose(self):
        game = GameState()
        game.deck = [2,6]

        player_hand = Hand()
        player_hand.hand_list = [Card(7,'diamond'), Card(7,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(4, 'heart'), Card(9, 'heart')]

        player_turn(game=game, player_first_choice='double', dealer_face_up=4)
        dealer_turn(game=game)

        evaluate(game)

        self.assertEqual(-2*game.bet, game.value)


    # can evaluate multiple hands
    def test_evaluate_multiple_hands(self):
        game = GameState()
        game.deck = [8, 9, 10, 8]

        player_hand = Hand()
        player_hand.hand_list = [Card(9,'diamond'), Card(9,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(7, 'heart'), Card(10, 'heart')]

        # after split phase, the player should have 3 hands with the following totals: 17, 19, 17
        # dealer has 17
        # here are the follwing value + -'s: 0.00 + 25.00 + 0.00 = 25.00
        split_phase(game)
        dealer_turn(game)
        evaluate(game)

        self.assertEqual(3, len(game.player_hands))
        self.assertEqual(game.value, 25.00)

    def test_evaluate_multiple_hands_2(self):
        game = GameState()
        game.deck = [8, 9, 10, 8]

        player_hand = Hand()
        player_hand.hand_list = [Card(9,'diamond'), Card(9,'diamond')]
        game.player_hands.append(player_hand)
        game.dealer_hand.hand_list = [Card(10, 'heart'), Card(10, 'heart')]

        # after split phase, the player should have 3 hands with the following totals: 17, 19, 17
        # dealer has 20
        # here are the follwing value + -'s: -25.00 + -25.00 + -25.00 = -75.00
        split_phase(game)
        dealer_turn(game)
        evaluate(game)

        self.assertEqual(3, len(game.player_hands))
        self.assertEqual(game.value, -75.00)


if __name__ == '__main__':
    unittest.main()